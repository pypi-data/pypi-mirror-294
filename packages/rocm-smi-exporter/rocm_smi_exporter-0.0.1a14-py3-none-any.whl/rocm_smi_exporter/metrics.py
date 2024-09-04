"""
Metric names and labels are kept consistent with DCGM whenever possible.
"""

import logging
import time

from dataclasses import dataclass
from prometheus_client import start_http_server, Gauge
from pyrsmi import rocml

from rocm_smi_exporter.kubelet import DevK8sInfo, query_kubelet_dev_alloc

from .wrapper import *

import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)


import platform

HOSTNAME = platform.node()

LABEL_HOSTNAME = "Hostname"
LABEL_RSMI_VERSION = "rsmiVersion"
LABEL_ROCM_KERNEL_VERSION = "rocmKernelVersion"
COMMON_LABELS = [LABEL_HOSTNAME, LABEL_RSMI_VERSION, LABEL_ROCM_KERNEL_VERSION]

LABEL_UID = "uid"
LABEL_PCI_ID = "pci_bus_id"
LABEL_GPU = "gpu"
LABEL_MODEL_NAME = "modelName"
PER_GPU_COMMON_LABELS = [LABEL_UID, LABEL_PCI_ID, LABEL_GPU, LABEL_MODEL_NAME]

"""
NOTE: Prometheus will relabel these metrics by appending 'exported_' to the original label.
https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config
"""
LABEL_K8S_CONTAINER_NAME = "container"
LABEL_K8S_POD_NAME = "pod"
LABEL_K8S_NAMESPACE_NAME = "namespace"
PER_GPU_K8S_LABELS = [
    LABEL_K8S_CONTAINER_NAME,
    LABEL_K8S_POD_NAME,
    LABEL_K8S_NAMESPACE_NAME,
]


def _get_common_labels():
    """
    Returns a dict of the common labels for metric
    """
    res = {}
    res[LABEL_HOSTNAME] = HOSTNAME
    res[LABEL_RSMI_VERSION] = rocml.smi_get_version()
    res[LABEL_ROCM_KERNEL_VERSION] = rocml.smi_get_kernel_version()
    return res


# These names are mimicing dcgm-exporter:
# DCGM_FI_DEV_GPU_UTIL and DCGM_FI_DEV_MEM_COPY_UTIL
METRIC_GPU_COUNT = "ROCM_SMI_DEV_GPU_COUNT"
METRIC_GPU_UTIL = "ROCM_SMI_DEV_GPU_UTIL"
METRIC_GPU_MEM_TOTAL = "ROCM_SMI_DEV_GPU_MEM_TOTAL"
METRIC_GPU_MEM_USED = "ROCM_SMI_DEV_GPU_MEM_USED"
METRIC_GPU_MEM_UTIL = "ROCM_SMI_DEV_MEM_UTIL"
METRIC_GPU_CU_OCCUPANCY = "ROCM_SMI_DEV_CU_OCCUPANCY"
METRIC_GPU_TEMP = "ROCM_SMI_DEV_TEMP"
METRIC_GPU_CUR_POWER = "ROCM_SMI_DEV_CUR_POWER"
METRIC_GPU_AVG_POWER = "ROCM_SMI_DEV_AVG_POWER"
METRIC_GPU_MAX_POWER = "ROCM_SMI_DEV_MAX_POWER"
METRIC_GPU_MEM_BUSY_PERCENT = "ROCM_SMI_DEV_MEM_BUSY_PERCENT"
METRIC_GPU_SCLK = "ROCM_SMI_DEV_SCLK"
METRIC_GPU_MCLK = "ROCM_SMI_DEV_MCLK"


class GPUMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    @dataclass
    class Config:
        port: int
        polling_interval_seconds: int
        resolve_k8s_dev_alloc: bool
        ignore_non_k8s_metrics: bool

    def __init__(self, config: Config):
        self.config = config
        self.common_labels = _get_common_labels()

        self.gpu_count = Gauge(METRIC_GPU_COUNT, "GPU count.", COMMON_LABELS)

        per_gpu_metric_labels = COMMON_LABELS + PER_GPU_COMMON_LABELS
        if self.config.resolve_k8s_dev_alloc:
            per_gpu_metric_labels += PER_GPU_K8S_LABELS

        self.define_per_gpu_metrics(per_gpu_metric_labels)

    def run_read_metrcs_loop(self):
        """Metrics fetching loop"""
        logger.info(f"Starting expoerter on :{self.config.port}")
        start_http_server(self.config.port)
        while True:
            logger.info(f"Fetching metrics ...")
            self.read_metrics()
            time.sleep(self.config.polling_interval_seconds)

    def read_metrics(self):
        """
        Get metrics from application and refresh Prometheus metrics.
        """
        ngpus = rocml.smi_get_device_count()
        self.gpu_count.labels(**self.common_labels).set(ngpus)

        k8s_dev_alloc = {}
        if self.config.resolve_k8s_dev_alloc:
            try:
                k8s_dev_alloc = query_kubelet_dev_alloc(
                    "/var/lib/kubelet/pod-resources/kubelet.sock"
                )
            except Exception as e:
                logger.warn(f"Cannot query kubelet pod resources API, error {e}")
        logger.debug(f"{k8s_dev_alloc=}")

        for dev in range(ngpus):
            pci_id = get_device_pci_id(dev)
            if (
                pci_id not in k8s_dev_alloc
                and self.config.resolve_k8s_dev_alloc
                and self.config.ignore_non_k8s_metrics
            ):
                logger.info(f"Ignored gpu:{dev} because it has no K8s info.")
                continue
            per_gpu_metric_labels = self.get_per_gpu_metric_labels(dev, k8s_dev_alloc)
            self.fetch_per_gpu_metrics(dev, per_gpu_metric_labels)

    def define_per_gpu_metrics(self, per_gpu_metric_labels: dict):
        self.gpu_util = Gauge(
            METRIC_GPU_UTIL, "GPU utilization (in %).", per_gpu_metric_labels
        )
        self.gpu_mem_used = Gauge(
            METRIC_GPU_MEM_USED, "GPU memory used (in Byte).", per_gpu_metric_labels
        )
        self.gpu_mem_total = Gauge(
            METRIC_GPU_MEM_TOTAL, "GPU memory total (in Byte).", per_gpu_metric_labels
        )
        self.gpu_mem_util = Gauge(
            METRIC_GPU_MEM_UTIL, "GPU memory utilization (in %).", per_gpu_metric_labels
        )
        self.gpu_cu_occupancy = Gauge(
            METRIC_GPU_CU_OCCUPANCY, "GPU CU occupancy (in %).", per_gpu_metric_labels
        )
        self.gpu_temp = Gauge(
            METRIC_GPU_TEMP, "GPU temperature (in c).", per_gpu_metric_labels
        )
        self.gpu_cur_power = Gauge(
            METRIC_GPU_CUR_POWER, "GPU current power, (in W).", per_gpu_metric_labels
        )
        self.gpu_max_power = Gauge(
            METRIC_GPU_MAX_POWER, "GPU max power, (in W).", per_gpu_metric_labels
        )
        self.gpu_avg_power = Gauge(
            METRIC_GPU_AVG_POWER,
            "GPU average power in the last sample window. This could be around 100ms or so, (in W).",
            per_gpu_metric_labels,
        )
        self.gpu_mem_busy_percent = Gauge(
            METRIC_GPU_MEM_BUSY_PERCENT,
            "GPU Memory Read/Write Activity (in %).",
            per_gpu_metric_labels,
        )
        self.gpu_sclk = Gauge(
            METRIC_GPU_SCLK,
            "GPU current clock frequency (in MHz).",
            per_gpu_metric_labels,
        )
        self.gpu_mclk = Gauge(
            METRIC_GPU_MCLK,
            "GPU memory current frequency (in MHz).",
            per_gpu_metric_labels,
        )

    def get_per_gpu_metric_labels(self, dev: int, k8s_dev_alloc: dict):
        uid = rocml.smi_get_device_unique_id(dev)
        dev_model_name = rocml.smi_get_device_name(dev)
        pci_id = get_device_pci_id(dev)

        labels = self.common_labels.copy()

        labels[LABEL_UID] = uid
        labels[LABEL_PCI_ID] = pci_id
        labels[LABEL_GPU] = dev
        labels[LABEL_MODEL_NAME] = dev_model_name

        if self.config.resolve_k8s_dev_alloc:
            k8s_info = k8s_dev_alloc.get(pci_id, DevK8sInfo())
            labels[LABEL_K8S_CONTAINER_NAME] = k8s_info.container
            labels[LABEL_K8S_POD_NAME] = k8s_info.pod
            labels[LABEL_K8S_NAMESPACE_NAME] = k8s_info.namespace
        return labels

    def fetch_per_gpu_metrics(self, dev: int, labels: dict):
        util = rocml.smi_get_device_utilization(dev)
        self.gpu_util.labels(**labels).set(util)

        mem_used = rocml.smi_get_device_memory_used(dev)
        self.gpu_mem_used.labels(**labels).set(mem_used)

        mem_total = rocml.smi_get_device_memory_total(dev)
        self.gpu_mem_total.labels(**labels).set(mem_total)

        mem_ratio = mem_used / mem_total * 100
        self.gpu_mem_util.labels(**labels).set(mem_ratio)

        cu_occupancy = smi_get_device_cu_occupancy(dev)
        self.gpu_cu_occupancy.labels(**labels).set(cu_occupancy)

        temp = get_cur_temp(dev)
        self.gpu_temp.labels(**labels).set(temp)

        cur_power = get_cur_power(dev)
        self.gpu_cur_power.labels(**labels).set(cur_power)

        avg_power = get_avg_power(dev)
        self.gpu_avg_power.labels(**labels).set(avg_power)

        max_power = get_max_power(dev)
        self.gpu_max_power.labels(**labels).set(max_power)

        mem_busy = get_mem_busy_percent(dev)
        self.gpu_mem_busy_percent.labels(**labels).set(mem_busy)

        sclk = get_sclk(dev)
        self.gpu_sclk.labels(**labels).set(sclk)

        mclk = get_mclk(dev)
        self.gpu_mclk.labels(**labels).set(mclk)

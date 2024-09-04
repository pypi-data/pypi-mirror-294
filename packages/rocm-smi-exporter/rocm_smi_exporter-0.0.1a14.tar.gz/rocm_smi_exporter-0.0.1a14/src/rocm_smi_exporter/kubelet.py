import contextlib
import os
import grpc

from typing import Dict

from github.com.kubernetes.kubelet.pkg.apis.podresources.v1 import api_pb2_grpc
from github.com.kubernetes.kubelet.pkg.apis.podresources.v1 import api_pb2


# Records the information of this device in the context of Kubernetes.
class DevK8sInfo:
    def __init__(
        self,
        namespace: str = "",
        pod: str = "",
        container: str = "",
        resource_name: str = "",
    ):
        self.namespace = namespace
        self.pod = pod
        self.container = container
        self.resource_name = resource_name


def query_kubelet_dev_alloc(socket_path) -> Dict[str, DevK8sInfo]:
    if not os.path.exists(socket_path):
        raise FileNotFoundError(f"Cannot find kubelet socket file at {socket_path}")

    c = _connect_to_server(socket_path)
    if not c:
        raise ConnectionError(f"Cannot connect to Kubelet socket at {socket_path}")

    with contextlib.closing(c):
        client = api_pb2_grpc.PodResourcesListerStub(c)
        timeout_seconds = 0.1
        resp = client.List(api_pb2.ListPodResourcesRequest(), timeout=timeout_seconds)

        device_to_pod_map = {}
        for pod in resp.pod_resources:
            for container in pod.containers:
                for devices in container.devices:
                    for device_id in devices.device_ids:
                        # Change everything to upper case.
                        device_id = device_id.upper()
                        device_to_pod_map[device_id] = DevK8sInfo(
                            namespace=pod.namespace,
                            pod=pod.name,
                            container=container.name,
                            resource_name=devices.resource_name,
                        )

    return device_to_pod_map


def _connect_to_server(socket):
    options = [("grpc.default_authority", "localhost")]
    channel = grpc.insecure_channel(f"unix://{socket}", options=options)

    try:
        connection_timeout_seconds = 0.1
        grpc.channel_ready_future(channel).result(timeout=connection_timeout_seconds)
    except grpc.FutureTimeoutError as err:
        return None

    return channel

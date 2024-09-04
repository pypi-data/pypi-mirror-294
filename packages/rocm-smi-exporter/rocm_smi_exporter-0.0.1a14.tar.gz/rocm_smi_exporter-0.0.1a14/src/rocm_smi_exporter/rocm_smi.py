"""
This file contains code copied (or sometimes modified) from [rocm_smi.py](
    https://github.com/ROCm/rocm_smi_lib/blob/amd-staging/python_smi_tools/rocm_smi.py
)

It's easier to manage the correspondance with the file with the same name.
"""

import logging

from ctypes import *
from .rsmiBindings import *
from pyrsmi import rocml


# This loads librocm into rocm_lib
rocml.smi_initialize()

from pyrsmi.rocml import rocm_lib as rocmsmi


def getTemp(device):
    """Display the current temperature from a given device's sensor

    :param device: DRM device identifier
    :param sensor: Temperature sensor identifier
    :param silent: Turn on to silence error output
        (you plan to handle manually). Default is on.
    """
    temp = c_int64(0)
    RSMI_TEMP_CURRENT = 0x0
    SENSOR_INDEX = 1  # for junction
    ret = rocmsmi.rsmi_dev_temp_metric_get(
        c_uint32(device), SENSOR_INDEX, RSMI_TEMP_CURRENT, byref(temp)
    )
    if rocml.rsmi_ret_ok(ret):
        return temp.value / 1000
    return -1


def getPower(device, power_type):
    """Return dictionary of power responses.
        Response power dictionary:

        .. code-block:: python

            {
                'power': string wattage response or 'N/A' (for not RSMI_STATUS_SUCCESS),
                'power_type': power type string - 'Current Socket' or 'Average',
                'unit': W (Watt)
                'ret': response of rsmi_dev_power_get(device, byref(power), byref(power_type))
            }

    :param device: DRM device identifier
    """

    power = c_int64(0)
    power_ret_dict = {
        "power": "N/A",
        "power_type": "N/A",
        "unit": "W",
        "ret": rsmi_status_t.RSMI_STATUS_NOT_SUPPORTED,
    }
    ret = rocmsmi.rsmi_dev_power_get(device, byref(power), byref(power_type))
    if ret == rsmi_status_t.RSMI_STATUS_SUCCESS:
        power_ret_dict = {
            "power": str(power.value / 1000000),
            "power_type": rsmi_power_type_dict[power_type.value],
            "unit": "W",
            "ret": ret,
        }
    else:
        power_ret_dict["ret"] = ret
    return power_ret_dict


def getMaxPower(device, silent=False):
    """Return the maximum power cap of a given device

    :param device: DRM device identifier
    :param silent: Turn on to silence error output
        (you plan to handle manually). Default is off.
    """
    power_cap = c_uint64()
    ret = rocmsmi.rsmi_dev_power_cap_get(device, 0, byref(power_cap))
    if rsmi_ret_ok(ret, device, "get_power_cap", silent):
        # take floor of result (round down to nearest integer)
        return float(power_cap.value / 1000000) // 1
    return -1


def rsmi_ret_ok(my_ret, device=None, metric=None, silent=True):
    """Returns true if RSMI call status is 0 (success)

        If status is not 0, error logs are written to the debug log and false is returned

    :param device: DRM device identifier
    :param my_ret: Return of RSMI call (rocm_smi_lib API)
    :param metric: Parameter of GPU currently being analyzed
    :param silent: Echo verbose error response.
        True silences err output, False does not silence err output (default).
    """
    if my_ret != rsmi_status_t.RSMI_STATUS_SUCCESS:
        err_str = c_char_p()
        rocmsmi.rsmi_status_string(my_ret, byref(err_str))
        # leaving the commented out prints/logs to help identify errors in the future
        # print("error string = " + str(err_str))
        # print("error string (w/ decode)= " + str(err_str.value.decode()))
        returnString = ""
        if device is not None:
            returnString += "%s GPU[%s]:" % (my_ret, device)
        if metric is not None:
            returnString += " %s: " % (metric)
        else:
            metric = ""
        if err_str.value is not None:
            returnString += "%s\t" % (err_str.value.decode())
        return False
    return True


def getMemoryBusyPercent(device):
    memoryUse = c_int64()
    ret = rocmsmi.rsmi_dev_memory_busy_percent_get(device, byref(memoryUse))
    if rsmi_ret_ok(ret, device, "% memory use"):
        return memoryUse.value
    return -1


def getOdSclk(device):
    rsmi_od = c_int32()
    ret = rocmsmi.rsmi_dev_overdrive_level_get(device, byref(rsmi_od))
    if rsmi_ret_ok(ret, device, "get_overdrive_level_sclk"):
        return rsmi_od.value
    return -1


def getOdMclk(device):
    rsmi_od = c_int32()
    ret = rocmsmi.rsmi_dev_mem_overdrive_level_get(device, byref(rsmi_od))
    if rsmi_ret_ok(ret, device, "get_overdrive_level_sclk"):
        return rsmi_od.value
    return -1


def getClkFreq(device, clk_defined: str):
    freq = rsmi_frequencies_t()
    if (
        rocmsmi.rsmi_dev_gpu_clk_freq_get(
            device, rsmi_clk_names_dict[clk_defined], None
        )
        == 1
    ):
        ret = rocmsmi.rsmi_dev_gpu_clk_freq_get(
            device, rsmi_clk_names_dict[clk_defined], byref(freq)
        )
        if rsmi_ret_ok(
            ret, device, "get_gpu_clk_freq_" + str(clk_defined), silent=True
        ):
            levl = freq.current
            if levl >= freq.num_supported:
                return -1
            return freq.frequency[levl] / 1000000


def smi_get_device_pci_id(dev):
    """returns unique PCI ID of the device in 64bit Hex with format:
       BDFID = ((DOMAIN & 0xffffffff) << 32) | ((BUS & 0xff) << 8) |
                    ((DEVICE & 0x1f) <<3 ) | (FUNCTION & 0x7)

    This was adapted from smi_get_device_pci_id() in
    https://github.com/ROCm/pyrsmi/blob/main/pyrsmi/rocml.py
    """
    bdfid = c_uint64()
    ret = rocmsmi.rsmi_dev_pci_id_get(dev, byref(bdfid))
    return bdfid.value if rocml.rsmi_ret_ok(ret) else -1


def get_device_pci_id(dev: int):
    """Format device_bus_id as fixed format string.

    :param device_bus_id: Device/GPU's PCI bus ID
    :return formatted GPU ID

    This was adapted from getBus() in
    github.com/ROCm/rocm_smi_lib/blob/amd-staging/python_smi_tools/rocm_smi.py

    AMD's device plugin uses this formated bus ID as device identifier.
    NVIDIA uses GPU's uuid.
    """
    device_bus_id = smi_get_device_pci_id(dev)
    domain = (device_bus_id >> 32) & 0xFFFFFFFF
    bus = (device_bus_id >> 8) & 0xFF
    device = (device_bus_id >> 3) & 0x1F
    function = device_bus_id & 0x7
    dev_id = "{:04X}:{:02X}:{:02X}.{:0X}".format(domain, bus, device, function)
    return dev_id.upper()


def smi_get_device_cu_occupancy(dev):
    """returns list of process ids running compute on the device dev"""
    num_procs = rocml.c_uint32()
    ret = rocmsmi.rsmi_compute_process_info_get(None, rocml.byref(num_procs))
    if rocml.rsmi_ret_ok(ret):
        buff_sz = num_procs.value + 10
        proc_info = (rocml.rsmi_process_info_t * buff_sz)()
        ret2 = rocmsmi.rsmi_compute_process_info_get(
            rocml.byref(proc_info), rocml.byref(num_procs)
        )

        return (
            sum(proc_info[i].cu_occupancy for i in range(num_procs.value))
            if rocml.rsmi_ret_ok(ret2)
            else -1
        )
    else:
        return -1

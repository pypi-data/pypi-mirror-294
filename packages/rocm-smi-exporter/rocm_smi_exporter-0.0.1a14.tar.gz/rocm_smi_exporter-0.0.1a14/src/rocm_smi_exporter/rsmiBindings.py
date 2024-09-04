"""
This file contains code copied (or sometimes modified) from [rocm_smi.py](
    https://github.com/ROCm/rocm_smi_lib/blob/amd-staging/python_smi_tools/rsmiBindings.py
)

It's easier to manage the correspondance with the file with the same name.
"""

from ctypes import *


class rsmi_status_t(c_int):
    RSMI_STATUS_SUCCESS = 0x0
    RSMI_STATUS_INVALID_ARGS = 0x1
    RSMI_STATUS_NOT_SUPPORTED = 0x2
    RSMI_STATUS_FILE_ERROR = 0x3
    RSMI_STATUS_PERMISSION = 0x4
    RSMI_STATUS_OUT_OF_RESOURCES = 0x5
    RSMI_STATUS_INTERNAL_EXCEPTION = 0x6
    RSMI_STATUS_INPUT_OUT_OF_BOUNDS = 0x7
    RSMI_STATUS_INIT_ERROR = 0x8
    RSMI_INITIALIZATION_ERROR = RSMI_STATUS_INIT_ERROR
    RSMI_STATUS_NOT_YET_IMPLEMENTED = 0x9
    RSMI_STATUS_NOT_FOUND = 0xA
    RSMI_STATUS_INSUFFICIENT_SIZE = 0xB
    RSMI_STATUS_INTERRUPT = 0xC
    RSMI_STATUS_UNEXPECTED_SIZE = 0xD
    RSMI_STATUS_NO_DATA = 0xE
    RSMI_STATUS_UNEXPECTED_DATA = 0xF
    RSMI_STATUS_BUSY = 0x10
    RSMI_STATUS_REFCOUNT_OVERFLOW = 0x11
    RSMI_STATUS_SETTING_UNAVAILABLE = 0x12
    RSMI_STATUS_AMDGPU_RESTART_ERR = 0x13
    RSMI_STATUS_UNKNOWN_ERROR = 0xFFFFFFFF


class rsmi_power_type_t(c_int):
    RSMI_AVERAGE_POWER = c_int(0)
    RSMI_CURRENT_POWER = c_int(1)
    RSMI_INVALID_POWER = c_int(0xFFFFFFFF)


rsmi_power_type_dict = {
    0: "AVERAGE",
    1: "CURRENT SOCKET",
    0xFFFFFFFF: "INVALID_POWER_TYPE",
}

rsmi_clk_names_dict = {
    "sclk": 0x0,
    "fclk": 0x1,
    "dcefclk": 0x2,
    "socclk": 0x3,
    "mclk": 0x4,
}

RSMI_MAX_NUM_FREQUENCIES = 33


class rsmi_frequencies_t(Structure):
    _fields_ = [
        ("has_deep_sleep", c_bool),
        ("num_supported", c_int32),
        ("current", c_uint32),
        ("frequency", c_uint64 * RSMI_MAX_NUM_FREQUENCIES),
    ]

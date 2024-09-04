from .rocm_smi import *
from .rsmiBindings import *


def _get_power_value(get_power_result: dict):
    return (
        get_power_result["power"]
        if get_power_result["ret"] == rsmi_status_t.RSMI_STATUS_SUCCESS
        else -1
    )


def get_cur_power(dev):
    return _get_power_value(getPower(dev, rsmi_power_type_t.RSMI_CURRENT_POWER))


def get_avg_power(dev):
    return _get_power_value(getPower(dev, rsmi_power_type_t.RSMI_AVERAGE_POWER))


def get_max_power(dev):
    return getMaxPower(dev, silent=True)


def get_cur_temp(dev):
    return getTemp(dev)


def get_mem_busy_percent(dev):
    return getMemoryBusyPercent(dev)


def get_sclk(dev):
    return getClkFreq(dev, "sclk")


def get_mclk(dev):
    return getClkFreq(dev, "mclk")

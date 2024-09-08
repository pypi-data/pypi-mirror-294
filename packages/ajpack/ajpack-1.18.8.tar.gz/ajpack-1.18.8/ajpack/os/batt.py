import psutil #type:ignore
from psutil import _common

def get_battery_status() -> dict[str, str]:
    """
    Works only on a device with a batterie! Raises an error, if no battery.

    Returns:
        - percent
        - seconds_left
        - power_plugged

    :return (dict[str, str]): The current battery status.
    """
    battery: _common.sbattery = psutil.sensors_battery()
    
    return {
        "percent":       str(battery.percent),
        "seconds_left":  str(battery.secsleft),
        "power_plugged": str(battery.power_plugged),
    }
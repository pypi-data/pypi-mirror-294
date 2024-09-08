import psutil #type:ignore

def get_battery_status() -> dict[str, str]:
    """
    Works only on a device with a batterie! Raises an error, if no battery.

    :return: The current battery status.
    """
    battery = psutil.sensors_battery()
    return {
        "percent": battery.percent,
        "seconds_left": battery.secsleft,
        "power_plugged": battery.power_plugged
    }
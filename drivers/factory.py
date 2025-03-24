from drivers.serial import SerialDriver
from drivers.tcp import TCPDriver


def get_driver(driver_type: str, config: dict):
    if driver_type == "serial":
        return SerialDriver(**config)
    elif driver_type == "tcp":
        return TCPDriver(**config)
    else:
        raise ValueError(f"Unsupported driver: {driver_type}")

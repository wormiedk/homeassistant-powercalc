from __future__ import annotations

import requests

from .errors import ConnectionError
from .powermeter import PowerMeasurementResult, PowerMeter


class ShellyPowerMeter(PowerMeter):
    def __init__(self, shelly_ip: str, timeout: int = 5):
        self.meter_uri = "http://{}/status/".format(shelly_ip)
        self.timeout = timeout
        self.validate_connection()

    def get_power(self) -> PowerMeasurementResult:
        r = requests.get(self.meter_uri, timeout=self.timeout)
        json = r.json()
        return PowerMeasurementResult(
            float(json["meters"][0]["power"]),
            float(json["meters"][0]["timestamp"]),
        )

    def validate_connection(self) -> bool:
        try:
            requests.get(self.meter_uri, timeout=self.timeout)
        except requests.RequestException as e:
            raise ConnectionError("Could not connect to Shelly Plug")

from typing import Protocol, runtime_checkable
import requests
import random


@runtime_checkable
class TemperatureSensor(Protocol):
    def read_temperature(self) -> float:
        ...

    def get_sensor_id(self) -> str:
        ...


class WeatherAPISensor:
    def read_temperature(self) -> float:
        try:
            url = "https://wttr.in/Odesa?format=%t"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            temperature = response.text.strip().replace("+", "").replace("°C", "")
            return float(temperature)

        except (requests.RequestException, ValueError) as error:
            raise RuntimeError("Не вдалося отримати температуру з API!") from error

    def get_sensor_id(self) -> str:
        return "WAS26-Odesa"


class SimulatedSensor:
    def __init__(self, base: float, deviation: float):
        self.base = base
        self.deviation = deviation

    def read_temperature(self) -> float:
        return self.base + random.uniform(-self.deviation, self.deviation)

    def get_sensor_id(self) -> str:
        return "SIMULATED-001"


class FakeAlways25:
    def read_temperature(self) -> float:
        return 25.0

    def get_sensor_id(self) -> str:
        return "Fake-25"


class BrokenSensor:
    def read_temperature(self) -> float:
        raise RuntimeError("Датчик зламаний!")

    def get_sensor_id(self) -> str:
        return "BROKEN-999"


def monitor_room(sensors: list[TemperatureSensor]) -> None:
    for sensor in sensors:
        sensor_id = sensor.get_sensor_id()

        try:
            temperature = sensor.read_temperature()
            print(f"[{sensor_id}] Температура: {temperature:.1f} °C")

        except Exception as error:
            print(f"[{sensor_id}] ПОМИЛКА: {error}")


class RealDHT22:
    def read_temperature(self) -> float:
        return 22.5

    def get_sensor_id(self) -> str:
        return "DHT22-001"


# Створення датчиків
sensors = [
    WeatherAPISensor(),
    SimulatedSensor(base=21.5, deviation=3.0),
    FakeAlways25(),
    BrokenSensor()
]

# Моніторинг температури
monitor_room(sensors)


# Перевірка сумісності з протоколом
print()
print(isinstance(RealDHT22(), TemperatureSensor))  # True
print(isinstance({"temp": 22}, TemperatureSensor))  # False

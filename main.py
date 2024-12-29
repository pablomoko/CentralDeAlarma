from alarm.alarm_system import AlarmSystem
from alarm.sensor import Sensor
from alarm.siren import Siren
import config.settings as settings


def main():
    alarm = AlarmSystem(
        mqtt_broker=settings.MQTT_BROKER,
        mqtt_port=settings.MQTT_PORT,
        module_name=settings.MODULE_NAME,
    )

    # Agregar sensores
    sensor1 = Sensor(name="Puerta", topic="sensors/Sensor_1/data", trigger_value=1)
    sensor2 = Sensor(name="Ventana", topic="sensors/Sensor_2/data", trigger_value=1)
    alarm.add_sensor(sensor1)
    alarm.add_sensor(sensor2)

    # Agregar sirenas
    siren1 = Siren(name="SirenaPrincipal", topic="sirens/SirenaPrincipal/data",
                   mqtt_client=alarm.client)
    alarm.add_siren(siren1)

    # Iniciar el sistema de alarma
    alarm.start()


if __name__ == "__main__":
    main()
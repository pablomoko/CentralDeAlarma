import paho.mqtt.client as mqtt
from alarm.sensor import Sensor
import json

class Siren:
    def __init__(self, name,  topic,state_topic="sirens/state",activation_message="ON", deactivation_message="OFF", mqtt_client=None):
        self.name = name
        self.topic = topic
        self.activation_message = activation_message
        self.deactivation_message = deactivation_message
        self.client = mqtt_client

    def activate(self):
        if self.client:
            print(f"Activando sirena: {self.name}")
            self.is_active = True
            state_message = json.dumps({"state": "active"})
            self.client.publish("sirens/state", state_message)

        else:
            print(f"Cliente MQTT no disponible para {self.name}.")

    def deactivate(self):
        if self.client:
            print(f"Desactivando sirena: {self.name}")
            self.is_active = False
            state_message = json.dumps({"state": "inactive"})
            self.client.publish("sirens/state", state_message)
        else:
            print(f"Cliente MQTT no disponible para {self.name}.")
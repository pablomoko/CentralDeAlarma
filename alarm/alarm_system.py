import paho.mqtt.client as mqtt
import json
import re

class AlarmSystem:
    def __init__(self, mqtt_broker, mqtt_port, module_name):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.module_name = module_name
        self.sensors = []
        self.sirens = []
        self.client = mqtt.Client()
        self.message_handlers = {}

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def add_siren(self, siren):
        self.sirens.append(siren)

    def register_message_handler(self, topic, handler):
        """Registrar manejador de mensaje para un tópico específico"""
        self.message_handlers[topic] = handler

    def match_topic(self, topic, pattern):
        """Compara el tópico con el patrón (que puede tener el comodín +)"""
        # Escapamos el patrón para usarlo en una expresión regular
        pattern = pattern.replace("+", "[^/]+")  # El comodín + se reemplaza por cualquier cosa excepto '/'
        # Comprobamos si el tópico coincide con el patrón usando expresiones regulares
        return re.fullmatch(pattern, topic) is not None

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Mensaje recibido: {topic} -> {payload}")

        # Intentamos encontrar un manejador para el tópico
        for registered_topic in self.message_handlers:
            if self.match_topic(topic, registered_topic):  # Usamos match_topic con patrón
                handler = self.message_handlers[registered_topic]
                handler(payload)
                return

        print(f"No hay manejador registrado para el tópico {topic}")

    def handle_sensor_message(self, payload):
        """Manejo del mensaje de sensor activado"""
        try:
            data = json.loads(payload)
            sensor_name = data.get("sensor")
            state = data.get("state")
        except json.JSONDecodeError:
            print("El mensaje recibido no es un JSON válido.")
            return

        # Comprobamos si alguno de los sensores coincide con el nombre y estado
        for sensor in self.sensors:
            if sensor.name == sensor_name and sensor.is_triggered(state):
                print(f"¡Sensor activado! {sensor.name}")
                self.activate_sirens()

    def handle_siren_control(self, payload):
        """Manejo de mensajes de control de sirenas (activación/desactivación)"""
        try:
            data = json.loads(payload)
            action = data.get("action")  # Puede ser 'activate' o 'deactivate'
        except json.JSONDecodeError:
            print("El mensaje recibido no es un JSON válido.")
            return

        if action == "activate":
            self.activate_sirens()
        elif action == "deactivate":
            self.deactivate_sirens()
        else:
            print(f"Acción desconocida: {action}")

    def activate_sirens(self):
        for siren in self.sirens:
            siren.activate()

    def deactivate_sirens(self):
        for siren in self.sirens:
            siren.deactivate()

    def start(self):
        # Registramos los manejadores
        self.register_message_handler("sensors/+/data", self.handle_sensor_message)
        self.register_message_handler("sirens/control", self.handle_siren_control)

        self.client.on_message = self.on_message
        self.client.connect(self.mqtt_broker, self.mqtt_port)

        # Suscribimos a los sensores y al control de sirenas
        for sensor in self.sensors:
            self.client.subscribe(sensor.topic)
        self.client.subscribe("sirens/control")

        print("Sistema de alarma iniciado...")
        self.client.loop_forever()

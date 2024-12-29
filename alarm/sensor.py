class Sensor:
    def __init__(self, name, topic, trigger_value):
        self.name = name
        self.topic = topic
        self.trigger_value = trigger_value

    def matches_topic(self, topic):
        return self.topic == topic

    def is_triggered(self, payload):
        return payload == self.trigger_value

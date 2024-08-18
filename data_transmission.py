import json
import paho.mqtt.client as mqtt
import ssl
import numpy as np
import time
from datetime import datetime
import random

class MQTTClient:
    def __init__(self, broker="", port=8883, topic="", username="", password=""):
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.tls_set(cert_reqs=ssl.CERT_NONE)  
        self.client.tls_insecure_set(True)  
        self.client.connect(broker, port, 60)
        self.topic = topic

    def publish_sensor_data(self, data):
        self.client.publish(self.topic, json.dumps(data))
        print(f"Published: {data}")

    def start_listening(self, influxdb_manager):
        def on_message(client, userdata, message):
            influxdb_manager.write_data(json.loads(message.payload))
            print(f"Received and written to InfluxDB: {json.loads(message.payload)}")

        self.client.on_message = on_message
        self.client.subscribe(self.topic)
        self.client.loop_forever()

class SensorSimulator:
    def generate_sensor_data(self):
        asset_name = random.choice(["pump 1", "pump 2", "pump 3"])
        current_time = time.time()
        timestamp_ms = int(round(current_time * 1000))  # Convert seconds to milliseconds
        data = {
            "asset": asset_name,
            "timestamp": timestamp_ms,  
            "vibration": np.random.normal(0, 1),
            "pressure": np.random.normal(100, 10),
            "temperature": np.random.normal(50, 5),
            "flow": np.random.normal(20, 2)
        }
        return data

    def start_simulation(self, mqtt_client):
        while True:
            sensor_data = self.generate_sensor_data()
            mqtt_client.publish_sensor_data(sensor_data)
            print(f"Published: {sensor_data}")
            time.sleep(5)

if __name__ == "__main__":
    mqtt_client = MQTTClient(password="")
    sensor_simulator = SensorSimulator()
    sensor_simulator.start_simulation(mqtt_client)
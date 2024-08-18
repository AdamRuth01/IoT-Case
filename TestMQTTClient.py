import unittest
from unittest.mock import MagicMock, patch
import json
import paho.mqtt.client as mqtt
import ssl
import numpy as np
import time
from datetime import datetime
import random

# Assuming the provided code is in a module named 'iot_module'
from data_transmission import MQTTClient, SensorSimulator

class TestMQTTClient(unittest.TestCase):
    @patch('iot_module.mqtt.Client')
    def test_publish_sensor_data(self, MockClient):
        mock_client_instance = MockClient.return_value
        mqtt_client = MQTTClient(password="test_password")

        data = {"asset": "pump 1", "timestamp": 123456789, "vibration": 0.5, "pressure": 101.5, "temperature": 50.5, "flow": 21.5}
        mqtt_client.publish_sensor_data(data)

        mock_client_instance.publish.assert_called_with("", json.dumps(data))
        print("Tested publish_sensor_data")

    @patch('iot_module.mqtt.Client')
    def test_start_listening(self, MockClient):
        mock_client_instance = MockClient.return_value
        mqtt_client = MQTTClient(password="test_password")
        influxdb_manager = MagicMock()

        mqtt_client.start_listening(influxdb_manager)

        mock_client_instance.subscribe.assert_called_with("")
        mock_client_instance.loop_forever.assert_called()
        print("Tested start_listening")

class TestSensorSimulator(unittest.TestCase):
    @patch('iot_module.MQTTClient')
    def test_generate_sensor_data(self, MockMQTTClient):
        sensor_simulator = SensorSimulator()

        data = sensor_simulator.generate_sensor_data()
        self.assertIn("asset", data)
        self.assertIn("timestamp", data)
        self.assertIn("vibration", data)
        self.assertIn("pressure", data)
        self.assertIn("temperature", data)
        self.assertIn("flow", data)
        print("Tested generate_sensor_data")

    @patch('iot_module.MQTTClient')
    def test_start_simulation(self, MockMQTTClient):
        mock_mqtt_client = MockMQTTClient.return_value
        sensor_simulator = SensorSimulator()

        with patch('iot_module.time.sleep', return_value=None):  # Avoid waiting during the test
            with patch.object(sensor_simulator, 'generate_sensor_data', return_value={"asset": "pump 1", "timestamp": 123456789, "vibration": 0.5, "pressure": 101.5, "temperature": 50.5, "flow": 21.5}):
                sensor_simulator.start_simulation(mock_mqtt_client)

                mock_mqtt_client.publish_sensor_data.assert_called()
                print("Tested start_simulation")

if __name__ == "__main__":
    unittest.main()

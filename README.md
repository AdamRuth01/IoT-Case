# IoT Use Case for a Centrifugal Pump

## Table of Contents
- [Objective](#objective)
- [Components](#components)
- [Implementation Steps](#implementation-steps)
    - [Sensor Deployment](#sensor-deployment)
    - [Data Transmission](#data-transmission)
    - [Data Storage and Processing](#data-storage-and-processing)
    - [Real-Time Monitoring](#real-time-monitoring)
    - [Alerts and Notifications](#alerts-and-notifications)
    - [Predictive Maintenance](#predictive-maintenance)
    - [Remote Access](#remote-access)
    - [Reporting and Analysis](#reporting-and-analysis)
- [Benefits](#benefits)
- [Example Scenario](#example-scenario)
- [Code](#code)
    - [MQTT Client and Sensor Simulator](#data-transmission-mqttclient-client-and-sensor-simulator)
    - [Kafka Integration](#kafka-integration)
    - [predictive.maintence](#predictive-pre-model)
    - [Testing](#testing)

## Objective
To enhance the operational efficiency and maintenance of centrifugal pumps by leveraging IoT technologies for real-time monitoring, predictive maintenance, and data-driven decision-making.

## Components
1. **Centrifugal Pump**: The primary equipment.
2. **Sensors**:
    - Vibration sensors
    - Pressure sensors
    - Temperature sensors
    - Flow sensors
3. **IoT Gateway**: To aggregate data from sensors and transmit it to the cloud.
4. **Cloud Platform**: For data storage, processing, and analytics (IXCB MQTT, Influx DB, Databrick, Snowflake).
5. **Dashboard and Analytics Tool**: For real-time monitoring and visualization (e.g., Grafana).
6. **Mobile App**: For remote alerts and monitoring. (Optional)

## Implementation Steps

### Sensor Deployment
- Install vibration, pressure, temperature, and flow sensors on the centrifugal pump. *(Simulate the Data)*
- Ensure sensors are calibrated and connected to the MQTT Broker.

### Data Transmission
- Configure the MQTT Client to collect data from the sensors.
- Set up the MQTT Rule Engine to transmit data to the cloud platform securely.

### Data Storage and Processing
- Store incoming data in an Influx DB.
- Implement data processing algorithms to filter and analyze the data in real-time.

### Real-Time Monitoring
- Develop a dashboard using tools like Grafana to display real-time data.
- Include visualizations for key parameters such as vibration levels, pressure, temperature, and flow rates.

### Alerts and Notifications
- Set thresholds for critical parameters.
- Configure the system to send alerts via email or mobile app notifications if thresholds are breached.

### Predictive Maintenance
- Use historical data and machine learning algorithms to predict potential failures.
- Schedule maintenance activities based on predictive analytics to prevent downtime.

### Remote Access
- Provide access to the dashboard and alerts via a mobile app.
- Enable remote control capabilities for authorized personnel to make adjustments as needed.

### Reporting and Analysis
- Generate periodic reports on pump performance and maintenance activities.
- Analyze data to identify trends and areas for improvement.

## Benefits
1. **Increased Uptime**: Predictive maintenance reduces unexpected failures and downtime.
2. **Cost Savings**: Preventive actions based on data insights minimize repair costs and extend pump life.
3. **Improved Efficiency**: Real-time monitoring ensures the pump operates within optimal parameters, enhancing efficiency.
4. **Enhanced Safety**: Early detection of anomalies helps prevent hazardous situations.
5. **Data-Driven Decisions**: Access to comprehensive data enables informed decision-making for maintenance and operations.

## Example Scenario
A manufacturing plant uses centrifugal pumps for water circulation. The pumps are equipped with IoT sensors that monitor vibration, pressure, temperature, and flow. Data is sent to the cloud and visualized on a Grafana dashboard. Maintenance teams receive alerts on their mobile devices if any parameter exceeds predefined thresholds. Predictive analytics identify a potential bearing failure, prompting a scheduled maintenance intervention, preventing an unexpected pump breakdown.

By implementing this IoT use case, the manufacturing plant ensures optimal performance and longevity of their centrifugal pumps, resulting in improved operational efficiency and reduced maintenance costs.

## Code

### data transmission mqttclient client and sensor simulator
_MQTT Client and Sensor Simulator_
_**Description of the Code**_
Libraries and Modules
json: Standard library module to work with JSON data.
paho.mqtt.client as mqtt: MQTT client library for Python.
ssl: Provides access to TLS/SSL wrapper for securing network connections.
numpy as np: Library for numerical operations in Python, used here for generating random numbers.
time: Module for time-related functions.
datetime: Module for handling date and time.
random: Module for generating random numbers.
Classes and Functions
MQTTClient Class

init Method: Initializes the MQTT client.
Connects to an MQTT broker using the provided credentials and settings.
Sets up TLS with insecure settings for simplicity (not recommended for production).
publish_sensor_data Method: Publishes JSON-encoded sensor data to a specified MQTT topic.
start_listening Method: Listens to messages on the subscribed MQTT topic and writes the received data to InfluxDB via an InfluxDB manager.
Defines an on_message callback function that processes incoming messages and prints the received data.
SensorSimulator Class

generate_sensor_data Method: Simulates sensor data.
Generates random data for different parameters such as vibration, pressure, temperature, and flow for a randomly chosen asset.
start_simulation Method: Continuously generates and publishes sensor data at 5-second intervals.
Main Execution
if name == "main":
Initializes an MQTTClient instance with the given password.
Initializes a SensorSimulator instance.
Starts the simulation, which repeatedly generates and publishes sensor data.
Summary
The code sets up an MQTT client that connects to a broker, publishes simulated sensor data, and can listen for incoming messages on a specific topic. The sensor data is generated randomly to simulate real-world conditions and published to the MQTT broker every 5 seconds.


### _kafka-integration_
_**Description of the Code**_
Libraries and Modules
functools: Standard library module for higher-order functions, used here to partially apply functions.
confluent_kafka.Consumer: Kafka consumer library for reading messages from Kafka topics.
logging: Standard library module for logging messages.
time: Standard library module for time-related functions.
random.choice and random.randint: Functions from the random module to generate random choices and integers.
requests: Library for making HTTP requests.
Functions and Their Descriptions
read_from_kafka Function

Purpose: Reads messages from a Kafka topic.
Logging Setup: Configures a logger to log messages to the console.
CA Certificate: Reads a CA certificate from a file (scania-root.pem). If the file is missing or empty, it prints an error message and exits.
Kafka Consumer Configuration: Sets up the Kafka consumer configuration with parameters such as bootstrap servers, security protocol, SASL mechanisms, CA certificate, OAuth token callback, and group ID.
Consumer Initialization: Creates a Kafka consumer instance with the provided configuration and logger.
Subscription: Subscribes the consumer to a specified Kafka topic.
Message Polling: Continuously polls for new messages from Kafka and prints the consumed messages. Handles errors and waits if no messages are available.
Graceful Shutdown: Ensures the consumer closes properly on script termination.
_get_token Function

Purpose: Retrieves an OAuth token for authentication.
Token Request: Sends a POST request to an OAuth token endpoint using client credentials.
Response Handling: Parses the response to extract the access token and its expiration time.
delivery_report Function

Purpose: Callback function to report the success or failure of message delivery.
Error Handling: Prints an error message if delivery fails.
Success Handling: Prints a success message with details about the delivered message.
delivery_callback Function

Purpose: Optional callback function for per-message delivery reports.
Error Handling: Prints an error message if delivery fails.
Success Handling: Prints a success message with details about the delivered message.
Main Execution
if name == "main":
Calls the read_from_kafka function to start reading messages from Kafka.
Summary
The code sets up a Kafka consumer to read messages from a specified Kafka topic. It configures the consumer with necessary security settings, including an OAuth token retrieval function. The consumer continuously polls for new messages and prints them, handling errors and waiting when no messages are available. The script ensures proper shutdown and provides optional delivery report callbacks for message production.

### _predictive-pre-model_
_**Description of the Code**_
Libraries and Modules
sklearn.linear_model (LinearRegression): A module from the scikit-learn library used to create and train linear regression models.
numpy (np): A library for numerical operations in Python, used here for generating random numbers.
pandas (pd): A library for data manipulation and analysis.
time: Standard library module for time-related functions.
Classes and Functions
PredictiveMaintenance Class
init Method: Initializes the predictive maintenance system.

Sample Data Creation: Generates a DataFrame with 100 days of historical data, including time, vibration, pressure, temperature, and flow measurements.
Feature Engineering and Model Training:
Features: Extracts the sensor data features (vibration, pressure, temperature, flow).
Target: Creates a binary target variable (0 for no failure, 1 for failure) randomly.
Model Training: Initializes a linear regression model and fits it to the features and target.
predict_maintenance Method: Predicts whether maintenance is required based on the provided sensor data.

Data Preparation: Converts the sensor data dictionary to a DataFrame.
Prediction: Uses the trained model to predict maintenance needs.
Output: Prints whether maintenance is required based on the prediction.
start_monitoring Method: Monitors real-time sensor data and predicts maintenance needs.

Query API: Uses the InfluxDB manager's query API to fetch recent data.
Query Definition: Defines a query to fetch data from the last 5 minutes from the specified InfluxDB bucket.
Continuous Monitoring: Continuously queries the data every 5 minutes, processes the results, and predicts maintenance needs.
Data Processing: Extracts sensor data from the query results and calls predict_maintenance with the extracted data.
Main Execution
start_monitoring Method: Continuously monitors and predicts maintenance needs based on real-time sensor data fetched from InfluxDB.
Summary
The code implements a predictive maintenance system using a linear regression model. It includes the following components:

Initialization and Training:

Creates a sample dataset with historical sensor data.
Extracts features and trains a linear regression model to predict maintenance needs.
Real-Time Monitoring:

Monitors real-time sensor data from InfluxDB.
Predicts maintenance needs based on the real-time data and the trained model.
Prediction:

Converts sensor data to a suitable format.
Uses the trained model to predict if maintenance is required.
Outputs the prediction result.
BDD and TDD Parallel
BDD (Behavior-Driven Development): The code can be enhanced by writing scenarios and examples describing the behavior of the predictive maintenance system. Tests would then ensure the system behaves as described in these scenarios.
TDD (Test-Driven Development): Tests can be written before implementing methods like predict_maintenance and start_monitoring. These tests would define the expected functionality, guiding the implementation to meet these predefined tests.
Parallel to Mockito in Java: In Java, Mockito is used to create mock objects for unit testing. The Python unittest.mock module provides similar functionality. For instance, in a test suite for this code, we could mock the InfluxDB manager and its query API to test the start_monitoring method without needing a real database connection. This approach ensures isolated and focused tests, similar to how Mockito is used in Java.

### _Testing_
_**Description of the Code**_
Libraries and Modules
unittest: Standard library module for writing and running tests.
unittest.mock (MagicMock, patch): Utilities from the unittest library for creating mock objects and patching.
json: Standard library module to work with JSON data.
paho.mqtt.client as mqtt: MQTT client library for Python.
ssl: Provides access to TLS/SSL wrapper for securing network connections.
numpy as np: Library for numerical operations in Python, used here for generating random numbers.
time: Module for time-related functions.
datetime: Module for handling date and time.
random: Module for generating random numbers.
Classes and Functions for Testing
TestMQTTClient Class

test_publish_sensor_data Method: Tests the publish_sensor_data method of the MQTTClient class.

Patch: Uses @patch to mock the mqtt.Client class.
Mock Client: Creates an instance of the mocked MQTT client.
MQTT Client Initialization: Initializes an MQTTClient instance with a test password.
Test Data: Defines a sample data dictionary to be published.
Assertion: Checks if the publish method of the mocked client is called with the correct topic and JSON-encoded data.
Prints: Outputs a confirmation message for the test.
test_start_listening Method: Tests the start_listening method of the MQTTClient class.

Patch: Uses @patch to mock the mqtt.Client class.
Mock Client: Creates an instance of the mocked MQTT client.
MQTT Client Initialization: Initializes an MQTTClient instance with a test password.
Mock InfluxDB Manager: Creates a mock object for the InfluxDB manager.
Listening Start: Calls the start_listening method with the mocked InfluxDB manager.
Assertions: Checks if the subscribe and loop_forever methods of the mocked client are called.
Prints: Outputs a confirmation message for the test.
TestSensorSimulator Class

test_generate_sensor_data Method: Tests the generate_sensor_data method of the SensorSimulator class.

Patch: Uses @patch to mock the MQTTClient class (although it's not used directly in this test).
Sensor Simulator Initialization: Creates an instance of the SensorSimulator class.
Generated Data: Calls the generate_sensor_data method to get sample data.
Assertions: Checks if the generated data contains the expected keys.
Prints: Outputs a confirmation message for the test.
test_start_simulation Method: Tests the start_simulation method of the SensorSimulator class.

Patch: Uses @patch to mock the MQTTClient class.
Mock MQTT Client: Creates an instance of the mocked MQTT client.
Sensor Simulator Initialization: Creates an instance of the SensorSimulator class.
Patches:
time.sleep: Patches the time.sleep function to avoid actual waiting during the test.
generate_sensor_data: Patches the generate_sensor_data method to return predefined data.
Simulation Start: Calls the start_simulation method with the mocked MQTT client.
Assertion: Checks if the publish_sensor_data method of the mocked MQTT client is called.
Prints: Outputs a confirmation message for the test.
Main Execution
if name == "main":
Executes the test cases defined in the script using unittest.main().
Summary
The code is a test suite for the MQTTClient and SensorSimulator classes using the unittest framework. It leverages mocking techniques to isolate and test individual components and their interactions. The tests ensure that methods like publish_sensor_data, start_listening, generate_sensor_data, and start_simulation work as expected, verifying their behavior through assertions and mock object interactions.

BDD and TDD Parallel
BDD (Behavior-Driven Development): This testing code focuses on the behavior of the MQTTClient and SensorSimulator classes, ensuring they meet the expected behaviors like publishing data, subscribing to topics, generating sensor data, and starting simulations.
TDD (Test-Driven Development): The unit tests can be written before the actual implementation of the methods to define the desired functionality, guiding the development process to meet these predefined tests.
Parallel to Mockito in Java: In Java, Mockito is commonly used for similar purposes—creating mock objects and verifying interactions within tests. The Python unittest.mock module serves the same purpose, providing tools to mock objects, patch methods, and assert method calls and behaviors.








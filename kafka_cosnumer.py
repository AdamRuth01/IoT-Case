import functools
from confluent_kafka import Consumer
import logging, time
from random import choice, randint
import requests


def read_from_kafka():

    mylogger = logging.getLogger()
    mylogger.setLevel(logging.DEBUG)
    mylogger.addHandler(logging.StreamHandler())

    with open('scania-root.pem', 'r') as file:
        ca_pem_string = file.read()

    if not ca_pem_string:
        print('scania-root.pem not found')
        return
    
    config = {
        'bootstrap.servers': 'oauthaws.iris-streaming.devtest.aws.scania.com:9093',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'OAUTHBEARER',
        'ssl.ca.pem': ca_pem_string,
        'oauth_cb': functools.partial(_get_token),
        'auto.offset.reset': 'earliest',
        "group.id": 'pii-New',
    }

    # Create Consumer instance
    consumer = Consumer(config, logger=mylogger)

    # Subscribe to topic
    topic = "Put your topic here"
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print(f'ERROR: {str(msg.error())}')
            else:
                # Extract the (optional) key and value, and print.

                print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()


def _get_token(config):
    # """Note here value of config comes from sasl.oauthbearer.config below.
    
    # _remove_proxy()
    token_url = 'https://fg.ciam.preprod.aws.scania.com/auth/realms/scania/protocol/openid-connect/token'
    client_id = 'Put your client id here'
    client_secret = 'Put your client secret here'

    payload = {
        'grant_type': 'client_credentials'
    }
    resp = requests.post(token_url,
                         auth=(client_id, client_secret),
                         data=payload)
    token = resp.json()
    # _add_proxy()

    return token['access_token'], time.time() + float(token['expires_in'])


def delivery_report(err, msg):
    """
    Reports the failure or success of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.
    """
    if err is not None:
        print('Delivery failed for User record {}: {}'.format(msg.key(), err))
        return
    print('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))


# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


if __name__ == '__main__':
    read_from_kafka()
from medrical.producer.patient import Patient
from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro
from configparser import SafeConfigParser
import json
import sys


delivered_status = False


def produce(topic_name, patient):
    ''' Produces patient's biometrics measured every second
        on a kafka topic

        Args:
            topic (str): The name of the topic (default: 'biometrics_default')
            patient (Patient): An Patient object
    '''
    parser = SafeConfigParser()
    config_file_path = 'medrical/config/pipeline.cfg'
    parser.read(config_file_path)
    global delivered_status
    KAFKA_HOST = parser.get('KAFKA', 'kafka_host')
    KAFKA_PORT = parser.get('KAFKA', 'kafka_port')
    SCHEMA_USER = parser.get('KAFKA', 'kafka_schema_registry_user')
    SCHEMA_PASSWORD = parser.get('KAFKA', 'kafka_schema_registry_password')
    SCHEMA_PORT = parser.get('KAFKA', 'kafka_schema_registry_port')

    VALUE_SCHEMA = open(
        'medrical/config/schemas/biometrics.avsc').read().replace('schema_name', topic_name)
    KEY_SCHEMA = open(
        'medrical/config/schemas/key.avsc').read().replace('schema_name', topic_name)

    avroProducer = AvroProducer({
        'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
        "security.protocol": "ssl",
        'ssl.ca.location': 'medrical/config/ssl/ca.pem',
        'ssl.certificate.location': 'medrical/config/ssl/service.cert',
        'ssl.key.location': 'medrical/config/ssl/service.key',
        'schema.registry.url': f'https://{SCHEMA_USER}:{SCHEMA_PASSWORD}@{KAFKA_HOST}:{SCHEMA_PORT}'
    }, default_key_schema=avro.loads(KEY_SCHEMA), default_value_schema=avro.loads(VALUE_SCHEMA))

    patient_biometrics = patient.get_biometrics()
    patient_id = patient.get_id()
    avroProducer.produce(topic=topic_name,
                            value=patient_biometrics, key=patient_id, callback=error_callback)
    avroProducer.flush()

    print(f'Published {patient_biometrics} to the topic "{topic_name}"')

    return delivered_status


def error_callback(err, msg):
    global delivered_status
    if err:
        delivered_status = False
    else:
        delivered_status = True

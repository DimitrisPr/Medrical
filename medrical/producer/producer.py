from medrical.producer.patient import Patient
from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro
from configparser import SafeConfigParser
import pathlib
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
    
    global delivered_status
    parser = SafeConfigParser()
    CONFIG_PATH = str(pathlib.Path(
        __file__).parent.parent.absolute()) + '/config/pipeline.cfg'
    parser.read(CONFIG_PATH)
    KAFKA_HOST = parser.get('KAFKA', 'kafka_host')
    KAFKA_PORT = parser.get('KAFKA', 'kafka_port')
    SCHEMA_USER = parser.get('KAFKA', 'kafka_schema_registry_user')
    SCHEMA_PASSWORD = parser.get('KAFKA', 'kafka_schema_registry_password')
    SCHEMA_PORT = parser.get('KAFKA', 'kafka_schema_registry_port')
    AVRO_PATH = str(pathlib.Path(
        __file__).parent.parent.absolute()) + '/config/schemas'
    VALUE_SCHEMA = open(
        AVRO_PATH+'/biometrics.avsc').read().replace('schema_name', topic_name)
    KEY_SCHEMA = open(
        AVRO_PATH+'/key.avsc').read().replace('schema_name', topic_name)
    SSL_PATH = str(pathlib.Path(
        __file__).parent.parent.absolute()) + '/config/ssl'

    patient_biometrics = patient.get_biometrics()
    patient_id = patient.get_id()

    avroProducer = AvroProducer({
        'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
        "security.protocol": "ssl",
        'ssl.ca.location': f'{SSL_PATH}/ca.pem',
        'ssl.certificate.location': f'{SSL_PATH}/service.cert',
        'ssl.key.location': f'{SSL_PATH}/service.key',
        'schema.registry.url': f'https://{SCHEMA_USER}:{SCHEMA_PASSWORD}@{KAFKA_HOST}:{SCHEMA_PORT}'
    }, default_key_schema=avro.loads(KEY_SCHEMA), default_value_schema=avro.loads(VALUE_SCHEMA))
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

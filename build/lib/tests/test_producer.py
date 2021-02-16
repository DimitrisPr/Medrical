from medrical.producer.producer import produce
from medrical.producer.patient import Patient
from confluent_kafka import avro
from configparser import SafeConfigParser
import unittest
import psycopg2


class TestProducer(unittest.TestCase):
    ''' Test for JDBC Kafka Connector '''
    parser = SafeConfigParser()
    config_file_path = 'medrical/config/pipeline.cfg'
    parser.read(config_file_path)

    POSTGRES_HOST = parser.get('POSTGRES', 'postgres_host')
    POSTGRES_PORT = parser.get('POSTGRES', 'postgres_port')
    POSTGRES_USER = parser.get('POSTGRES', 'postgres_user')
    POSTGRES_PASSWORD = parser.get('POSTGRES', 'postgres_password')

    conn = psycopg2.connect(
        f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/defaultdb?sslmode=require")
    cursor = conn.cursor()
    cursor = conn.cursor()

    def test_topic_delivery(self, topic_name='biometrics_default'):
        ''' Tests if the topic is delivered succesfully to Kafka.

            Args:
                topic_name (str): The name of the topic (default: 'biometrics_test')
            '''
        delivery_status = produce(topic_name, Patient())

        self.assertEqual(delivery_status, True)


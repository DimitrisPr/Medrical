from medrical.producer.producer import produce
from medrical.producer.patient import Patient
from configparser import SafeConfigParser
from confluent_kafka import avro
import unittest
import psycopg2
import pathlib




class TestConnector(unittest.TestCase):
    ''' Test for JDBC POSTGRES Connector '''
    parser = SafeConfigParser()
    config_file = str(pathlib.Path(__file__).parent.parent.absolute()) +'/medrical/config/pipeline.cfg'
    parser.read(config_file)

    POSTGRES_HOST = parser.get('POSTGRES', 'postgres_host')
    POSTGRES_PORT = parser.get('POSTGRES', 'postgres_port')
    POSTGRES_USER = parser.get('POSTGRES', 'postgres_user')
    POSTGRES_PASSWORD = parser.get('POSTGRES', 'postgres_password')

    conn = psycopg2.connect(
        f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/defaultdb?sslmode=require")
    cursor = conn.cursor()

    def test_table_auto_create(self, topic_name='biometrics_test'):
        ''' Tests whether a postgreSQL table is auto-created when the producer publishes a new topic.
            Topic name must match the regex: biometrics_(.*)

            Note: New tables may take some time to be created by the JDBC connector to postgres, 
            therefore this test may fail on newly created tables.

            Args:
                topic_name (str): The name of the topic (default: 'biometrics_test')
            '''
        produce(topic_name, Patient())
        self.cursor.execute(
            f"SELECT EXISTS (SELECT 1 AS result FROM pg_tables WHERE schemaname = 'public' AND tablename = '{topic_name}');")
        table_created = self.cursor.fetchone()[0]

        self.assertEqual(table_created, True)


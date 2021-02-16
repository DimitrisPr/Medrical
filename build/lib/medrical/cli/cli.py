from tests.test_connector import TestConnector
from tests.test_producer import TestProducer
from medrical.producer.producer import produce
from medrical.producer.patient import Patient
from medrical.config.config import configure

from configparser import SafeConfigParser
import unittest
import time
import sys


USAGE_STRING = """\nUsage:                               
            medrical <command>\n               
            Commands:                                   
                produce: \t Launches a Kafka producer   
                test <unit>: \t Launches medrical tests
                configure: \t Configures medrical (Kafka, PostgreSQL) 

            Units:
                producer:\t Tests Kafka producer 
                connector:\t Tests JDBC connector \n

            Examples:

            - medrical produce
            - medrical test producer
            - medrical test connector    
                """


def medrical():
    
    parser = SafeConfigParser()
    config_file_path = 'medrical/config/pipeline.cfg'
    parser.read(config_file_path)

    if parser.get('PIPELINE', 'is_configured') == 'False':
        configure()

    f''' Medrical cli tool
        {USAGE_STRING}
    '''
    args = sys.argv
    sys.argv = [sys.argv[0]]  # Clear args, not to be passed in tests

    if len(args[1:]) < 1:
        print(USAGE_STRING)
    elif args[1] == 'produce':
        try:
            while(True):
                produce('biometrics_default', Patient())
                time.sleep(1)  # Unreliable, but works for the example's sake
        except KeyboardInterrupt:
            sys.exit(0)
    elif args[1] == 'test':
        if args[2] == 'producer':
            suite = unittest.TestLoader().loadTestsFromTestCase(TestProducer)
            unittest.TextTestRunner(verbosity=2).run(suite)
        elif args[2] == 'connector':
            suite = unittest.TestLoader().loadTestsFromTestCase(TestConnector)
            unittest.TextTestRunner(verbosity=2).run(suite)
        else:
            print(f'Error: Unit does not exist\n{USAGE_STRING}')
    elif args[1] == 'configure':
        configure()
    else:
        print(USAGE_STRING)

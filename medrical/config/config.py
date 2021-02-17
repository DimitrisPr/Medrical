from configparser import SafeConfigParser 
import pathlib
import os

def configure():

    parser = SafeConfigParser()
    config_file = str(pathlib.Path(__file__).parent.absolute()) +'/pipeline.cfg'
    parser.read(config_file)

    def verify_configuration(answer=''):

        print(f''' \n
            Please double check the configuration!
            \tkafka_host: {parser.get('KAFKA', 'kafka_host')} 
            \tkafka_schema_registry_user: {parser.get('KAFKA', 'kafka_schema_registry_user')} 
            \tkafka_port: {parser.get('KAFKA', 'kafka_port')} 
            \tkafka_schema_registry_password: {parser.get('KAFKA', 'kafka_schema_registry_password')} 
            \tkafka_schema_registry_port: {parser.get('KAFKA', 'kafka_schema_registry_port')} 
            \tpostgres_host: {parser.get('POSTGRES', 'postgres_host')} 
            \tpostgres_user: {parser.get('POSTGRES', 'postgres_user')} 
            \tpostgres_password: {parser.get('POSTGRES', 'postgres_password')} 
            \tpostgres_port: {parser.get('POSTGRES', 'postgres_port')} 
            \n''')

        while answer.upper() != 'N' and answer.upper() != 'Y':
            answer = input('Would you like to change some field? (Y/N): ')

        if answer.upper() == 'Y' or answer.upper() == 'YES':
            field = input(
                'Please enter the name of the field (e.g kafka_password): ')
            value = input('Please enter the value of the field (e.g mypass): ')

            print(field)
            if 'kafka' in field:
                parser.set('KAFKA', f'{field}', value)
            else:
                parser.set('POSTGRES', f'{field}', value)

            verify_configuration()
        else:
            with open(config_file, 'w') as config:
                parser.write(config)

            print('\nKafka & PostgreSQL Setup successful!')

    print('\n--- SETUP MEDRICAL (medrical/config/pipeline.cfg) ---\n')

    kafka_host = input("Kafka host: ")
    kafka_port = input("Kafka port: ")
    kafka_schema_registry_user = input("Kafka schema registry user: ")
    kafka_schema_registry_password = input("Kafka schema registry password: ")
    kafka_schema_registry_port = input("Kafka schema registry port: ")
    postgres_host = input("postgres host: ")
    postgres_user = input("postgres user: ")
    postgres_password = input("postgres password: ")
    postgres_port = input("postgres port: ")

    parser.set('KAFKA', 'kafka_host', kafka_host)
    parser.set('KAFKA', 'kafka_port', kafka_port)
    parser.set('KAFKA', 'kafka_schema_registry_user', kafka_schema_registry_user)
    parser.set('KAFKA', 'kafka_schema_registry_password', kafka_schema_registry_password)
    parser.set('KAFKA', 'kafka_schema_registry_port', kafka_schema_registry_port)
    parser.set('POSTGRES', 'postgres_host', postgres_host)
    parser.set('POSTGRES', 'postgres_user', postgres_user)
    parser.set('POSTGRES', 'postgres_password', postgres_password)
    parser.set('POSTGRES', 'postgres_port', postgres_port)
    
    parser.set('PIPELINE', 'is_configured', 'True')

    with open(config_file, 'w') as config:
        parser.write(config)

    verify_configuration()
    ssl_configure()

def ssl_configure():

    print('\n--- CONFIGURE SSL ---\n\n')
    SSL_DIR = str(pathlib.Path(__file__).parent.parent.absolute()) +'/config/ssl'
    print(f'You can either place the files manually to the path {SSL_DIR}')
    print(f'or try by using this interfcae (unstable)\n ')

    answer = input('Would you like to open the SSL directory? (Y/N): ')
    if answer.upper() == 'Y' or answer.upper() == 'YES':
        user_os = input('What is your OS? (mac, win, linux): ')
        if user_os.upper() == 'MAC':
            os.system(f'open {SSL_DIR}')
        elif user_os.upper() == 'WIN':
            os.system(f'start {SSL_DIR}')
        elif user_os.upper() == 'LINUX':
            os.system(f'nautilus {SSL_DIR}')
    print(f'\nIf this has failed, please add the SSL files manually to {SSL_DIR}.')
    print('Run medrical -help for help')
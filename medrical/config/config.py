from configparser import SafeConfigParser 

def configure():

    parser = SafeConfigParser()
    config_file_path = 'medrical/config/pipeline.cfg'
    parser.read(config_file_path)

    def verify_configuration(answer=''):

        print(f''' \n
            Please double check the configuration!
                kafka_host: {parser.get('KAFKA', 'kafka_host')} 
                kafka_port: {parser.get('KAFKA', 'kafka_port')} 
                kafka_schema_registry_user: {parser.get('KAFKA', 'kafka_schema_registry_user')} 
                kafka_schema_registry_password: {parser.get('KAFKA', 'kafka_schema_registry_password')} 
                kafka_schema_registry_port: {parser.get('KAFKA', 'kafka_schema_registry_port')} 
                postgres_host: {parser.get('POSTGRES', 'postgres_host')} 
                postgres_user: {parser.get('POSTGRES', 'postgres_user')} 
                postgres_password: {parser.get('POSTGRES', 'postgres_password')} 
                postgres_port: {parser.get('POSTGRES', 'postgres_port')} 
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
            with open(config_file_path, 'w') as config:
                parser.write(config)

            print('\nSetup successful! \nRun medrical -help for help')

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

    with open(config_file_path, 'w') as config:
        parser.write(config)

    verify_configuration()


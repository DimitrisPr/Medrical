
<img src="https://prasakis.com/github/medrical.png?new" width="160" align="right">

**Tech Stack**

[![Build Status](https://img.shields.io/badge/Build%20with-Python-9CF?&logo=python)](https://img.shields.io/badge/Build%20with-python-9CF) 
[![Build Status](https://img.shields.io/badge/Published%20on%20PyPi-v0.1.10-9CF)](https://img.shields.io/badge/Build%20with-python-9CF) [![Build with](https://img.shields.io/badge/Built%20on-Apache%20Kafka-yellow)](https://img.shields.io/badge/Build%20with-kafka-yellow) [![Build with](https://img.shields.io/badge/Built%20on-PostgreSQL-yellow)](https://img.shields.io/badge/Build%20with-postgres-yellow) 

**Social**

[![Built on](https://img.shields.io/badge/Personal-Website-Green)](https://prasakis.com/medrical) [![Built on](https://img.shields.io/badge/LinkedIn-Profile-blue)](https://www.linkedin.com/in/dimitrisprs/)  [![Built on](https://img.shields.io/github/followers/dimitrispr?style=social)](https://img.shields.io/badge/Build%20with-kafka-yellow) 

# General
 
Medrical is a real-time medical metric monitoring system, powered by Apache Kafka and postgreSQL. It continuously monitors patient biometrics (e.g heart rate, body temprature, systolic & diastolic blood pressure) and publishes them to Kafka topics. A JDBC connector subscribes to those topics and stores them into a PostgreSQL DB table.  
 
*Medrical is a wordplay derived from the phrase "medical metrics"*

Table of Contents
=================

* [General](#general)
* [Installation](#installation)
* [Configuration](#configuration)
  * [Medrical Configuration](#medrical-configuration) 
  * [JDBC Connector Sink Configuration](#jdbc-connector-sink-configuration)  
  * [SSL Configuration](#ssl-configuration)  
* [How to run - Medrical Client](#how-to-run---medrical-client)
  * [Medrical producer](#medrical-producer)
  * [Medrical Unit Tests](#medrical-unit-tests)
* [Understanding Medrical's Architecture](#understanding-the-architecture-of-medrical)
* [To Do's](#to-do-testing)

# Installation

Prior installation, consider using a virtual enviroment
```sh
~$ virtualenv medrical_env
~$ source medrical_env/bin/activate
```

Medrical is published to PyPi. Install it on your machine with:

```sh
~$ pip install medrical
```

or using the git repo 

```sh
~$ git clone https://github.com/DimitrisPr/medrical.git
~$ cd medrical
~$ pip install .
```

# Configuration

Medrical requires a running instance of:
- A Kafka enviroment, with schema registry enabled and the option `kafka.auto_create_topics_enable = true`
- <a href="https://github.com/aiven/aiven-kafka-connect-jdbc"> A Kafka JDBC connector sink </a>
- A postgreSQL database (ideally with TimescaleDB extension enabled for future integrations)

## Medrical Configuration

Medrical can be configured with:

```sh
~$ medrical-configure
```

The cli configuration interface requests the credentials of Kafka, Schema and postgreSQL.

Medrical can be re-configured at a later point in time.

### Demo Medrical configuration

<img src="https://prasakis.com/github/medrical-configure.png" width="450">

## JDBC Connector Sink Configuration

The JDBC connector's configuration must support several requirements including:

- AVRO serialization converters
- Topic regex
- Dynamic topic naming

### Demo JDBC connector configuration

```
{
    "name": "sink",
    "connector.class": "io.aiven.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "key.converter.schema.registry.url": "https://username:password@host:port",
    "key.converter.basic.auth.credentials.source": "USER_INFO",
    "key.converter.basic.auth.user.info": "username:password",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "https://username:password@host:port",
    "value.converter.basic.auth.credentials.source": "USER_INFO",
    "value.converter.basic.auth.user.info": "username:password",
    "topics.regex": "biometrics_(.*)",
    "connection.url": "jdbc:postgresql://host:port/db_name",
    "connection.user": "username",
    "connection.password": "password",
    "insert.mode": "insert",
    "table.name.format": "${topic}",
    "auto.create": "true",
    "auto.evolve": "true",
    "schema.registry.url": "https://username:password@host:port"
}
```

Note that the proper configuration of the medrical application and the JDBC Connector is essential in order for medrical to run.

## SSL Configuration

The Medrical configurator provides a cli interface for SSL configuration `medrical configure ssl`, but it is unstable and has only been tested in Linux. 
Alternatively, the {access key, access certificate, CA certificate} = {ca.pem, service.cert, service.key} files must either be manually added to `medrical/config/ssl/` directory with the exact aforementioned names, or be programmatically added as strings in the code of `medrical/producer/producer.py`.


<img src="https://prasakis.com/github/medrical-ssl.png" width="700">



# How to run - Medrical Client

Just like the configuration cli interface, medrical application can be launched with:

```sh
~$ medrical
```

<img src="https://prasakis.com/github/medrical-cli.png?new" width="450">

## Medrical producer

The medrical producer can be launched with:
```sh
~$ medrical produce
```
The produces publishes by default events to a topic named "biometrics_default". The topic name can be changed programmatically. The JDBC connector is subscribed to topics with names based on the regex `biometrics_(.*)`.


## Medrical unit tests

There are two unit tests currently implemented in medrical. A test for the JDBC connector and a test for the Kafka biometric producer. The former and the latter can be executed with the following commands respectively.

```sh
~$ medrical test connector
~$ medrical test producer
```

### To Do Testing

Throughout testing of later versions should include:

- More unit tests for JDBC producer (e.g test that *every* new event is properly published when running in a loop continuously)
- More unit tests for JDBC connector (e.g time needed to create a new table given a new topic,) 
- Test for the Medrical's command line client

## Understanding the architecture of Medrical

The following table presents briefly each medical submodule 

| File/Module | Brief description |
| ------ | ------ |
| medrical/producer/patient.py | This module simulates the biometrics of a patient similar to the [Aiven's fake Pizza Data Producer](https://github.com/aiven/kafka-python-fake-data-producer)|
| medrical/producer/producer.py | This is a Kafka producer. It monitors patient's biometrics and publishes them as events to Kafka |
| medrical/cli/cli.py | This module implements the Medrical's command line interface |
| medrical/config| This module has several configuration files concerning the AVRO schemas, SSL certificates, medrical configuration etc |
| medrical/config/config.py | This module is the Medrical's configuration script. It is used by cli.py |
| medrical/config/pipeline.cfg | This config file stores Kafka's and PostgreSQL's credentials |
| medrical/config/ssl | This directory stores all the SSL related certificates/keys |
| medrical/config/schemas | This directory stores the value and key AVRO schemas |
| tests/ | This module includes all the unit tests |
| tests/test_producer.py | Test that verifies that the producer publishes the topics succesfully to Kafka. |
| tests/test_connector.py | Test that verifies whether a postgreSQL table is auto-created when the producer publishes a new topic. |
                                                                                                      



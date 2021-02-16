from datetime import datetime
import threading
import random
import time
import json


class Patient:
    ''' Produces fake biobiometric data

    This class is intended to produce fake biobiometric
    data for consumption by Kafka.
    '''

    def __init__(self, name='', surname='', age=-1, id_='-1'):
        ''' Constructs a patient. 

            Args:
                name (str): The name of the patient
                surname (str): The surname of the patient
                age (int): The age of the patient
                id (int): The id of the patient
        '''

        self.name = name
        self.surname = surname
        self.age = age
        self.id_ = id_
        self.pulse = random.randint(80, 90)
        self.oxygen = random.randint(95, 100)
        self.temprature = random.uniform(35.5, 37.2)
        self.systolic = random.randint(100, 110)
        self.diastolic = random.randint(65, 80)

    def get_pulse(self):
        '''Simulate current heartrate (pulse) beat-per-minute (bpm)'''
        return random.randint(self.pulse - 1, self.pulse + 1)

    def get_oxygen(self):
        '''Simulates the oxygen level of a patient.'''
        return random.randint(self.pulse - 1, self.pulse + 1)

    def get_temprature(self):
        '''Simulates the body temprature of a patient.'''
        return random.uniform(
            self.temprature - (0.1), self.temprature + (0.1))

    def get_systolic_pressure(self):
        '''Simulates the systolic pressure of a patient.'''
        return random.randint(self.systolic - 1, self.systolic + 1)

    def get_diastolic_pressure(self):
        '''Simulates the diastolic pressure of a patient.'''
        return random.randint(self.diastolic - 1, self.diastolic + 1)

    def get_biometrics(self):
        ''' Returns patient's biometrics, json format '''
        biometrics = {
            "heartbeat": self.get_pulse(),
            "oxygen": self.get_oxygen(),
            "temprature": round(self.get_temprature(), 1),
            "systolic": self.get_systolic_pressure(),
            "diastolic": self.get_diastolic_pressure(),
            "time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }

        return biometrics

    def get_id(self):
        ''' Returns id in dictonary '''
        return {"id": self.id_}


if __name__ == '__main__':
    pass

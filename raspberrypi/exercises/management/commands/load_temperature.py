import os
import glob
import time
from exercises.models import TemperatureReading
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Load tempreature reading to database'

    def handle(self, *args, **options):
        temp_c, temp_f = self.read_temp()

        TemperatureReading.objects.create(tempC=temp_c, tempF=temp_f)
        self.stdout.write(self.style.SUCCESS("Success"))

        last_temp = TemperatureReading.objects.last()
        if last_temp.tempC > 35:
            send_mail('Alarm', 'Temperatura w poomieszczeniu przekroczyła 40°C, sprawdź co się dzieje.',
                      'krzanowski.maciek@gmail.com', ['krzanowski.maciek@gmail.com'])
        if last_temp.tempC < 10:
            send_mail('Alarm', 'Temperatura w poomieszczeniu obniżyła się do 10°C, sprawdź co się dzieje.',
                      'krzanowski.maciek@gmail.com', ['krzanowski.maciek@gmail.com'])

    @staticmethod
    def read_temp_raw():
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]  # return a list(in this case [0]-string), of directories
        device_file = device_folder + '/w1_slave'

        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':  # strip() remove all white spaces at start and end
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')  # take list index of t
        if equals_pos != -1:  # if temp is not empty proceed
            temp_string = lines[1][equals_pos + 2:]  # take temp value
            temp_c = float(temp_string) / 1000.0  # Celecius
            temp_f = temp_c * 9.0 / 5.0 + 32.0  # Farenheit
            return temp_c, temp_f



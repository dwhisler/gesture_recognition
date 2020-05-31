import serial
import keyboard
import time
import os

def read_session():
    print("Looking for Arduino...")
    with serial.Serial('/dev/ttyACM0', 115200) as ser:
        print("Arduino found!")
        raw_data = []
        new_data_available = False

        performer = "bill"
        take = 1

        measuring_bias = True
        while (ser.readline().strip().decode('utf-8') == "Measuring bias..."):
            if (measuring_bias):
                measuring_bias = False
                print('Measuring bias...')

        print('Ready for new capture, press q to quit, CTRL to capture new data')
        while not keyboard.is_pressed('q'):
            if keyboard.is_pressed('ctrl'):
                gesture = 'leftcircle'
                new_data_available = True
                print('Capturing data, press Space to stop')
                while not keyboard.is_pressed('space'):
                    raw_data.append(ser.readline())
            if (new_data_available):
                new_data_available = False
                print('Finished capturing')
                parse_data(raw_data, gesture, performer, take)
                take += 1
                raw_data = []
                print('Ready for new capture, press q to quit, CTRL to capture new data')
        print('Finished session')

def parse_data(raw_data, gesture, performer, take):
    path = '../data/session2/'

    fname = path + performer + '_' + gesture + '_' + str(take) + '.csv'

    with open(fname, 'w') as f:
        f.write('accX,gyrX,accY,gyrY,accZ,gyrZ,qW,qX,qY,qZ,sample_rate,\n')
        for data in raw_data:
            data_str = data.strip().decode('utf-8').split()
            for s in data_str:
                f.write(s + ',')
            f.write('\n');

if __name__ == '__main__':
    read_session()

import serial
import keyboard
import time
import os
import sys

# Function to create progress bar in terminal to help gesture timing
def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

# Reads training gesture data via a command line interface
def read_session_fixed_len():
    print("Looking for Arduino...")
    with serial.Serial('/dev/ttyACM0', 115200) as ser:
        print("Arduino found!")
        raw_data = []
        new_data_available = False

        performer = "david"
        take = 1
        gesture = 'right'
        seq_length = 256

        print('Gesture:', gesture)

        measuring_bias = True
        while (ser.readline().strip().decode('utf-8') == "Measuring bias..."):
            if (measuring_bias):
                measuring_bias = False
                print('Measuring bias...')

        print('Ready for new capture, press q to quit, space to capture new data')
        while not keyboard.is_pressed('q'):
            if keyboard.is_pressed('space'):

                new_data_available = True
                print('Capturing data, press Space to stop')
                while len(raw_data) < seq_length:
                    raw_data.append(ser.readline())
                    update_progress(len(raw_data)/seq_length)

            if (new_data_available):
                new_data_available = False
                print('Finished capturing take', take)
                parse_data(raw_data, gesture, performer, take)
                take += 1
                raw_data = []
                print('Ready for new capture, press q to quit, space to capture new data')

        print('Finished session')

# Parses raw data from serial port and saves to local file
def parse_data(raw_data, gesture, performer, take):
    path = '../data/session5/'

    fname = path + performer + '_' + gesture + '_' + str(take) + '.csv'

    with open(fname, 'w') as f:
        f.write('accX,gyrX,accY,gyrY,accZ,gyrZ,qW,qX,qY,qZ,sample_rate,\n')
        for data in raw_data:
            data_str = data.strip().decode('utf-8').split()
            for s in data_str:
                f.write(s + ',')
            f.write('\n');

if __name__ == '__main__':
    read_session_fixed_len()

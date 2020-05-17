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

        performer = "david"
        take = 1

        measuring_bias = True
        while (ser.readline().strip().decode('utf-8') == "Measuring bias..."):
            if (measuring_bias):
                measuring_bias = False
                print('Measuring bias...')

        print('Ready for new capture, press q to quit, CTRL to capture new data')
        while not keyboard.is_pressed('q'):
            if keyboard.is_pressed('ctrl'):
                print('Which gesture will you perform? 1 for Wing, 2, for Ring, 3 for Slope, 4 for None')
                time.sleep(0.1)
                gesture = keyboard.read_key()
                while not (gesture == '1' or gesture == '2' or gesture == '3' or gesture == '4'):
                    print("Gesture not recognized")
                    print('Which gesture will you perform? 1 for Wing, 2, for Ring, 3 for Slope, 4 for None')
                    gesture = keyboard.read_key()

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
    if gesture == '1':
        gesture = 'wing'
    elif gesture == '2':
        gesture = 'ring'
    elif gesture == '3':
        gesture = 'slope'
    else:
        gesture = 'none'

    fname = performer + '_' + gesture + '_' + str(take) + '.csv'

    with open(fname, 'w') as f:
        f.write('accX,gyrX,accY,gyrY,accZ,gyrZ,qW,qX,qY,qZ,sample_rate,\n')
        for data in raw_data:
            data_str = data.strip().decode('utf-8').split()
            for s in data_str:
                f.write(s + ',')
            f.write('\n');

if __name__ == '__main__':
    read_session()

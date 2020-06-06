import serial
import keyboard

# Performs action based on received interpreted gesture from Arduino over serial
def gesture_interpreter():
    print('Looking for Arduino...')
    with serial.Serial('/dev/ttyACM0', 115200) as ser:
        print("Arduino found!")
        measuring_bias = True
        while (ser.readline().strip().decode('utf-8') == "Measuring bias..."):
            if (measuring_bias):
                measuring_bias = False
                print('Measuring bias...')

        print('Ready!')
        while(ser):
            gesture = ser.readline().strip().decode('utf-8')
            print(gesture)
            if (gesture == 'Down'):
                keyboard.press_and_release('j')
            elif (gesture == 'Up'):
                keyboard.press_and_release('l')
            elif (gesture == 'Right'):
                keyboard.press_and_release('k')

if __name__ == '__main__':
    gesture_interpreter()

import numpy as np
import pygatt
import binascii

def read_gesture_ble():
    YOUR_DEVICE_ADDRESS = "CF:06:15:AB:CC:AF"

    # The BGAPI backend will attempt to auto-discover the serial device name of the
    # attached BGAPI-compatible USB adapter.
    adapter = pygatt.GATTToolBackend()

    adapter.start()
    device = adapter.connect(YOUR_DEVICE_ADDRESS)
    characteristics = adapter.discover_characteristics(device)
    # uuids = list(characteristics.keys())
    # print(uuids)
    #print(device.char_read(uuids[3]))

    for uuid in characteristics.keys():
        print(uuid)
    #     print(device.char_read(uuid))
    adapter.disconnect(device)
    adapter.stop()


if __name__ == '__main__':
    read_gesture_ble()

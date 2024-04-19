from evdev import InputDevice
from select import select


# INPUT PARAMETERS
MOUSE_INPUT = "/dev/input/event9"
KEYBOARD_INPUT = "/dev/input/event5"

# OUTPUT PARAMETER
OUTPUT_FILENAME = "event_file.txt"

devices = map(InputDevice, (MOUSE_INPUT, KEYBOARD_INPUT))
devices = {dev.fd: dev for dev in devices}

for dev in devices.values():
    with open(OUTPUT_FILENAME, 'w') as file:
        while True:
            r, w, x = select(devices, [], [])
            for fd in r:
                for event in devices[fd].read():
                    file.write(str(event) + "\n")
                    print(event)
                    
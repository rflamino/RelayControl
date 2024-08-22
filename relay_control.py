# RelayControl - Serial control of relay board UD74B08 8ch IO Digital USB COM Serial Port UART Relay Module
# Author: Reinaldo S. Flamino
# Description: This Python script allows you to control relays via a serial port connection.
# The script sends 8 bytes commands to toggle, turn on, turn off, interlock or momentarily activate relays connected to the specified COM port.

import serial  # py -m pip install pyserial
import sys
import time

def calculate_checksum(command_bytes):
    return sum(command_bytes) % 256

def create_command(relay, action):
    header = [0x55, 0x56]
    zeros = [0x00, 0x00, 0x00]
    command = header + zeros + [relay, action]
    checksum = calculate_checksum(command)
    command.append(checksum)  
    return bytearray(command)

def send_command(port, relay, action):
    try:
        with serial.Serial(
            port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.1
        ) as ser:
            command = create_command(relay, action)
            ser.write(command)
            ser.flush()  # Ensure all data is sent
            # Wait until there is data waiting in the input buffer
            while ser.in_waiting == 0:
                pass  # Busy-wait for data to arrive
            
            #print(f"Sent command: {' '.join(format(x, '02X') for x in command)}")

            # Now read the 8-byte response from the device
            response = ser.read(8)  # Read 8 bytes from the serial port
            if len(response) == 8:
                #print(f"Received response: {' '.join(format(x, '02X') for x in response)}")
                return response
            else:
                print("Error: Did not receive 8 bytes from the device.")
                return None

    except serial.SerialException as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_all_relay_statuses(response, action):
    if response:
        if action == 7:  # ALL ON
            print("All relays are now ON.")
        elif action == 8:  # ALL OFF
            print("All relays are now OFF.")
        else:
            relay_number = response[5]  # 6th byte in the response represents the relay number
            relay_status = response[6]  # 7th byte in the response represents the relay status
            status_map = {1: 'ON', 2: 'OFF'}
            status = status_map.get(relay_status, 'UNKNOWN')
            print(f"Relay {relay_number}: {status}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python relay_control.py <COM_PORT> <RELAY_NUMBER> <ACTION>")
        print("RELAY_NUMBER: 1-8")
        print("ACTION: 0=READ STATUS 1=ON, 2=OFF, 3=TOGGLE, 4=INTERLOCK, 5=MOMENTARY ON, 7=ALL ON, 8=ALL OFF")
        sys.exit(1)

    port = sys.argv[1]
    relay = int(sys.argv[2])
    action = int(sys.argv[3])

    if relay < 1 or relay > 8:
        print("Error: Relay number must be between 1 and 8.")
        sys.exit(1)

    if action not in [0,1, 2, 3, 4, 5, 7, 8]:
        print("Error: Action must be 0 (READ STATUS), 1 (ON), 2 (OFF), 3 (TOGGLE), 4 (INTERLOCK),5 (MOMENTARY ON), 7 (ALL ON), or 8 (ALL OFF).")
        sys.exit(1)

    response = send_command(port, relay, action)

    # Print the status of all relays in a compact way
    print_all_relay_statuses(response, action)

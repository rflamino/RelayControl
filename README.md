# RelayControl
Serial control of relay board UD74B08 8ch IO Digital USB COM Serial Port UART Relay Module.
This Python script allows you to control relays via a serial port connection. The script sends hexadecimal commands to toggle, turn on, turn off, or momentarily activate relays connected to the specified COM port.

Command is:
python relay_control.py <COM_PORT> <RELAY_NUMBER> <ACTION>

where parameters are:
<COM_PORT>: The COM port to which the relay device is connected (e.g., COM4).
<RELAY_NUMBER>: The relay number you want to control (1-8).
<ACTION>: The action to perform on the relay:
1: Turn ON
2: Turn OFF
3: Toggle
4: Momentary ON (0.5-second hold, then release)


To toggle relay 1 connected to COM4:
python relay_control.py COM4 1 3



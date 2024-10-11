import time
from machine import Pin, UART

# Define UART values
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1)

# Send and receive a message
uart.write("Sent from Abby")
while True:
    if uart.any():
        data = uart.read()
        print(data)
        break  # Exit the loop after the first message

    
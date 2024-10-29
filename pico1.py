# This code is licensed under the MIT License, and Apache License
# machine by Raspberry Pi Ltd. 4.0 International Licence 
# TIME by Nicholas Delinte. GNU General Public License v3.0
import time
from machine import Pin, UART, PWM, ADC #import libraries 

# Initializing UART for communication between Picos
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)) #this info was given in previous lab 
uart.init(bits=8, parity=None, stop=1)

# Initialize ADC to read the analog signal
adc = ADC(Pin(26)) #connected to pin 26

# Initialize PWM on Pin 15 for signal output
pwm_pin = Pin(15) # connected to pin 15
pwm = PWM(pwm_pin)
pwm_frequency = 1000  # Set initial frequency to 1 kHz
pwm.freq(pwm_frequency)

# Initialize LEDs on Pins 16 and 17 for indicating message reception and transmission
receive_led = Pin(16, Pin.OUT)  # LED for message reception (red LED)
send_led = Pin(17, Pin.OUT)     # LED for message sending (green LED)

def process_pwm():
    # function reads analog signal and adjusts the pwm duty cycle to match it 
    analog_value = adc.read_u16()  # Read 16-bit ADC value (0 to 65535, min and max)
    
    # Set PWM duty cycle based on the ADC value
    pwm.duty_u16(analog_value)  # Output filtered PWM signal on Pin 15
    print(f"Analog PWM control: Frequency={pwm_frequency} Hz, Duty Cycle={(analog_value / 65535) * 100:.2f}%") #print values
    
    # Read ADC value (0 to 65535, as it's a 16-bit ADC)
    return analog_value

while True:
    # Process the analog input to adjust PWM duty cycle
    analog_value = process_pwm()

    # Check if a message is received from the other Pico
    if uart.any():
        message = uart.read() #read the message 
        try:
            # Decode the message if available
            decoded_message = message.decode('utf-8').strip()
            print(f"Received PWM signal from the other Pico: {decoded_message}, PWM signal from my Pico: {analog_value}")

            # Light up the receive LED when a message is received
            receive_led.value(1)
            time.sleep(1)  # Keep LED on for 1 second
            receive_led.value(0)
        
        # handle errors and debug  
        except UnicodeDecodeError: # where data given is not valid
            print("Error decoding message: Non-UTF-8 bytes received")
        except Exception as e: # any other unexpected errors
            print(f"Unexpected error: {e}")

    # Send the analog PWM signal as a formatted string over UART
    uart.write(f"{analog_value}\n")  # Send the message as a newline-terminated string
    
    # Light up the send LED when a message is sent
    send_led.value(1)
    time.sleep(1)  # Keep LED on for 1 second
    send_led.value(0)

    # Delay to avoid data collision
    time.sleep(1)


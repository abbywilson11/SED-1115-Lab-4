from machine import Pin
import time

DS = Pin(20, Pin.OUT)
SHCP = Pin(18, Pin.OUT)
STCP = Pin(19, Pin.OUT)
OE = Pin(21, Pin.OUT)

#set bits/lights to all off
off = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

#change on and off 
lights = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

north_red = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,1]]
north_yellow = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,1,0]]
north_green = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,1,0,0]]
north_car = [[0,0,0,0], [1,0,0,0], [0,0,0,0], [0,0,0,0]]

east_red = [[0,0,0,0], [0,0,0,0], [0,0,0,1], [0,0,0,0]]
east_yellow = [[0,0,0,0], [0,0,0,0], [0,0,1,0], [0,0,0,0]]
east_green = [[0,0,0,0], [0,0,0,0], [0,1,0,0], [0,0,0,0]]
east_car = [[1,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]

south_red = [[0,0,0,0], [0,0,0,1], [0,0,0,0], [0,0,0,0]]
south_yellow = [[0,0,0,0], [0,0,1,0], [0,0,0,0], [0,0,0,0]]
south_green = [[0,0,0,0], [0,1,0,0], [0,0,0,0], [0,0,0,0]]
south_car = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [1,0,0,0]]

west_red = [[0,0,0,1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
west_yellow = [[0,0,1,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
west_green = [[0,1,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
west_car = [[0,0,0,0], [0,0,0,0], [1,0,0,0], [0,0,0,0]]

#Making my function that turns the lights on (blender)
def shift_register_output(light_settings):

    # Shift out 16 bits to the shift register (1 by 1)
    for direction in light_settings: 
        for bit in direction : 
            DS.value(bit)
            # Clock line
            SHCP.value(1)
            SHCP.value(0)
    #store memory
    STCP.value(1)
    STCP.value(0)
    OE.off()
    print("Shift registor was succesfuly outputed.")

#define shift register output for lights 
shift_register_output(lights)

#define names of each light for printing in terminal
def cycle_lights():
    light_states = [
        (north_red, "North Red"),
        (north_yellow, "North Yellow"),
        (north_green, "North Green"),
        (north_car, "North Car"),
        (east_red, "East Red"),
        (east_yellow, "East Yellow"),
        (east_green, "East Green"),
        (east_car, "East Car"),
        (south_red, "South Red"),
        (south_yellow, "South Yellow"),
        (south_green, "South Green"),
        (south_car, "South Car"),
        (west_red, "West Red"),
        (west_yellow, "West Yellow"),
        (west_green, "West Green"),
        (west_car, "West Car")

    ]

#in terminal, show when the light is turned on and off 
    for state, name in light_states:
        print(f"Turning on {name}") #calling strings has to be with curly brackets
        shift_register_output(state)
        time.sleep(5)  # Keep the light on for 5 seconds
        
        print(f"Turning off {name}")
        shift_register_output(off)  # Turn off all lights
        time.sleep(1)  # Short pause between states of the lights

print(lights)

# Run the light cycle
while True:
    cycle_lights()
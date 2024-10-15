import time
from gpiozero import OutputDevice

# Define GPIO pins for machine control (change these as per your setup)
labeling_start_pin = 6
labeling_stop_pin = 27
filling_stop_pin = 23
blowing_start_pin = 24
blowing_stop_pin = 22

# Initialize OutputDevice objects for each machine control
labeling_start = OutputDevice(labeling_start_pin)
labeling_stop = OutputDevice(labeling_stop_pin)
filling_stop = OutputDevice(filling_stop_pin)
blowing_start = OutputDevice(blowing_start_pin)
blowing_stop = OutputDevice(blowing_stop_pin)

# Functions to control each machine
def start_labeling_machine():
    labeling_start.on()
    time.sleep(2)  # Hold high for 2 seconds to start
    labeling_start.off()
    print("Labeling machine started.")

def stop_labeling_machine():
    labeling_stop.on()
    time.sleep(2)  # Hold high for 2 seconds to stop
    labeling_stop.off()
    print("Labeling machine stopped.")

def start_filling_machine():
    filling_stop.off()  # Assume LOW starts the machine
    print("Filling machine started.")

def stop_filling_machine():
    filling_stop.on()  # Assume HIGH stops the machine
    print("Filling machine stopped.")

def start_blowing_machine():
    blowing_start.on()
    blowing_stop.off()  # Ensure stop is off when starting
    print("Blowing machine started.")

def stop_blowing_machine():
    blowing_start.off()
    blowing_stop.on()
    print("Blowing machine stopped.")

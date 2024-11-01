import time
from gpiozero import OutputDevice

# GPIO pin assignments
labeling_start_pin = 6
labeling_stop_pin = 27
filling_stop_pin = 23
# blowing_start_pin = 24
blowing_stop_pin = 25

# Initialize OutputDevice objects for each machine control
labeling_start = OutputDevice(labeling_start_pin)
labeling_stop = OutputDevice(labeling_stop_pin)
filling_stop = OutputDevice(filling_stop_pin)
# blowing_start = OutputDevice(blowing_start_pin)
blowing_stop = OutputDevice(blowing_stop_pin)

def start_labeling_machine():
    labeling_start.on()
    time.sleep(2)
    labeling_start.off()
    print("Labeling machine started.")

def stop_labeling_machine():
    labeling_stop.on()
    time.sleep(2)
    labeling_stop.off()
    print("Labeling machine stopped.")

def start_filling_machine():
    filling_stop.off()
    print("Filling machine started.")

def stop_filling_machine():
    filling_stop.on()
    print("Filling machine stopped.")

def start_blowing_machine():
    blowing_stop.off()
    print("Blowing machine started.")

def stop_blowing_machine():
    blowing_stop.on()
    print("Blowing machine stopped.")

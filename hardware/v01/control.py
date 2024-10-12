import time
from gpio_setup import *

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
    blowing_start.on()
    blowing_stop.off()
    print("Blowing machine started.")

def stop_blowing_machine():
    blowing_start.off()
    blowing_stop.on()
    print("Blowing machine stopped.")

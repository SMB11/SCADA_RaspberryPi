
import time

def start_labeling_machine():
    LABELING_START_PIN.on()
    time.sleep(2)
    LABELING_START_PIN.off()
    print("Labeling machine started.")

def stop_labeling_machine():
    LABELING_STOP_PIN.on()
    time.sleep(2)
    LABELING_STOP_PIN.off()
    print("Labeling machine stopped.")

def stop_filling_machine():
    FILLING_STOP_PIN.on()
    print("Filling machine stopped.")

def start_filling_machine():
    FILLING_STOP_PIN.off()
    print("Filling machine started.")

def start_blowing_machine():
    BLOWING_START_PIN.on()
    BLOWING_STOP_PIN.off()
    print("Blowing machine started.")

def stop_blowing_machine():
    BLOWING_START_PIN.off()
    BLOWING_STOP_PIN.on()
    print("Blowing machine stopped.")

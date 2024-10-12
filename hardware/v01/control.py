import time
from gpio_setup_lgpio import chip_handle, LABELING_START_PIN, LABELING_STOP_PIN, FILLING_STOP_PIN, BLOWING_START_PIN, BLOWING_STOP_PIN

def start_labeling_machine():
    lgpio.gpio_write(chip_handle, LABELING_START_PIN, 1)
    time.sleep(2)
    lgpio.gpio_write(chip_handle, LABELING_START_PIN, 0)
    print("Labeling machine started.")

def stop_labeling_machine():
    lgpio.gpio_write(chip_handle, LABELING_STOP_PIN, 1)
    time.sleep(2)
    lgpio.gpio_write(chip_handle, LABELING_STOP_PIN, 0)
    print("Labeling machine stopped.")

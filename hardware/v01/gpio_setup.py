import lgpio
import time

# Define the GPIO pins
LABELING_START_PIN = 4
LABELING_STOP_PIN = 27
FILLING_STOP_PIN = 23
BLOWING_START_PIN = 24
BLOWING_STOP_PIN = 22
SENSOR1_PIN = 19
SENSOR2_PIN = 20

# Initialize GPIO chip (usually 0 on Pi)
chip_handle = lgpio.gpiochip_open(0)

# Setup output pins
lgpio.gpio_claim_output(chip_handle, LABELING_START_PIN)
lgpio.gpio_claim_output(chip_handle, LABELING_STOP_PIN)
lgpio.gpio_claim_output(chip_handle, FILLING_STOP_PIN)
lgpio.gpio_claim_output(chip_handle, BLOWING_START_PIN)
lgpio.gpio_claim_output(chip_handle, BLOWING_STOP_PIN)

# Setup input pins
lgpio.gpio_claim_input(chip_handle, SENSOR1_PIN)
lgpio.gpio_claim_input(chip_handle, SENSOR2_PIN)

# Function to release GPIO resources
def cleanup_gpio():
    lgpio.gpiochip_close(chip_handle)

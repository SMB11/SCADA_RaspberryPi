import time

def start_labeling_machine(GPIO, LABELING_START_PIN, LABELING_STOP_PIN):
    GPIO.output(LABELING_START_PIN, GPIO.HIGH)
    time.sleep(2)  # Hold high for 2 seconds
    GPIO.output(LABELING_START_PIN, GPIO.LOW)
    print("Labeling machine started.")

def stop_labeling_machine(GPIO, LABELING_START_PIN, LABELING_STOP_PIN):
    GPIO.output(LABELING_STOP_PIN, GPIO.HIGH)
    time.sleep(2)  # Hold high for 2 seconds
    GPIO.output(LABELING_STOP_PIN, GPIO.LOW)
    print("Labeling machine stopped.")

def stop_filling_machine(GPIO, FILLING_STOP_PIN):
    GPIO.output(FILLING_STOP_PIN, GPIO.HIGH)
    print("Filling machine stopped.")
    
def start_filling_machine(GPIO, FILLING_STOP_PIN):
    GPIO.output(FILLING_STOP_PIN, GPIO.LOW)
    print("Filling machine started.")

def start_blowing_machine(GPIO, BLOWING_START_PIN, BLOWING_STOP_PIN):
    GPIO.output(BLOWING_START_PIN, GPIO.HIGH)
    GPIO.output(BLOWING_STOP_PIN, GPIO.LOW)
    print("Blowing machine started.")

def stop_blowing_machine(GPIO, BLOWING_START_PIN, BLOWING_STOP_PIN):
    GPIO.output(BLOWING_START_PIN, GPIO.LOW)
    GPIO.output(BLOWING_STOP_PIN, GPIO.HIGH)
    print("Blowing machine stopped.")

from gpiozero import LED, Button

def initialize_gpio():
    global LABELING_START_PIN, LABELING_STOP_PIN, FILLING_STOP_PIN, BLOWING_START_PIN, BLOWING_STOP_PIN
    global SENSOR1_PIN, SENSOR2_PIN
    global LABELING_WORKING_PIN, LABELING_ALARM_PIN, LABELING_ALARM_HANDLED_PIN
    global FILLING_WORKING_PIN, FILLING_ALARM_PIN, FILLING_ALARM_HANDLED_PIN
    global BLOWING_WORKING_PIN, BLOWING_ALARM_PIN

    # Output pins for machine controls
    LABELING_START_PIN = LED(4)
    LABELING_STOP_PIN = LED(27)
    FILLING_STOP_PIN = LED(23)
    BLOWING_START_PIN = LED(24)
    BLOWING_STOP_PIN = LED(22)

    # Input pins for sensors and machine status
    SENSOR1_PIN = Button(19, pull_up=True)
    SENSOR2_PIN = Button(20, pull_up=True)
    LABELING_WORKING_PIN = Button(21, pull_up=True)
    LABELING_ALARM_PIN = Button(19, pull_up=True)
    LABELING_ALARM_HANDLED_PIN = Button(12, pull_up=True)
    FILLING_WORKING_PIN = Button(16, pull_up=True)
    FILLING_ALARM_PIN = Button(5, pull_up=True)
    FILLING_ALARM_HANDLED_PIN = Button(6, pull_up=True)
    BLOWING_WORKING_PIN = Button(18, pull_up=True)
    BLOWING_ALARM_PIN = Button(10, pull_up=True)

def cleanup_gpio():
    # Properly release resources
    LABELING_START_PIN.close()
    LABELING_STOP_PIN.close()
    FILLING_STOP_PIN.close()
    BLOWING_START_PIN.close()
    BLOWING_STOP_PIN.close()

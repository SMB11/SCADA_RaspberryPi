
from gpiozero import LED, Button
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

def initialize_gpio():
    global LABELING_START_PIN, LABELING_STOP_PIN, FILLING_STOP_PIN, BLOWING_START_PIN, BLOWING_STOP_PIN
    global SENSOR1_PIN, SENSOR2_PIN
    global LABELING_WORKING_PIN, LABELING_ALARM_PIN, LABELING_ALARM_HANDLED_PIN
    global FILLING_WORKING_PIN, FILLING_ALARM_PIN, FILLING_ALARM_HANDLED_PIN
    global BLOWING_WORKING_PIN, BLOWING_ALARM_PIN

    LABELING_START_PIN = LED(4, pin_factory=factory)
    LABELING_STOP_PIN = LED(27, pin_factory=factory)
    FILLING_STOP_PIN = LED(23, pin_factory=factory)
    BLOWING_START_PIN = LED(24, pin_factory=factory)
    BLOWING_STOP_PIN = LED(22, pin_factory=factory)

    SENSOR1_PIN = Button(13, pin_factory=factory)
    SENSOR2_PIN = Button(26, pin_factory=factory)
    LABELING_WORKING_PIN = Button(21, pin_factory=factory)
    LABELING_ALARM_PIN = Button(19, pin_factory=factory)
    LABELING_ALARM_HANDLED_PIN = Button(12, pin_factory=factory)
    FILLING_WORKING_PIN = Button(16, pin_factory=factory)
    FILLING_ALARM_PIN = Button(5, pin_factory=factory)
    FILLING_ALARM_HANDLED_PIN = Button(6, pin_factory=factory)
    BLOWING_WORKING_PIN = Button(18, pin_factory=factory)
    BLOWING_ALARM_PIN = Button(10, pin_factory=factory)

def cleanup_gpio():
    LABELING_START_PIN.close()
    LABELING_STOP_PIN.close()
    FILLING_STOP_PIN.close()
    BLOWING_START_PIN.close()
    BLOWING_STOP_PIN.close()

from gpiozero import Button, OutputDevice

# Define output devices for machine control
labeling_start = OutputDevice(4)
labeling_stop = OutputDevice(27)
filling_stop = OutputDevice(23)
blowing_start = OutputDevice(24)
blowing_stop = OutputDevice(22)

# Define input devices for status and alarm monitoring
labeling_working = Button(21, pull_up=True)
labeling_alarm = Button(19, pull_up=True)
labeling_alarm_handled = Button(12, pull_up=True)
filling_working = Button(16, pull_up=True)
filling_alarm = Button(5, pull_up=True)
filling_alarm_handled = Button(6, pull_up=True)
blowing_working = Button(18, pull_up=True)
blowing_alarm = Button(10, pull_up=True)

# Define sensors for bottle counting
sensor1 = Button(13, pull_up=True)
sensor2 = Button(26, pull_up=True)

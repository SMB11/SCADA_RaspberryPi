from gpiozero import Button, OutputDevice

# Define input and output devices using gpiozero

# Labeling Machine
labeling_start = OutputDevice(4)
labeling_stop = OutputDevice(27)
labeling_working = Button(21)
labeling_alarm = Button(19)
labeling_alarm_handled = Button(12)

# Filling Machine
filling_stop = OutputDevice(23)
filling_working = Button(16)
filling_alarm = Button(5)
filling_alarm_handled = Button(6)

# Blowing Machine
blowing_start = OutputDevice(24)
blowing_stop = OutputDevice(22)
blowing_working = Button(18)
blowing_alarm = Button(10)

# Sensors
sensor1 = Button(13)
sensor2 = Button(26)

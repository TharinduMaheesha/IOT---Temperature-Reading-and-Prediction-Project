
import os
import glob
import time
import RPi.GPIO as GPIO # python module to assist in controlling GPIO on a raspberry pi
import paho.mqtt.client as paho #provides a client class which enable applications to connect to an MQTT broker to publish sensor data
from paho import mqtt

GPIO.setmode(GPIO.BOARD) #specifying that the pins are refrred by the pin number on the plug
GPIO.setup(11,GPIO.OUT) # setting the GPIO pin 11 as output which connects the servo to control the servo
servo1 = GPIO.PWM(11,50) #setting servo pulse wdth modulation to 50Hz for the pin 11
servo1.start(0) # starting duty cycle with but without changing the axis angle (pulse off)

mqtt_broker = "broker.hivemq.com" #Defining mqtt broker
mqtt_port = 1883 # Defining default mqtt port
mqtt_topic = "IOTDBA_2022_05" # Specific MQTT topic for the system

#Executing commands
os.system('modprobe w1-gpio') # Enabling one wire interface
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/' #Assigning the base filepath of the sensor
device_folder = glob.glob(base_dir + '28*')[0] # Getting filepath
device_file = device_folder + '/w1_slave'


# Reading sensor output data in its raw form and converting to required format using this function 
def read_temp():
    
    #Reading the raw temperature
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()

    # Extracting the temperature reading by splitting the 12 bit output
    while lines[0].strip()[-3:] != 'YES':
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        
    equals_pos = lines[1].find('t=')
    
    # converting to degrees celcius
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_celcius = float(temp_string) / 1000.0
        return temp_celcius

# Calculating gauge axes angle based on input temperature.
def cal_angle(temp):

    if temp >= 10 and temp <= 40:
        angle = 180 - ((temp - 10)*6)
    elif temp < 10:
        angle = 180
    elif temp > 40:
        angle = 0

    return angle

# Calclating duty cycle (percentage on time)
# The range of sensor is between 0.5 ms and 2.5 ms pulse widths
# Meaning 0 degrees  = 0.5 ms and 180 degrees = 2.5 ms
# To calculate percentage on time we divide respective pulse width by 20 ms which is the pulse potential(1/50)
# Hence, 0 degree = 0.5 / 20 = 2.5% and 180 degrees = 2.5 / 20 = 12.5%
# increase in percentage by 1 will be = 180/(12.5 - 2.5) = 18 degree
# Hence to calculate the percentage for an angle of x = (x/18) + 2.5
# Adding 2.5 is necessary since the values does to start from 0 but from 2.5

def cal_dutycycle(angle):

    value = 2.5 + (angle/18)
    return value

# connecting to the paho client for mqtt
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.connect(mqtt_broker, mqtt_port)


# Main loop to read sensor data in regular intervals and to move the actuator 
# As well as to publsih the sensor data to the node red dashboard
while True:
    temp_true = read_temp() # Reading the  temp value from the sensor
    client.publish(mqtt_topic, payload= temp_true, qos=1) # Publishing the read value to the dashboard

    # rounding the temperature to the nearest whole number
    # Since we are only displaying effect and the temperature values as a whole number in the gauge 
    temp_rounded = round(temp_true) 
    print(temp_true)

    angle = cal_angle(temp_rounded) # Calculating angle to be moved by the actuator
    duty = cal_dutycycle(angle) # Calculating the percentage on time
    
    servo1.ChangeDutyCycle(duty)
    time.sleep(0.5) # Turning off for 0.5s to avoid the servo motor from moving(jitter) after moving initially
    servo1.ChangeDutyCycle(0) # Turning the pulse off
    time.sleep(5)




import serial

import time

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

def write_read(x):
	arduino.write(bytes(x, 'utf-8'))
	time.sleep(0.5)
	data = arduino.readline()
	return data

def send_angle():
    aAngle = input("Enter a angle for A :")
    bAngle = input("Enter a angle for B :")
    zHeigh = input("Enter a height for Z :")
    testString = "G0:A" + str(aAngle) + ":B" + str(bAngle) + ":Z" + zHeigh + "\r\n"
    value = write_read(testString)
    print(value)
    return 1
    
def send_speed():
    aSpeed = input("Enter a speed for A :")
    bSpeed = input("Enter a speed for B :")
    zSpeed = input("Enter a speed for Z :")
    testString = "G1:A" + str(aSpeed) + ":B" + str(bSpeed) + ":Z" + zSpeed + "\r\n"
    value = write_read(testString)
    print(value)
    return 1
    
def send_homing():
    testString = "G2:\r\n"
    value = write_read(testString)
    print(value)
    return 1
    
while True:
    choix = input(" 1 : move motor, 2 : setSpeed :")
    if choix == '1':
        send_angle()
    elif choix == '2':
        send_speed()
    elif choix == '3':
        send_homing()
    
    

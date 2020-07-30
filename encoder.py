#!/usr/bin/python3
from tkinter import *
import time
import os
import serial
import RPi.GPIO as GPIO
M1A = 21
M1B = 20
M2A = 13
M2B = 19
PWM1 = 16
PWM2 = 26
SERVO = 22
ENC1A = 2
ENC1B = 3
ENC2A = 14
ENC2B = 15
GPIO.setwarnings(False)
# Configuración de pines
GPIO.setmode(GPIO.BCM)
GPIO.setup(M1A,GPIO.OUT)
GPIO.setup(M1B,GPIO.OUT)
GPIO.setup(M2A,GPIO.OUT)
GPIO.setup(M2B,GPIO.OUT)
GPIO.setup(PWM1,GPIO.OUT)
GPIO.setup(PWM2,GPIO.OUT)
GPIO.setup(SERVO,GPIO.OUT)
GPIO.setup(ENC1A,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENC1B,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENC2A,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ENC2B,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configuración de PWM de Motores y 
pwm1 = GPIO.PWM(PWM1, 100)
pwm2 = GPIO.PWM(PWM2, 100)
pwm_servo = GPIO.PWM(SERVO, 50)
max_pwm = 100
pwm1_value=0
pwm2_value=0
cont1 = 0
cont2 = 0
cont3 = 0
cont4 = 0
last = GPIO.input(ENC1A)
while cont2 < 10000:
    now = GPIO.input(ENC1A)

    if now != last:
        cont1 += 1
    else:
        cont1 += 0
    last = now
    cont2 += 1
    
print(cont1)       
    
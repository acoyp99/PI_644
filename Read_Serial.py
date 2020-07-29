from tkinter import *
import time
import os
import serial

ser = serial.Serial('/dev/ttyUSB0',57600)
while True:
    r_s=ser.readline()
    t_r_s = r_s.decode()
    t_r_s = t_r_s.split()
    for i in range(0, len(t_r_s)):
        t_r_s[i] = int(t_r_s[i])
        
    print(t_r_s)

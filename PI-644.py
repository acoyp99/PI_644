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
GPIO.setup(ENC1A,GPIO.IN)
GPIO.setup(ENC1B,GPIO.IN)
GPIO.setup(ENC2A,GPIO.IN)
GPIO.setup(ENC2B,GPIO.IN)

# Configuración de PWM de Motores y 
pwm1 = GPIO.PWM(PWM1, 100)
pwm2 = GPIO.PWM(PWM2, 100)
pwm_servo = GPIO.PWM(SERVO, 50)
max_pwm = 100
pwm1_value=0
pwm2_value=0

def motor_atras(pwm1_value,pwm2_value):
    GPIO.output(M1A , False)
    GPIO.output(M1B , True)
    GPIO.output(M2A , True)
    GPIO.output(M2B , False)
    pwm1.start(pwm1_value)
    pwm2.start(pwm2_value)

def motor_adelante(pwm1_value,pwm2_value):
    GPIO.output(M1A , True)
    GPIO.output(M1B , False)
    GPIO.output(M2A , False)
    GPIO.output(M2B , True)
    pwm1.start(pwm1_value)
    pwm2.start(pwm2_value)

def motor_izquierda(pwm1_value,pwm2_value):
    GPIO.output(M1A , False)
    GPIO.output(M1B , True)
    GPIO.output(M2A , False)
    GPIO.output(M2B , True)
    pwm1.start(pwm1_value)
    pwm2.start(pwm2_value)

def motor_derecha(pwm1_value,pwm2_value):
    GPIO.output(M1A , True)
    GPIO.output(M1B , False)
    GPIO.output(M2A , True)
    GPIO.output(M2B , False)
    pwm1.start(pwm1_value)
    pwm2.start(pwm2_value)
    
def motor_stop():
    GPIO.output(M1A , False)
    GPIO.output(M1B , False)
    GPIO.output(M2A , False)
    GPIO.output(M2B , False)

def control_manual():
    print('HOLA')

def lin_bor():
    global data
    global time1
    data = []
    time1 = []
    t_r_s = []
    cont = 0
    pwmA=0
    pwmB=0
    ser = serial.Serial('/dev/ttyUSB0',57600)
    pwm_servo.start(3)
    while True:
        r_s=ser.readline()
        t_r_s = r_s.decode()
        t_r_s = t_r_s.split()
        for i in range(0, len(t_r_s)):
            t_r_s[i] = int(t_r_s[i])
        
        if t_r_s[0]<20:
            break
        if len(t_r_s)>6:
            if t_r_s[9]==0:
                break
    
        elif len(t_r_s)>3:
            start = time.time()
            Err = 30 - t_r_s[3]
            Err2 = 30 - t_r_s[4]
            if Err > 0:
                pwmA = max_pwm
                pwmB = int(abs(max_pwm/Err))
            elif Err < 0:
                pwmA = int(abs(max_pwm/Err))
                pwmB = max_pwm
            else:
                pwmA = max_pwm
                pwmB = max_pwm
            data.append(pwmA)
            data.append(pwmB)
            time1.append(time.time()-start)
            motor_adelante(pwmA,pwmB)
            pwm_servo.ChangeDutyCycle(6)
            cont += 1
            
    
    motor_stop()  
    pwm_servo.ChangeDutyCycle(3)
    time.sleep(1)
    pwm_servo.stop()
    print(len(time1),len(data))           

def lin_carr():
    cont = 0
    cont_time = 0
    pwmA=0
    pwmB=0
    ser = serial.Serial('/dev/ttyUSB0',57600)
    pwm_servo.start(3)
    while cont<len(data):
        r_s=ser.readline()
        t_r_s = r_s.decode()
        t_r_s = t_r_s.split()
        for i in range(0, len(t_r_s)):
            t_r_s[i] = int(t_r_s[i])
        
        if t_r_s[0]<20:
            break
        if len(t_r_s)>6:
            if t_r_s[9]==0:
                break
    
        elif len(t_r_s)>3:
            pwmA = data[cont]
            cont+=1
            pwmB = data[cont]
            motor_adelante(pwmA,pwmB)
            pwm_servo.ChangeDutyCycle(6)
            cont += 1
            time.sleep(time1[cont_time])
            cont_time += 1
            
    
    motor_stop()  
    pwm_servo.ChangeDutyCycle(3)
    time.sleep(1)
    pwm_servo.stop()
    print(len(time1),len(data))           

def giro_derecha():
    ser = serial.Serial('/dev/ttyUSB0',57600)
    pwm_giro = int(max_pwm/2)
    while True:
        r_s=ser.readline()
        t_r_s = r_s.decode()
        t_r_s = t_r_s.split()
        for i in range(0, len(t_r_s)):
            t_r_s[i] = int(t_r_s[i])
            
        if len(t_r_s) > 3:
            if t_r_s[3] > 70 or t_r_s[1] > 70:
                if t_r_s[3] - t_r_s[1]:
                    motor_derecha(pwm_giro,pwm_giro)
                else:
                    motor_izquierda(pwm_giro,pwm_giro)      
            elif t_r_s[2]<20:
                break
            else:
                motor_stop()

def anden_paralelo():
    t_r_s = []
    ser = serial.Serial('/dev/ttyUSB0',57600)
    pwm_giro = int(max_pwm/2)
    while True:
        r_s=ser.readline()
        t_r_s = r_s.decode()
        t_r_s = t_r_s.split()
        for i in range(0, len(t_r_s)):
            t_r_s[i] = int(t_r_s[i])
        if t_r_s[0] < t_r_s[2]:
            motor_derecha(max_pwm,int(max_pwm/3))
        elif t_r_s[4]<30:
            motor_stop()
            break
        
def anden_perp():
    t_r_s = []
    ser = serial.Serial('/dev/ttyUSB0',57600)
    pwm_giro = int(max_pwm/2)
    cont = 0
    ref = 0
    while True:
        r_s=ser.readline()
        t_r_s = r_s.decode()
        t_r_s = t_r_s.split()
        for i in range(0, len(t_r_s)):
            t_r_s[i] = int(t_r_s[i])
        if cont < 1:
            ref = t_r_s[4]
            
        cont += 1
        if t_r_s[2]<ref:
            motor_stop()
            break
        else:
            motor_derecha(max_pwm,int(max_pwm)) 
            
#         if len(t_r_s) > 3 and t_r_s[1]>70:
#             if t_r_s[0]<30 and t_r_s[2]>30:
#                 motor_derecha(max_pwm,max_pwm)
#             else:
#                 motor_stop()
#                 break
#             
            

def quit1():
    app.destroy()

LARGE_FONT= ("Verdana", 14)
m_font = ("Verdana", 10)
spin_font = ("Verdana", 16)


class SeaofBTCapp(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Login, Options, dem_auto, dem_man, sum_pc):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="¡Bienvenido usuario!", font=LARGE_FONT)
        label.pack()
        
        bottomframe = Frame(self)
        bottomframe.pack( side = BOTTOM )

        button = Button(self, text="Acceder al robot", width=30, height=5, font=m_font, relief="raised", borderwidth=5, command=lambda: controller.show_frame(Login))
        button.pack()
        
        button = Button(bottomframe, text="Salir", height=2, font=m_font, relief="raised", borderwidth=5, command=quit1)
        button.pack()
        
        label = Label(bottomframe, text="PI-644 v1.0", font=m_font)
        label.pack()

class Login(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        # Función de validar acceso
        def validateLogin():
            if username.get() == 'admin':
                if password.get() == 'psswd':
                    controller.show_frame(Options)    
                else:
                    print("Contraseña incorrecta")         
            else:
                print("Usuario incorrecto")   
        
        #Top Frame
        topframe = Frame(self)
        topframe.pack( side = TOP )
        #Bottom Frame
        bottomframe = Frame(self)
        bottomframe.pack( side = BOTTOM )
        
        label = Label(topframe, text="Ingreso de usuario", font=LARGE_FONT)
        label.pack(expand=True)
        
        # Opciones de usuario
        L1 = Label(topframe, text="Nombre de usuario", font=m_font)
        L1.pack(expand=True)
        username = StringVar(self)
        o_u = ["Admin", "Administrator", "admin", "admin01"]
        username.set(o_u[0])
        combo_U = OptionMenu(topframe, username, *o_u)
        combo_U.pack(expand=True) 
        
        # Opciones de contraseña
        L2 = Label(topframe, text="Contraseña de acceso", font=m_font)
        L2.pack(expand=True)
        password = StringVar(self)
        o_p = ["pass", "passwd", "password", "psswd"]
        password.set(o_p[0])
        combo_U = OptionMenu(topframe, password, *o_p)
        combo_U.pack(expand=True) 
        
        # Boton de validación de acceso
        button2 = Button(topframe, text="Validar", font=m_font, relief="raised", borderwidth=5, width=15, command=validateLogin)
        button2.pack(expand=True)
        
        # Boton para retroceder
        button1 = Button(bottomframe, text="Atrás", relief="raised", borderwidth=5, command=lambda: controller.show_frame(StartPage))
        button1.pack()

class Options(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Opciones", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        bottomframe = Frame(self)
        bottomframe.pack( side = BOTTOM )

        button1 = Button(bottomframe, text="Atrás", relief="raised", borderwidth=5, command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = Button(self, text="Demarcado automático", relief="raised", borderwidth=5, width=25, height=2, font=m_font, command=lambda: controller.show_frame(dem_auto))
        button2.pack()
        
        button2 = Button(self, text="Demarcado manual",
                         relief="raised",
                         borderwidth=5, width=25,
                         height=2, font=m_font,
                         command=control_manual)
        button2.pack()
        
        button2 = Button(self, text="Estadísticas", relief="raised", borderwidth=5, width=25, height=2, font=m_font, command=lambda: controller.show_frame(sum_pc))
        button2.pack()

class sum_pc(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        #Top Frame
        topframe = Frame(self)
        topframe.pack( side = TOP )
        topframe1 = Frame(topframe)
        topframe1.pack( side = TOP )
        topframe2 = Frame(topframe1)
        topframe2.pack( side = TOP )
        #Bottom Frame
        bottomframe = Frame(self)
        bottomframe.pack( side = BOTTOM )
        
        def actualizar_pintura():
            text1 = "Cantidad de pintura: " + spin1.get() + "%"
            label1.configure(text=text1)
            
        def actualizar_generador():
            text2 = "Carga generador: " + spin2.get() + "%"
            label2.configure(text=text2)
        
        label = Label(topframe2, text="Estadísticas", font=LARGE_FONT)
        label.pack()
        
        label = Label(topframe2, text="Suministro de pintura y energía", font=m_font)
        label.pack(fill = BOTH, expand = True)
        
        spin1 = Spinbox(topframe1, from_=0, to=100, font=spin_font, width=8)
        spin1.pack(fill = BOTH,side=LEFT)
        bt_pi = Button(topframe1, text="Actualizar % pintura", font=m_font, command=actualizar_pintura)
        bt_pi.pack(fill = BOTH, expand = True, side=LEFT)
        spin2 = Spinbox(topframe, from_=0, to=100, font=spin_font, width=8, command=actualizar_generador)
        spin2.pack(fill = BOTH,side=LEFT)
        bt_en = Button(topframe, text="Actualizar % de energía", font=m_font)
        bt_en.pack(fill = BOTH, expand = True, side=LEFT)
        
        label = Label(self, text="Control remoto: OK", font=m_font)
        label.pack(fill = BOTH, expand = True)
        label1 = Label(self, text="Cantidad de pintura: --", borderwidth=2, relief="sunken", font=m_font)
        label1.pack(expand = True, fill=BOTH)
        label2 = Label(self, text="Carga generador: --", borderwidth=2, relief="sunken", font=m_font)
        label2.pack(fill = BOTH, expand = True)
        label3 = Label(self, text="Estado de los sensores: OK", borderwidth=2, relief="sunken", font=m_font)
        label3.pack(fill = BOTH, expand = True)
        label4 = Label(self, text="Reposo del compresor: 60 minutos", borderwidth=2, relief="sunken", font=m_font)
        label4.pack(fill = BOTH, expand = True)
        
        button1 = Button(bottomframe, text="Atras", font=m_font, relief="raised", borderwidth=5, command=lambda: controller.show_frame(Options))
        button1.pack(expand = True)
        
class dem_man(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        #Top Frame
        topframe = Frame(self)

        
class dem_auto(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Demarcado automático", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        # Función de testeo
        def test1():
            motor_adelante(50,50)
            time.sleep(0.5)
            motor_atras(50,50)
            time.sleep(0.5)
            motor_stop()
        
            
        # Función general
        def func():
            if type_dem.get() == 'Medición del anden':
                print ('Medición')
            elif type_dem.get() == 'Medicion de la via':
                print ('LIN')
            elif type_dem.get() == 'Linea de borde de pavimento':
                time.sleep(3)
                lin_bor()
                time.sleep(3)
                giro_derecha()
            elif type_dem.get() == 'Lineas discontinuas':
                time.sleep(2)
                anden_perp()
            elif type_dem.get() == 'Lineas de estacionamiento':
                time.sleep(2)
                anden_paralelo()
            elif type_dem.get() == 'Linea de carril':
                time.sleep(2)
                lin_carr()
            elif type_dem.get() == 'Trazado completo':
                time.sleep(2)
                anden_paralelo()
        
        topframe = Frame(self)
        topframe.pack( side = TOP )
        topframe1 = Frame(topframe)
        topframe1.pack( side = TOP )
        topframe2 = Frame(topframe1)
        topframe2.pack( side = TOP )
        topframe3 = Frame(topframe2)
        topframe3.pack( side = TOP )
        
        bottomframe = Frame(self)
        bottomframe.pack( side = BOTTOM )
        bottomframe1 = Frame(bottomframe)
        bottomframe1.pack( side = BOTTOM )

        button2 = Button(topframe3, text="Test del demarcador", relief="raised", borderwidth=5, width=20, height=2, state=NORMAL, command=test1)
        button2.pack()
        
        L1 = Label(topframe3, text="Configuración de demarcado", font=m_font)
        L1.pack()
        type_dem = StringVar(self)
        o_u = ["Medición del anden", "Medicion de la via", "Linea de borde de pavimento",
               "Lineas discontinuas", "Lineas de estacionamiento", "Linea de carril", "Trazado completo"]
        type_dem.set(o_u[0])
        combo_U = OptionMenu(topframe3, type_dem, *o_u)
        combo_U.pack() 
        
        L2 = Label(topframe2, text="Distancia", width=15)
        L2.pack(side=LEFT)
        L3 = Label(topframe2, text="No Estacionamientos", width=15)
        L3.pack(side=LEFT)
        
        spin1 = Spinbox(topframe1, from_=0, to=100, font=spin_font, width=8)
        spin1.pack(side=LEFT)
        spin2 = Spinbox(topframe1, from_=0, to=100, font=spin_font, width=8)
        spin2.pack(side=LEFT)
        
        button2 = Button(topframe, text="Iniciar demarcado", relief="raised", borderwidth=5, width=20, height=2, state=NORMAL, command=func)
        button2.pack()
        
        L4 = Label(bottomframe, text="Proceso en curso...", width=15)
        L4.pack(side=LEFT)
        L4 = Label(bottomframe, text="86%...", width=10)
        L4.pack(side=LEFT)
        L4 = Label(bottomframe, text="Estado: OK", width=13)
        L4.pack(side=LEFT)
        
        button1 = Button(bottomframe1, text="Atras", relief="raised", borderwidth=5, state=NORMAL, command=lambda: controller.show_frame(Options))
        button1.pack()

app = SeaofBTCapp()
full = '460x300'
app.attributes("-fullscreen", True)
app.title("Demarcador vial")
app.mainloop()
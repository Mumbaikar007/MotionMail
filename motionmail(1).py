#imports
import RPi.GPIO as GPIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from picamera import PiCamera
import time

#Pi board setups
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from PIR motion sensor

#camera initials
camera=PiCamera()
camera.rotation=180

# smtp gmail

# receiver's mail
to = "" 

# sender's mail
user = ""
password = "kossine123"


#smtp server setup ...
smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo()
smtpserver.login ( user, password)


msg = MIMEMultipart()

msg['To']=to
msg['From']=user
msg['Subject']='IOT'

msg.attach(MIMEText("Hello"))

#ultrasonic
prev=0
current=0
i = 0

#GPIO.setup(3, GPIO.OUT)         #LED output pin
while True:
    prev = i 
    i=GPIO.input(7)
    if i==0:                 #When output from motion sensor is LOW
        print ("No intruders")
        #GPIO.output(3, 0)  #Turn OFF LED
        time.sleep(0.1)
            
    elif i==1:               #When output from motion sensor is HIGH
        print ("Intruder detected")
        #GPIO.output(3, 1)  #Turn ON LED
        time.sleep(0.1)
        if ( prev != i ):
            print("M")   
            
            #camera
            camera.start_preview()
            time.sleep(3)
            camera.capture('/home/pi/Desktop/image.jpg')
            camera.stop_preview()

            #mail
            fp=open('/home/pi/Desktop/image.jpg','rb')
            msg.attach(MIMEImage(fp.read()))

            smtpserver.sendmail ( user, to , msg.as_string())

            #smtpserver.close()

            print("mailed !!")


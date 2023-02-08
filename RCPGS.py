import socket
import pygame
import RPi.GPIO as GPIO

pygame.init()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(1)

conn, addr = server_socket.accept()
print('Connected by', addr)

GPIO.setwarnings(False)
servoPin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

pwm = GPIO.PWM(servoPin, 50)
pwm.start(7.5)

clock = pygame.time.Clock()

while True:
    data = conn.recv(1024)
    print(data)
    #steer = data.decode()
    #steeringVal = steer.split(".")
    #steering = float(steeringVal[0])
    #mSteering = (steering + 1) * 45
    #print(mSteering)
    #pwm.ChangeDutyCycle(mSteering / 18 + 2.5)
    clock.tick(240)

conn.close()
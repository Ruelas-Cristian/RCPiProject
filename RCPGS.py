import socket
import pygame
import pygame.camera
import pygame.image
import struct
import RPi.GPIO as GPIO

pygame.init()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(1)

conn, addr = server_socket.accept()
print('Connected by', addr)

#setting up servo
GPIO.setwarnings(False)
servoPin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

#powering servo
pwm = GPIO.PWM(servoPin, 50)
pwm.start(7.5)

#camera stuff
clock = pygame.time.Clock()
pygame.camera.init()
camera = pygame.camera.Camera("/dev/video0", (640, 480))
camera.start()

while True:
    #broadcast
    image = camera.get_image()
    sendImage = pygame.image.tostring(image, "RGB")
    conn.sendall(sendImage)

    data = conn.recv(8)
    steering, gas, brake = struct.unpack('!fff', data)
    print('Steering: ', steering)
    print('Gas: ', gas)
    print('Brake: ', brake)
    #steeringVal = steer.split(".")
    #steering = float(steeringVal[0])
    #mSteering = (steering + 1) * 45
    #print(mSteering)
    #pwm.ChangeDutyCycle(mSteering / 18 + 2.5)
    
    clock.tick(60)

camera.stop()
pygame.camera.quit()
conn.close()
import sys
#import RPi.GPIO as GPIO
import pygame
import socket
import time

from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((1000, 1000), 0, 32)
screen.fill((0, 0, 0))

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect(('RaspberryPi IP', 8080))

clock = pygame.time.Clock()

pygame.joystick.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for controller in controllers:
    print(controller.get_name())
    #take notes of controller


#Gauges
class gauge:
    def __init__(pedal, x, y, w, h, color, back):
        pedal.x = x
        pedal.y = y
        pedal.w = w
        pedal.h = h
        pedal.color = color
        pedal.back = back

gasGauge = gauge(900, 800, 50, 200, (0, 255, 0), (0, 0, 0))
brakeGauge = gauge(800, 800, 50, 200, (255, 0, 0), (0, 0, 0))
#Maybe when we get the 1/10th scale in the future :(
#clutchGauge = gauge(700, 800, 50, 200, (0, 0, 255), (0, 0, 0))

gasPedal = 0
brakePedal = 0
clutchPedal = 0

while True:
    if controller.get_name() == 'FANATEC Wheel' :
        #note of controls
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #steering wheel axis is (0), left corresponds to -1, and right corresponds to 1
                steeringAxis = controller.get_axis(0)
                time.sleep(.005)
                mappingSteering = (steeringAxis + 1) * 45
                print(mappingSteering)
                #change the servo position like this
                sendSteer = str(mappingSteering).encode()
                clientSock.sendall(sendSteer)

                #Acceleration pedal (1), brake pedal (4), clutch pedal (5) all go from -1 (idle) to 1 (pressed all the way)
                gasPedal = controller.get_axis(1)
                mappingGas = 1 - ((gasPedal + 1) / 2)
                
                brakePedal = controller.get_axis(4)
                mappingBrake = 1 - ((brakePedal + 1) / 2)
                
                #Maybe when we get the 1/10th scale in the future :(
                #clutchPedal = controller.get_axis(5)
                #mappingClutch = 1 - ((clutchPedal + 1) / 2)
                
                #Displaying pedals
                gasFill = mappingGas * gasGauge.h
                pygame.draw.rect(screen, gasGauge.back, (gasGauge.x, gasGauge.y, gasGauge.w, gasGauge.h))
                pygame.draw.rect(screen, gasGauge.color, (gasGauge.x, gasGauge.y + (gasGauge.h - gasFill), gasGauge.w, gasFill))
                
                brakeFill = mappingBrake * brakeGauge.h
                pygame.draw.rect(screen, brakeGauge.back, (brakeGauge.x, brakeGauge.y, brakeGauge.w, brakeGauge.h))
                pygame.draw.rect(screen, brakeGauge.color, (brakeGauge.x, brakeGauge.y + (brakeGauge.h - brakeFill), brakeGauge.w, brakeFill))
                
                #Maybe when we get the 1/10th scale in the future :(
                #clutchFill = mappingClutch * clutchGauge.h
                #pygame.draw.rect(screen, clutchGauge.back, (clutchGauge.x, clutchGauge.y, clutchGauge.w, clutchGauge.h))
                #pygame.draw.rect(screen, clutchGauge.color, (clutchGauge.x, clutchGauge.y + (clutchGauge.h - clutchFill), clutchGauge.w, clutchFill))

                #maybe we can control servos here for camera
                #joystick x axis (2), left corresponds to 1, right corresponds to -1
                #y axis (3), up corresponds to -1, down corresponds to 1
                wheelJoyX = controller.get_axis(2)
                wheelJoyY = controller.get_axis(3)
                invX = wheelJoyX * - 1
                invY = wheelJoyY * - 1

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()            

    elif controller.get_name() == 'Controller (Xbox One For Windows)':
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #Left thumbstick axis is (0), left corresponds to -1, and right corresponds to 1
                steeringAxis = controller.get_axis(0)
                mappingSteering = (steeringAxis + 1) * 45
                sendSteer = "{:.6f}".format(str(mappingSteering).encode())
                clientSock.sendall(sendSteer)
                #change the servo position like this

                #Left trigger is (4), Right trigger is (5): both going from -1 to 1
                gasPedal = controller.get_axis(5)
                mappingGas = ((gasPedal + 1) / 2)
                
                brakePedal = controller.get_axis(4)
                mappingBrake = ((brakePedal + 1) / 2)

                #Displaying Pedals
                gasFill = mappingGas * gasGauge.h
                pygame.draw.rect(screen, gasGauge.back, (gasGauge.x, gasGauge.y, gasGauge.w, gasGauge.h))
                pygame.draw.rect(screen, gasGauge.color, (gasGauge.x, gasGauge.y + (gasGauge.h - gasFill), gasGauge.w, gasFill))
                
                brakeFill = mappingBrake * brakeGauge.h
                pygame.draw.rect(screen, brakeGauge.back, (brakeGauge.x, brakeGauge.y, brakeGauge.w, brakeGauge.h))
                pygame.draw.rect(screen, brakeGauge.color, (brakeGauge.x, brakeGauge.y + (brakeGauge.h - brakeFill), brakeGauge.w, brakeFill))

                #maybe control for camera
                wheelJoyX = controller.get_axis(2)
                wheelJoyY = controller.get_axis(3)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
    
    elif controller.get_name() == 'PS4 Controller':
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                #Left thumbstick axis is (0), left corresponds to -1, and right corresponds to 1
                steeringAxis = controller.get_axis(0)
                mappingSteering = (steeringAxis + 1) * 45
                sendSteer = float(mappingSteering)
                clientSock.send(str(sendSteer).encode())
                #change the servo position like this

                #Left trigger is (4), Right trigger is (5): both going from -1 to 1
                gasPedal = controller.get_axis(5)
                mappingGas = ((gasPedal + 1) / 2)
                
                brakePedal = controller.get_axis(4)
                mappingBrake = ((brakePedal + 1) / 2)

                #Displaying Pedals
                gasFill = mappingGas * gasGauge.h
                pygame.draw.rect(screen, gasGauge.back, (gasGauge.x, gasGauge.y, gasGauge.w, gasGauge.h))
                pygame.draw.rect(screen, gasGauge.color, (gasGauge.x, gasGauge.y + (gasGauge.h - gasFill), gasGauge.w, gasFill))
                
                brakeFill = mappingBrake * brakeGauge.h
                pygame.draw.rect(screen, brakeGauge.back, (brakeGauge.x, brakeGauge.y, brakeGauge.w, brakeGauge.h))
                pygame.draw.rect(screen, brakeGauge.color, (brakeGauge.x, brakeGauge.y + (brakeGauge.h - brakeFill), brakeGauge.w, brakeFill))

                #maybe control for camera
                wheelJoyX = controller.get_axis(2)
                wheelJoyY = controller.get_axis(3)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()  


    pygame.display.update()
    clock.tick(30)
    clientSock.close
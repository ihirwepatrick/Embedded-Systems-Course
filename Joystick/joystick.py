import pygame
import sys
import serial
import time
pygame.init()
window_size = (640, 480)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Joystick Controlled Avatar')
WHITE = (255, 220, 25)
RED = (255, 0, 0)
circle_radius = 30
circle_color = RED
circle_position = [window_size[0] // 2, window_size[1] // 2]
clock = pygame.time.Clock()
arduino = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            arduino.close()
            pygame.quit()
            sys.exit()
    try:
        data = arduino.readline().decode('utf-8').strip()
        if data:
            x_str, y_str = data.split(",")
            x = int(x_str)
            y = int(y_str)
            print("X: " + x_str + "Y: " + y_str)
            if x < 400:
                circle_position[0] -= 5
            elif x > 600:
                circle_position[0] += 5
            if y < 400:
                circle_position[1] -= 5
            elif y > 600:
                circle_position[1] += 5
    except Exception as e:
        print(f"Error: {e}")
    window.fill(WHITE)
    pygame.draw.circle(window, circle_color, circle_position, circle_radius)
    pygame.display.flip()
    clock.tick(30)
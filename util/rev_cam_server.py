import socket
import sys
import pygame
from PIL import Image



pygame.init()
screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption('Remote Webcam Viewer')
font = pygame.font.SysFont("Arial",14)
clock = pygame.time.Clock()
timer = 0
previousImage = ""
image = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8000))
s.listen(5)

while True:
    try:
        if timer < 1:
            connection, addr = s.accept()

            received = []

            while True:
                data = connection.recv(4096)

                if not data:
                    break
                else:
                    received.append(data)

        dataset = b''.join(received)

        image = pygame.image.fromstring(dataset, (640, 480), 'RGB')

        screen.blit(image, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    except:
        pygame.quit()
        sys.exit()



        




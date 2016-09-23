from plugins import Plugin, Command
import glob
from threading import Thread
import pygame
import pygame.camera

import socket

class Main(Plugin):

    name = 'Camera'
    version = '1.0.0'

    def setup(self):
        
        pygame.init()
        pygame.camera.init()
        
        c = Command('/cam_stream', usage='HOSTNAME /cam_stream <host> <port> <id> - stream webcam to remote host')
        self.add_command(c)

        c = Command('/cam_stream_stop', usage='HOSTNAME /cam_stream_stop - stop webcam streaming')
        self.add_command(c)

        c = Command('/cameras', usage='HOSTNAME /cameras - list cameras by ID number')
        self.add_command(c)

        c = Command('/snapshot', usage='HOSTNAME /snapshot <id> - take a picture from the camera #<id>')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/cam_stream':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_cam_stream, args=tuple(arg_list))
            t.start()

        if command == '/cam_stream_stop':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_cam_stream_stop)
            t.start()

        if command == '/cameras':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_cameras, args=tuple(arg_list))
            t.start()
        if command == '/snapshot':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_snapshot, args=tuple(arg_list))
            t.start()

    def handle_cameras(self, chat_id):
        try:
            cameras = ['Camera ID: {}'.format(x) for x in pygame.camera.list_cameras()]

            return self.bot.send_message(chat_id, '\n'.join(cameras))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


    def handle_snapshot(self, chat_id, cam_id):
        self.bot.send_message(chat_id, 'Taking a picture!')
        fname = self.bot.get_tmp(self.bot.generate_file_name('snapshot.png'))
        try:
            self.cam = pygame.camera.Camera(cam_id, (640,480))
            self.cam.start()
            image = self.cam.get_image()
            self.cam.stop()
            pygame.image.save(image, fname)

            f = open(fname, 'rb')

            self.bot.bot.sendPhoto(chat_id, f)

            f.close()

        except Exception as e:
            self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_cam_stream_stop(self):
        self.stop = True

    def handle_cam_stream(self, chat_id, host, port, cam_id):
        try:
            self.cam = pygame.camera.Camera(cam_id, (640, 480))
            self.cam.start()

            self.stop = False

            self.bot.send_message(chat_id, 'Webcam Streaming started, sending {} data to server {}:{}'.format(cam_id, host, port))

            while not self.stop:
                s = socket.socket()
                s.connect((host, int(port)))
                
                image = self.cam.get_image()

                data = pygame.image.tostring(image, 'RGB')

                s.sendall(data)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

            self.cam.stop()
            return self.bot.send_message(chat_id, 'Webcam Streaming stopped')

        except Exception as e:
            self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

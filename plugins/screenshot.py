from plugins import Plugin, Command

from threading import Thread

import os
from time import sleep
import pyscreenshot as ImageGrab

class Main(Plugin):

    name = 'Screenshot'
    version = '1.0.0'
    
    def setup(self):
        
        c = Command('/screenshot', usage='HOSTNAME /screenshot [delay] - takes a screenshot with an option [delay], in seconds')
        self.add_command(c)
        

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/screenshot':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_screenshot, args=tuple(arg_list))
            t.start()

    def handle_screenshot(self, chat_id, delay=None):
        try:
            fname = self.bot.get_tmp(self.bot.generate_file_name('screenshot.png'))

            if delay:
                self.bot.send_message(chat_id, 'Will take screenshot after {} seconds'.format(delay))
                sleep(int(delay))
            else:
                self.bot.send_message(chat_id, 'Taking screenshot...')

            ImageGrab.grab().save(fname, "PNG")
            f = open(fname, 'rb')
            self.bot.bot.sendPhoto(chat_id, f)
            f.close()
            os.remove(fname)
            return
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

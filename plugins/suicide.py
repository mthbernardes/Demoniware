from plugins import Plugin, Command

from threading import Thread

import os
import random
from time import sleep

class Main(Plugin):

    name = 'Suicide'
    version = '1.0.0'
    
    def setup(self):

        self.quotes = ['Give me my robe, put on my crown', 'I am dying, Egypt, dying', 'O happy dagger!', 'O true apothecary!', 'One that loved not wisely but too well', 'To be, or not to be', 'To sleep, perchance to dream', 'Tomorrow, and tomorrow, and tomorrow']
        
        c = Command('/suicide', usage='HOSTNAME /suicide [delay] - commit suicide with an option [delay], in seconds')
        self.add_command(c)
        

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/suicide':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_suicide, args=tuple(arg_list))
            t.start()

    def handle_suicide(self, chat_id, delay=None):
        try:
            self.bot.send_message(chat_id, random.choice(self.quotes))
            sleep(5)
            os._exit(0)
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

from plugins import Plugin, Command

from threading import Thread


class Main(Plugin):

    name = 'Download & Upload'
    version = '1.0.0'
    
    def setup(self):
        
        c = Command('/upload', usage='HOSTNAME /upload <file> - upload <file> to Telegram')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/upload':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_upload, args=tuple(arg_list))
            t.start()


    def handle_upload(self, chat_id, fname):
        try:
            f = open(fname, 'rb')
            return self.bot.bot.sendDocument(chat_id, f)
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


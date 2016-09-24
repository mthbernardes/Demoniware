from plugins import Plugin, Command

from threading import Thread
import glob
from zipfile import ZipFile
from telepot.exception import TelegramError


class Main(Plugin):

    name = 'Download & Upload'
    version = '1.0.0'
    
    def setup(self):
        
        c = Command('/upload', usage='HOSTNAME /upload <file> - upload <file> to Telegram')
        self.add_command(c)

        c = Command('/mass_upload', usage='HOSTNAME /mass_upload <pattern> - upload all files matching <pattern> to Telegram')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/upload':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_upload, args=tuple(arg_list))
            t.start()
        elif command == '/mass_upload':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_mass_upload, args=tuple(arg_list))
            t.start()


    def handle_upload(self, chat_id, fname):
        try:
            f = open(fname, 'rb')
            return self.bot.bot.sendDocument(chat_id, f)
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_mass_upload(self, chat_id, pattern):
        try:
            files = glob.glob(pattern)
            if len(files) == 0:
                return self.bot.send_message(chat_id, 'Error: 0 files found matching pattern {}'.format(pattern))
            else:
                self.bot.send_message(chat_id, 'Found {} files matching pattern {}, starting upload...'.format(len(files), pattern))

                zname = self.bot.get_tmp(self.bot.generate_file_name('mass_upload.zip'))
                
                with ZipFile(zname, 'w') as z:
                    for fname in glob.glob(pattern):
                        try:
                            z.write(fname)
                        except:
                            continue

                with open(zname, 'rb') as f:
                    self.bot.bot.sendDocument(chat_id, f)

                return self.bot.send_message(chat_id, 'Upload finished for pattern {} !'.format(pattern))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


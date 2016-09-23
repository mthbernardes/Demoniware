from plugins import Plugin, Command

from threading import Thread

import os
import pyaudio
import wave

class Main(Plugin):

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

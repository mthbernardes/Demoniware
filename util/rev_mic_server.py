import pyaudio
import sys
import socket

from threading import Thread



FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

frames = []

def udpStream(CHUNK):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 12345))

    while True:
        try:
            soundData, addr = s.recvfrom(CHUNK * CHANNELS * 2)
            frames.append(soundData)
        except OSError:
            continue

    s.close()

def play(stream, CHUNK):
    BUFFER = 10
    while True:
        if len(frames) == BUFFER:
            while True:
                stream.write(frames.pop(0), CHUNK)


if __name__ == "__main__":
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )

    Ts = Thread(target = udpStream, args=(CHUNK,))
    Tp = Thread(target = play, args=(stream, CHUNK,))
    Ts.setDaemon(True)
    Tp.setDaemon(True)
    Ts.start()
    Tp.start()
    Ts.join()
    Tp.join()

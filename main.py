import subprocess
import time
import pyaudio
import wave
import threading
import datetime

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3
stream = None
frames = []
recording = False
recordingThread = None
p = None


def startRecording():
    global recordingThread, recording, p
    print(f"Starting recording")
    p = pyaudio.PyAudio()
    recording = True
    recordingThread = threading.Thread(target=recordAudio)
    recordingThread.start()


def recordAudio():
    global frames, recording, p
    print("Recording thread started")
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    while recording:
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    print("Recording thread stopped")


def stopRecording():
    global frames, recording, p, recordingThread
    print(f"Stopping recording")
    recording = False
    recordingThread.join()
    p.terminate()
    wf = wave.open(getFilename(), 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    frames = []


def getFilename():
    return f"recording{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.wav"

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode('ISO-8859-1')
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


def awaitCalls():
    onCall = False
    while True:
        isThereProcess = process_exists("CallingShellApp.exe")
        time.sleep(0.5)

        if not isThereProcess == onCall and isThereProcess:
            startRecording()
            onCall = True
        if not isThereProcess == onCall:
            stopRecording()
            onCall = False
        print(f"onCall: {onCall}")



threads = []
x = threading.Thread(target=awaitCalls)
threads.append(x)
x.start()

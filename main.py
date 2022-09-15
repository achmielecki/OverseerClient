import os
import subprocess
import time
import pyaudio
import wave
import threading
import datetime
import requests
import json

import config
from views import loginView, registerView

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
sendFileQueue = []


def startClient():
    if not config.testmode:
        not_registered, email, password = loginView.Dialog().show()
    else:
        not_registered = False
        email = config.testemail
        password = config.testpass
    if not_registered:
        name, surname = registerView.Dialog().show()
        register(email, password, name, surname)
    return login(email, password)


def login(email, password):
    data = {'email': email, 'password': password}
    response = requests.post(config.apiUrl + "/login", data)
    if response.status_code != 200:
        raise RuntimeError()
    token = json.loads(response.content)["result"]
    return token


def register(email, password, name, surname):
    data = {'email': email, 'name': name, 'surname': surname, 'password': password}
    response = requests.post(config.apiUrl + "/register/", data)
    if response.status_code != 201:
        raise RuntimeError()
    return response


def awaitCalls():
    onCall = False
    while True:
        isThereProcess = processExists("CallingShellApp.exe")
        time.sleep(0.5)

        if not isThereProcess == onCall and isThereProcess:
            startRecording()
            onCall = True
        if not isThereProcess == onCall:
            stopRecording()
            onCall = False
        print(f"onCall: {onCall}")


def processExists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode('ISO-8859-1')
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


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
    global frames, recording, p, recordingThread, sendFileQueue
    print(f"Stopping recording")
    recording = False
    recordingThread.join()
    p.terminate()
    filename = getFilename()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    frames = []
    sendFileQueue.append(filename)


def getFilename():
    return f"recordings/recording{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.wav"


def sendFilesToApi():
    detectOldFilesToSend()
    while True:
        if isThereFileToSend():
            takeFirstFileAndSend()
        time.sleep(60)


def detectOldFilesToSend():
    global sendFileQueue
    sendFileQueue = ["recordings/" + it for it in os.listdir('./recordings')]


def isThereFileToSend():
    global sendFileQueue
    return len(sendFileQueue) > 0


def takeFirstFileAndSend():
    global sendFileQueue
    filename = sendFileQueue.pop()
    sendFileToApi(filename)


def sendFileToApi(filename):
    global token, sendFileQueue
    with open(filename, 'rb') as rec:
        response = requests.post(
            config.apiUrl + "/recordings/new_recording",
            params={'timestamp': getTimeFromFilename(filename)},
            files={'recording': rec},
            headers={'x-access-token': token})
    if response.status_code == 200: #TODO if unauthorized login again
        deleteRecording(filename)
    else:
        sendFileQueue.append(filename)


def getTimeFromFilename(filename):
    return filename[9:][:10] + "T" + filename[19:][:-4].replace("-", ":") + "Z"  # timestamp format Yyyy-mm-ddTHh:Mm:ssZ


def deleteRecording(filename):
    os.remove(filename)
    print(f"file deleted: {filename}")


token = startClient()
threads = []
x = threading.Thread(target=awaitCalls)
threads.append(x)
y = threading.Thread(target=sendFilesToApi)
y.start()
x.start()

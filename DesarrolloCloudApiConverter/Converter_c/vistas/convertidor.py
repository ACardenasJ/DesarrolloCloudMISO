# import required modules
from os import path
import subprocess
from vistas.vistas import VistaEnviarCorreo as email



class converter():
    email = email()
    #MP3 to WAV
    def mp3_wav(self):
        bashCommand = "ffmpeg -i kwest.mp3 -acodec pcm_u8 -ar 22050 ./sounds/KW.wav"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #MP3 to WMA
    def mp3_WMA(self):
        bashCommand = "ffmpeg -i kwest.mp3 ./sounds/KW.wma"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #WAV to MP3
    def wav_mp3(self):
        bashCommand = "ffmpeg -i kwest.wav -vn -ar 44100 -ac 2 -b:a 192k ./sounds/KW.mp3"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #WAV to WMA
    def wav_wma(self):
        bashCommand = "ffmpeg -i kwest.wav ./sounds/KW.wma"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #WMA to MP3
    def wma_mp3(self):
        bashCommand = "ffmpeg -i kwest.wma -f mp3 -ab 192 ./sounds/KW.mp3"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #WMA to WAV
    def WMA_WAV(self):
        bashCommand = "ffmpeg -i kwest.wma ./sounds/KW.wav"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #MP3 to AAC
    def mp3_acc(self):
        bashCommand = "ffmpeg  -i kwest.mp3 -c:a aac -vn ./sounds/KW.m4a"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #MP3 to OGG
    def mp3_ogg(self):
        bashCommand = " ffmpeg -y -i kwest.mp3  -strict -2 -acodec vorbis -ac 2 -aq 50 ./sounds/KW.ogg"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()







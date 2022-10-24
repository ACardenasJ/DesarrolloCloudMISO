# import required modules
from os import path
import subprocess
#from vistas.vistas import VistaEnviarCorreo as email

UPLOAD_DIRECTORY = "/usr/src/app/upfiles/"
PROCESS_DIRECTORY = "/usr/src/app/pofiles/"

class converter():
    #email = email()
    
    #MP3 to WAV
    def mp3_wav(self,file_name):
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".mp3 -acodec pcm_u8 -ar 22050 "+PROCESS_DIRECTORY+file_name+".wav"
        process = subprocess.Popen(bashCommand.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        print('SUBPROCESS ERROR: ' + str(error), flush=True)
        print('SUBPROCESS stdout: ' + str(output.decode()), flush=True)  

    #MP3 to WMA
    def mp3_WMA(self,file_name):
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".mp3 "+PROCESS_DIRECTORY+file_name+".wma"
        process = subprocess.Popen(bashCommand.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        print('SUBPROCESS ERROR: ' + str(error), flush=True)
        print('SUBPROCESS stdout: ' + str(output.decode()), flush=True)  

    #WAV to MP3
    def wav_mp3(self,file_name):
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".wav -vn -ar 44100 -ac 2 -b:a 192k "+PROCESS_DIRECTORY+file_name+".mp3"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #WAV to WMA
    def wav_wma(self,file_name):
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".wav "+PROCESS_DIRECTORY+file_name+".wma"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #WMA to MP3
    def wma_mp3(self,file_name):
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".wma -f mp3 -ab 192 "+PROCESS_DIRECTORY+file_name+".mp3"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #WMA to WAV
    def WMA_WAV(self,file_name):
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".wma "+PROCESS_DIRECTORY+file_name+".wav"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #MP3 to AAC
    def mp3_acc(self,file_name):
        bashCommand = "ffmpeg  -i "+UPLOAD_DIRECTORY+file_name+".mp3 -c:a aac -vn "+PROCESS_DIRECTORY+file_name+".m4a"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    #MP3 to OGG
    def mp3_ogg(self,file_name):
        bashCommand = " ffmpeg -y -i "+UPLOAD_DIRECTORY+file_name+".mp3  -strict -2 -acodec vorbis -ac 2 -aq 50 "+PROCESS_DIRECTORY+file_name+".ogg"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()







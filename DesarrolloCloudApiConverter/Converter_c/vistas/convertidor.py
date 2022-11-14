# import required modules
from os import path
import subprocess
#from vistas.vistas import VistaEnviarCorreo as email
import json
#from decouple import config
from urllib.request import urlopen
import requests
from flask import request
import os

import random
url = "https://storage.googleapis.com/bucket_music_file_storage_1/enviroments.json?rand_v="+str(random.randint(1,10000000))
response = urlopen(url)
data = json.loads(response.read())
BUCKET_URL = data['BUCKET_URL']
print(url,flush=True)
print(BUCKET_URL,flush=True)

UPLOAD_DIRECTORY = "./vistas/upfiles/"
PROCESS_DIRECTORY = "./vistas/pofiles/"
def descargador(file_name):
    url_bucket = 'http://{}/api/BucketUp/{}'.format(BUCKET_URL,file_name)
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    with requests.get(url_bucket, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)




def subir_archivo(file_name):
    url_bucket = 'http://{}/api/BucketPo/{}'.format(BUCKET_URL,file_name)
    file_path = os.path.join(PROCESS_DIRECTORY, file_name)
    files = {'file': open(file_path, 'rb')}
    requests.post(url_bucket, files=files)


class converter():
    #email = email()
    
    #MP3 to WAV
    def mp3_wav(self,file_name):
        #descargar archivo localmente
        descargador(file_name+".mp3")      
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".mp3 -acodec pcm_u8 -ar 22050 "+PROCESS_DIRECTORY+file_name+".wav"
        process = subprocess.Popen(bashCommand.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        print(output,flush=True)
        print(error,flush=True)
        subir_archivo(file_name+".wav")
        #guardar archivo en bucket
    #MP3 to WMA
    def mp3_WMA(self,file_name):
        bashCommand = "ffmpeg -i "+UPLOAD_DIRECTORY+file_name+".mp3 "+PROCESS_DIRECTORY+file_name+".wma"
        process = subprocess.Popen(bashCommand.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = process.communicate()
        print(output,flush=True)
        print(error,flush=True)
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
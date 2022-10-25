from flask_restful import Resource
from flask import request
from sqlalchemy import desc
from vistas.convertidor import converter as convertidor_
import smtplib, ssl
import requests

UPLOAD_DIRECTORY = "/usr/src/app/upfiles/"
PROCESS_DIRECTORY = "/usr/src/app/pofiles/"

class statusCheck(Resource):
    def get(self):
        return {'status': 'ok'}

class doTask(Resource):
    def post(self):
        taskInfo = request.get_json()
        print(taskInfo, flush=True)
        convertidor = convertidor_()
        file_name = taskInfo['file_name']    
        new_format = taskInfo['new_format']
        taskId = taskInfo['id_task']

        if ((file_name is not None) and (new_format is not None) and (taskId is not None)):
            origen_convert = file_name.split(".")[1]
            destino_convert = new_format.split(".")[1]
            file_name_ = file_name.split('.')[0]
            print(origen_convert, destino_convert, file_name_,flush=True)

            if((origen_convert == "mp3") and (destino_convert == "wav")):
                print("mp3 a wav", flush=True)
                convertidor.mp3_wav(file_name_)
            elif((origen_convert == "mp3") and (destino_convert == "wma")):
                print("mp3 a wma", flush=True)
                convertidor.mp3_WMA(file_name_)
            elif((origen_convert == "wav") and (destino_convert == "mp3")):
                print("wav a mp3")
                convertidor.wav_mp3(file_name_)
            elif((origen_convert == "wav") and (destino_convert == "wma")):
                print("wav a wma")
                convertidor.wav_wma(file_name_)
            elif((origen_convert == "wma") and (destino_convert == "mp3")):
                print("wma a mp3")
                convertidor.wma_mp3(file_name_)
            elif((origen_convert == "wma") and (destino_convert == "wav")):
                print("wma a wav")
                convertidor.WMA_WAV(file_name_)
            elif((origen_convert == "mp3") and (destino_convert == "acc")):
                print("mp3 a acc")
                convertidor.mp3_acc(file_name_)
            elif((origen_convert == "mp3") and (destino_convert == "ogg")):
                print("mp3 a ogg")
                convertidor.mp3_ogg(file_name_)
            else:
                print("no se puede convertir archivo")

            url_back = 'http://backend:5000/api/taskUpd/{}'.format(taskId)
            actualizar = requests.put(url_back)
            if(actualizar.status_code == 200):
                return {'status': 'ok'}, 200
            else:
                return {'status': 'error'}, 400
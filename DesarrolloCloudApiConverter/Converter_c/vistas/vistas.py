from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from vistas.convertidor import converter as convertidor_
import smtplib, ssl

UPLOAD_DIRECTORY = "/usr/src/app/upfiles/"
PROCESS_DIRECTORY = "/usr/src/app/pofiles/"

class statusCheck(Resource):
    def get(self):
        print("GET RECIBIDO")
        return {'status': 'ok'}

class doTask(Resource):
    def post(self):
        print("TAREA RECIBIDA", flush=True)
        taskInfo = request.get_json()
        print(taskInfo, flush=True)
        convertidor = convertidor_()
        file_name = taskInfo['file_name']    
        new_format = taskInfo['new_format']
        timestamp = taskInfo['timestamp']
        status = taskInfo['status']
        taskId = taskInfo['taskId']
        email = taskInfo['email']
        # data = {'file_name' : file_name, 
        #             'new_format' : new_format, 
        #             'timestamp' : timestamp,
        #             'status' : status, 
        #             'id_usuario': usuario.id,
        #             'email': usuario.email}        
        # palabra = line.split(',')
        # file_name = palabra[0].split(":")[1]
        # new_format = palabra[1].split(":")[1] 
        # timestamp = palabra[2].split(":")[1]
        #status = palabra[3].split(":")[1]
        #taskId = palabra[4].split(":")[1]


        if file_name is not None and new_format is not None and timestamp is not None and status is not None and taskId is not None and email is not None:
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

            #   ENVIAR CORREO
            #VistaEnviarCorreo.enviar_correo(self,email)
            return {'status': 'ok'}, 200
        else:
            return {'status': 'error'}, 400
    
        

class VistaEnviarCorreo(Resource):

    def enviar_correo(self, sender_email):
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "acj8991@gmail.com"
        receiver_email = sender_email
        password = "1213456"
        message = """\
        Subject: Hi there

        Su archivo fue realizado exitosamante."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

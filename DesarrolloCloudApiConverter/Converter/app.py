from Converter import create_app
from markupsafe import escape
from flask_restful import Api
from convertidor import converter as convertidor

app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)

file_path_redis = "./Backend/vistas/programar_task.txt"

class Converter(self):

    def convertir(self):
        convertidor = convertidor()
        with open(file_path_redis) as archivo:
            lines_of_tasks = archivo.readlines()
            print(ine_of_task)

            for line in lines_of_tasks:
                palabra = line.split(',')
                file_name = palabra[0].split(":")[1]
                new_format = palabra[1].split(":")[1] 
                timestamp = palabra[2].split(":")[1]
                #status = palabra[3].split(":")[1]
                #taskId = palabra[4].split(":")[1]


                origen_convert = file_name.split(".")
                destino_convert = new_format.split(".")
                if((origen_convert == "mp3") and (destino_convert == "wav")):
                    convertidor.mp3_wav()
                elif((origen_convert == "mp3") and (destino_convert == "wma")):
                    convertidor.mp3_WMA()
                elif((origen_convert == "wav") and (destino_convert == "mp3")):
                    convertidor.wav_mp3()
                elif((origen_convert == "wav") and (destino_convert == "wma")):
                    convertidor.wav_wma()
                elif((origen_convert == "wma") and (destino_convert == "mp3")):
                    convertidor.wma_mp3()
                elif((origen_convert == "wma") and (destino_convert == "wav")):
                    convertidor.WMA_WAV()
                elif((origen_convert == "mp3") and (destino_convert == "acc")):
                    convertidor.mp3_acc()
                elif((origen_convert == "mp3") and (destino_convert == "ogg")):
                    convertidor.mp3_ogg()
from lib2to3.pytree import convert
#from Converter import create_app
from markupsafe import escape
from flask_restful import Api
from vistas.convertidor import converter as convertidor_
from vistas import statusCheck


from flask import Flask
def create_app(config_name):
    app = Flask(__name__)
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()
api = Api(app)

api.add_resource(statusCheck, '/api/status')

file_path_redis = "./vistas/programar_task.txt"

class Converter():

    def convertir(self):
        convertidor = convertidor_()
        with open(file_path_redis) as archivo:
            lines_of_tasks = archivo.readlines()
            print(lines_of_tasks)

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

converter = Converter()
converter.convertir()

print(' * CONVERTER corriendo ----------------')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002,debug=True)

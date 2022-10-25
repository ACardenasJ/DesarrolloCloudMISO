# DesarrolloCloudMiso
Aqui se desarrollara todo lo que es Desarrollo Cloud

# INSTRUCCIONES PARA CORRER EL PROYECTO

* Descargar Docker Desktop V4.13.0
* En el terminal correr el siguiente comando en la carpeta raiz DesarrolloCloudApiConverter: docker-compose up --build 

## Instrucciones - Entorno Virtual Local

Crear Entorno
python3 -m venv venv
Activar Entorno
source venv/bin/activate
Desactivar Entorno
deactivate

Instala requerimientos generales
pip3 install -r requirements.txt 

Probar
api --> puerto 5001
* flask run -p 5001

back --> puerto 5000 
* flask run -p 5000

converter --> puerto 5002
* flask run -p 5002


## Docker
Carpeta Backend
Compilar dockerFile: 
* docker build ./Backend/. -t deploy_back 
Correr dockerFile individual: 
* docker run -p 5000:5000 -t -i deploy_back:latest

Carpeta Api
Compilar dockerFile: 
* docker build ./Api_c/. -t deploy_api 
Correr dockerFile individual: 
* docker run -p 5001:5001 -t -i deploy_api:latest

Carpeta Converter
Compilar dockerFile: 
* docker build ./Converter_c/. -t deploy_converter
Correr dockerFile individual: 
* docker run -p 5002:5002 -t -i deploy_converter:latest


## Docker Compose
Carpeta Raiz - correr docker-compose: 
* docker-compose up --build

## URLs de prueba de status
Backend:
* http://localhost:5000/api/status

Api:
* http://localhost:5001/api/status

Converter:
* http://localhost:5002/api/status


## Docker commands

listar dockers: docker ps

revisar dentro de un docker: docker exec -it desarrollocloudapiconverter-api-1 sh

revisar volumenes: docker volume ls

revisar detalle de volumen: docker volume inspect desarrollocloudapiconverter_shared-volume

volumen compartido entre dockers: cd /usr/src/app/upfiles


## Convertir archivos
ffmpeg -i /usr/src/app/upfiles/basto.mp3 /usr/src/app/pofiles/basto.wma
ffmpeg -i basto.mp3 basto.wma
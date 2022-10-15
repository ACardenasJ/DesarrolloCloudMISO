from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import requests
import json


class VistaAPIGateway(Resource):
    def post(self):
        try:
            url = 'http://localhost:5002/validarPass'
            
            data = {'usuario' : request.json['usuario'],
                    'contrasena': request.json['contrasena']}                   

            content = requests.post(url,json=data)
            print(content.json())
            if content.status_code == 404:
                return {'error': 'Servicio que valida la complejidad del passs no esta disponible'}, 404
            else:
                registerResponse = content.json()
                registerResponseDate = registerResponse['status']
                if registerResponseDate == 'False':
                    return {'error': 'pass Invalido'}, 405
                
                url_back = 'http://localhost:5000/signin/user'
                dataBudy = {'usuario' : request.json['usuario'],
                            'contrasena': request.json['contrasena'],
                            'u_email': request.json["u_email"], 
                            'phone' : request.json["phone"]}
                register = requests.post(url_back,json=dataBudy)  
                return register.json(), 200
        except ConnectionError as e:
            return {'error': 'Servicio InfoTemp offline -- Connection'}, 404
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            return {'error': 'Servicio InfoTemp offline -- Timeout'}, 404
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return {'error': 'Servicio InfoTemp offline -- ManyRedirects'}, 404
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            return {'error': 'Servicio InfoTemp offline -- Request'}, 404
        except Exception as e:
            return {'error': 'Servicio InfoTemp - Error desconocido -' + str(e)}, 404
    """Codigo para que juan trabaje y deje de mamar gallo
    Codigo para que juan trabaje y deje de mamar gallo
    Codigo para que juan trabaje y deje de mamar gallo
    Codigo para que juan trabaje y deje de mamar gallo
    Codigo para que juan trabaje y deje de mamar gallo
    Codigo para que juan trabaje y deje de mamar gallo
    Codigo para que juan trabaje y deje de mamar gallo"""
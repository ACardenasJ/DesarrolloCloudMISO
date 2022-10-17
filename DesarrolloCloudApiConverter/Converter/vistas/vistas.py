from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
import json
from sqlalchemy import desc

import re


class VistaValidarPassword(Resource):

    def post(self):
        password = request.json['contrasena']
        validarPassword = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,15}", password)
        status = "True" if validarPassword is not None else "False"
        return {'status': status, 'response': 201}

from flask import Flask
from flask_cors import CORS
def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temperatura.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #app.config['JWT_SECRET_KEY'] = 'frase-secreta'  # Change this!

    #app.config['PROPAGATE_EXCEPTIONS'] = True
    
    return app
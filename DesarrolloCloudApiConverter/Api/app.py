from Api import create_app
from markupsafe import escape
from flask_restful import Api
from Api.vistas.vistas import VistaSingUp, VistaLogIn, VistaTask, VistaFiles 



app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)


api.add_resource(VistaSingUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
#api.add_resource(VistaTask, '/api/task')
api.add_resource(VistaTask, '/api/task/<int:id_task>')
api.add_resource(VistaFiles, '/api/files/<string:file_name>')
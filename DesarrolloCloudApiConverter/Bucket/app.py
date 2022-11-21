from flask_restful import Api
from flask import Flask
from flask_cors import CORS
from vistas import statusCheck, ManageBucketUP, ManageBucketPO, MBucketPOST

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    return app

app = create_app('default')

app_context = app.app_context()
app_context.push()
api = Api(app)

api.add_resource(statusCheck, '/api/status')
api.add_resource(MBucketPOST, '/api/BucketUp/<string:file_name>/<int:id_task>')
api.add_resource(ManageBucketUP, '/api/BucketUp/<string:file_name>')
api.add_resource(ManageBucketPO, '/api/BucketPo/<string:file_name>')

print(' * Up/Down Bucket corriendo ----------------')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005,debug=True)
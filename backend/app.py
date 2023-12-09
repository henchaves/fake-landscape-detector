from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources.upload_image import UploadImage


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(UploadImage, "/predict")
    
    CORS(app)
    return app

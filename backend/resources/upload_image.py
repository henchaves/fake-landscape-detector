from flask import Flask, render_template, make_response
from flask_restful import Resource, reqparse
import werkzeug

from datetime import datetime
import os

from libs.predict_image import load_image, request_model

class UploadImage(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("file", type=werkzeug.datastructures.FileStorage, location="files")
    headers = {"Content-Type": "text/html"}

    @classmethod
    def post(cls):
        files = cls.parse.parse_args()
        image = files["file"]
        if "image" in image.content_type:
            time_str = datetime.now().strftime("%Y%m%d%H%M%S")
            image_filename = f"{time_str}-{image.filename}"
            image_path = os.path.join("uploads", image_filename)
            image.save(image_path)
            X = load_image(image_filename, "uploads")
            prediction, probability = request_model(X)
            if len(prediction) == 0:
                prediction = ["Not Found"]

            probability = round(probability * 100, 2)
            probability = str(probability) + "%"
            return {"prediction": prediction, "probability": probability}, 200
            # return make_response(render_template("index.html", message="Upload an image", result=prediction), 200, cls.headers)
        return {"message": "Error"}, 400
    
    @classmethod
    def get(cls):
        return make_response(render_template("index.html", message="Upload an image"), 200, cls.headers)

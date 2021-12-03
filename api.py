from __future__ import print_function 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
from google.cloud import vision
import io
from database import get_connection
 
from datetime import timedelta
 
# Configuración de formatos de archivo permitidos
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg', 'JPEG'])

def detect_text_uri(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    string = ""
    ban = 0
    for item in texts:
        if "DOMICILIO" in item.description or "EDAD" in item.description or "FEC" in item.description:
            ban = 0
        if ban == 1:
            string += f"{item.description} " 
        if "NOMBRE" in item.description:
            ban = 1
    try:
        name = string.split("NOMBRE ")[1] 
        if name == "":
            return "No name detecte, please try again"
        return name
    except:
        return "No name detected, please try again" 

    for item in texts:
        if "DOMICILIO" in item.description or "EDAD" in item.description or "FEC" in item.description:
            ban = 0
        if ban == 1:
            string += f"{item.description} " 
        if "NOMBRE" in item.description:
            ban = 1
    try:
        name = string.split("NOMBRE ")[1] 
        if name == "":
            return "No name detected, please try again"
        return name
    except:
        return "No name detected, please try again" 

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def insert(name, color):
                cx = get_connection()
                with cx.cursor() as cursor:
                    cursor.execute("INSERT INTO api (name, color) VALUES (%s, %s)",
                                (name, color))
                cx.commit()
                cx.close()

def get_patients():
    cx = get_connection()
    patients = []
    with cx.cursor() as cursor:
        cursor.execute("SELECT * FROM api")
        patients = cursor.fetchall()
    cx.close()
    return patients

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)
 
 
@app.route ('/upload', methods = ['POST']) 
def upload():
    if request.method == 'POST':
        color = int(request.form.get("color"))
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify ({"error": 1001, "msg": "Verifique el tipo de imagen cargada, solo png, PNG, jpg, JPG, bmp"})
 
 
        basepath = os.path.dirname (__file__)

        upload_path = os.path.join (basepath, secure_filename (f.filename)) 

        f.save(upload_path)
 
        img = cv2.imread(upload_path)
        #cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
 
        name = detect_text_uri(upload_path)
        if 'please' in name:
            return 'Error'
        else:
            insert(name, color)
            return 'Ok'

@app.route("/patients", methods = ['GET'])
def juegos():
    response = get_patients()
    return jsonify(response)
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
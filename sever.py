import flask
import werkzeug
import time
import cv2
import numpy as np
import joblib
import requests
import os   
import json
import urllib
from flask_cors import CORS
from io import BytesIO
from OpenSSL import SSL
from PIL import Image



def process_url(url):
    Picture_request = requests.get(url)
    path = "./res/image.jpg"
    with open(path, 'wb') as f:
        f.write(Picture_request.content)
    return path


app = flask.Flask(__name__)
@app.route("/v1/auth/url_image", methods=['POST', 'OPTION'])
def handle_request():
    response = flask.Response()
    f = None
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"]= "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    #print("\nNumber of Received Images : ", len(files_ids))
    #print(flask.request.form["url"])
    try:
        if flask.request.form['url']:
            url = flask.request.form['url']
            filepath = process_url(url)
            command = ".\darknet.exe detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights -ext_output -dont_show -out ./res/result.json "+filepath
            os.system("start /wait cmd /c {command}".format(command=command))
            print("done")
            with open("./res/result.json") as json_file:
                data = json.load(json_file)
            return str(data)
    except:
        pass
        
    
    return "Failed"

@app.route("/v1/auth/upload_image", methods=['POST'])
def handle_request2():
    response = flask.Response()
    f = None
    response.headers["Access-Control-Allow-Origin"] = "*"  
    if flask.request.files['image']:
        img = flask.request.files['image']
        filename = werkzeug.utils.secure_filename(img.filename)
        print("Image Filename : " + img.filename)
        filepath = "E:/AIA/yoloV4/darknet/res" + "/"+filename
        img.save(filepath)
        command = ".\darknet.exe detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights -ext_output -dont_show -out ./res/result.json "+filepath
        os.system("start /wait cmd /c {command}".format(command=command))
        #os.system('cmd /k {command}'.format(command=command))
        print("done")
        with open('E:/AIA/yoloV4/darknet/res/result.json') as json_file:
            data = json.load(json_file)

        return str(data)

    return "failed"


def main():
	cors = CORS(app)
	app.run(host="192.168.1.2", port=8080, debug=True)


if __name__ == '__main__':
    main()
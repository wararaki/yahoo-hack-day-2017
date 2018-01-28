'''
sample application
'''
# load libraries
import json
import time
import copy
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from flask import Flask, render_template, request, Response
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import tensorflow as tf
import websocket

# generate application instance
app = Flask("Yahoo Hack Day 2017")

# load model
model = load_model("models/detect_model.hdf5")
model._make_predict_function()
tf_graph = tf.get_default_graph()

# define flags
flag_alert = False
flag_start_time = None

# ng_image
ng_info = {"time": None, "image": None}

def fix_base64_to_np(b64_img):
    '''
    convert data
    '''
    str_img = b64_img.replace('data:image/jpeg;base64,', '')
    # print(str_img)
    buf = BytesIO(base64.b64decode(str_img))#.encode('utf-8')
    img = Image.open(buf)
    img = img.resize((100, 100))
    img = img.convert('RGB')
    data = np.array([np.asarray(img)])
    # data = img_to_array(img)
    # print(data.shape)
    return data


def validate_images(images):
    '''
    if the car is near, this method return True
    '''
    ## base64 convert
    cnt = 0
    predicts = []
    for image in images:
        data = fix_base64_to_np(image)
        with tf_graph.as_default():
            result = model.predict_classes(data)
        # print(result)
        cnt += result
        if result == 0:
            predicts.append('near')
        elif result == 1:
            predicts.append('far')
        else:
            predicts.append('unknown')

    # if near, return true
    result_flag = cnt > len(images)
    return result_flag, predicts


@app.route("/api/detect", methods=["POST"])
def detect():
    '''
    detection car
    '''
    request_json = request.json
    if request.method == 'POST':
        img = request_json.get('image')
        data = fix_base64_to_np(img)
        with tf_graph.as_default():
            pred = model.predict_classes(data)
        if pred == 0:
            msg = 'near'
            ng_info["time"] = time.time()
            ng_info["image"] = img
        elif pred == 1:
            msg = 'far'
        else:
            msg = pred
        body = json.dumps({"predict": msg, "image": img})
        response = Response(body, status=200, mimetype='application/json')
    else:
        body = json.dumps({"message": "bad request."})
        response = Response(body, status=400, mimetype='application/json')

    return response



@app.route("/api/reckless_driving/analyze", methods=["GET", "POST"])
def analyze():
    '''
    analyze driving
    '''
    # flag check
    global flag_alert
    global flag_start_time
    
    request_json = request.json

    if request.method == 'POST':
        # get images
        req_time = request_json.get('current_time')
        images = request_json.get('images')
        # print(request_json)
        # check
        result_flag, predicts = validate_images(images)
        # result_flag = False
        # images = [image+"_ok" for image in images]

        # alert check
        alert_signal = False
        reckless_level = 0
        if result_flag and flag_alert:
            diff_time = time.time() - flag_start_time
            # alert check: if spend over 10sec, this api return the alert signal.
            if diff_time > 10.0:
                alert_signal = True
                reckless_level = 5
        # flag time check
        elif flag_alert:
            flag_start_time = time.time()
            flag_alert = True
        # flag reset
        else:
            flag_start_time = None
            flag_alert = False

        body = json.dumps({"status": True,  "alert_signal": alert_signal, "reckless_level": reckless_level, "predicts": predicts, "current_time": req_time, "images": images})
        response = Response(body, status=200, mimetype='application/json')
    else:
        body = json.dumps({"message": "bad request."})
        response = Response(body, status=400, mimetype='application/json')
        flag_alert = False

    return response


@app.route("/api/reckless_driving/report", methods=["POST"])
def report():
    '''
    report
    '''
    request_json = request.json

    if request.method == "POST":
        images = request_json.get("images")
        images = [image+"_ok" for image in images]
        # images processing
        body = json.dumps({"status": True, "images": images})
        response = Response(body, status=200, mimetype="application/json")
    else:
        body = json.dumps({"message": "bad request"})
        response = Response(body, status=400, mimetype="application/json")

    return response


@app.route("/ng_check")
def ng_check():
    '''
    return ng_checklist
    '''
    access_time = time.time()
    if ng_info.get('time') is None or (access_time - ng_info.get('time')) > 60:
        body = {"time": None, "image": None, "is_ng": False}
    else:
        body = copy.deepcopy(ng_info)
        body['is_ng'] = True
    response = Response(json.dumps(body), status=200, mimetype="application/json")

    return response


@app.route("/test")
def index():
    '''
    return testpage
    '''
    return render_template('test.html')


@app.route("/test2")
def test2():
    '''
    return detect test page
    '''
    return render_template('test2.html')


@app.route("/sample")
def sample():
    '''
    sample output
    '''
    return '''
            <html>
                <head>
                </head>
                <body>
                    <div>
                        Hello, World!
                    </div>
                </body>
            </html>
           '''

if __name__ == "__main__":
    '''
    app run
    '''
    app.run(host="0.0.0.0", debug=True)
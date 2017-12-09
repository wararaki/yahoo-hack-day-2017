'''
sample application
'''
# load libraries
import json
import time
import base64
from PIL import Image
import numpy as np
from flask import Flask, render_template, request, Response
from keras.models import load_model

# generate application instance
app = Flask("Yahoo Hack Day 2017")

# load model
model = load_model("models/detect_model.hdf5")

# define flags
flag_alert = False
flag_start_time = None

def fix_base64_to_np(b64_img):
    '''
    convert data
    '''
    str_img = b64_img.replace('data:image/jpeg;base64,', '')
    buf = base64.b64decode(str_img).encode('utf-8')
    img = Image.open(buf)
    img = img.resize((100, 100))
    data = np.array(img.asarray())
    return data


def validate_images(images):
    '''
    if the car is near, this method return True
    '''
    ## base64 convert
    cnt = 0
    for image in images:
        data = fix_base64_to_np(image)
        result = model.predict(data)
        print(result)
        cnt += result
        # check(image)
    
    # if near, return true
    if cnt > 3:
        return True
    return False


@app.route("/api/detect", methods=["POST"])
def detect():
    '''
    detection car
    '''
    request_json = request.json
    if request.method == 'POST':
        img = request_json.get('image')
        data = fix_base64_to_np(img)
        pred = model.predict(data)
        if pred == 0:
            msg = 'near'
        elif pred == 1:
            msg = 'far'
        else:
            msg = 'error'
        body = json.dumps({"predict": msg})
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
        # result_flag = validate_images(images)
        result_flag = False
        images = [image+"_ok" for image in images]

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

        body = json.dumps({"status": True,  "alert_signal": alert_signal, "reckless_level": reckless_level, "images": images, "current_time": req_time})
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
        response = Response(body, status=400, mimetype="application/json")
    else:
        body = json.dumps({"message": "bad request"})
        response = Response(body, status=400, mimetype="application/json")

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
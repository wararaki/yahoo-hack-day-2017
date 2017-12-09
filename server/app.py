'''
sample application
'''
# load libraries
import json
import time
from flask import Flask, render_template, request, Response

# generate application instance
app = Flask("Yahoo Hack Day 2017")

# load model

flag_alert = False
flag_start_time = None

def validate_images(images):
    '''
    if the car is near, this method is True
    '''
    ## base64 convert
    # for image in images:
    #     check(image)

    # if near, return true
    return False

@app.route("/api/reckless_driving/analyze", method=["GET", "POST"])
def analyze():
    '''
    analyze driving
    '''
    # flag check
    global flag_alert
    global flag_start_time

    if request.method == 'POST':
        # get images
        req_time = request.args.get('current_time')
        images = request.args.get('images')
        
        # check
        result_flag = validate_images(images)
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
        body = json.dumps({"message": "get reqiest"})
        response = Response(body, status=200, mimetype='application/json')
        flag = False

    return response


@app.route("/test")
def index():
    '''
    return testpage
    '''
    return render_template('test.html')


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
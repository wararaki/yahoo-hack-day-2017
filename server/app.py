'''
sample application
'''
# load libraries
import json
from flask import Flask, render_template, request, Response

# generate application instance
app = Flask("Yahoo Hack Day 2017")


@app.route("/api/reckless_driving/analyze", method=["POST"])
def analyze():
    '''
    analyze driving
    '''
    if request.method == 'POST':
        body = json.dumps({"id": 1, "answer": 5})
        response = Response(body, status=200, mimetype='application/json')
    else:
        body = json.dumps({"message": "get reqiest"})
        response = Response(body, status=200, mimetype='application/json')

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
'''
sample application
'''

from flask import Flask

app = Flask("sample")

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
    app.run(host="0.0.0.0", debug=True)
# This is the code for the Flask web server
from flask import Flask, render_template
from camera import Capture

# camera init stuff
capture = Capture()
capture.start()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", image_data=get_image_b64())

@app.route("/get_image_b64")
def get_image_b64():
    return capture.get_image_b64().decode()

if __name__ == "__main__":
    app.run("0.0.0.0")
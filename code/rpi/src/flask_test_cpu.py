from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/move")
def run_script():
    #subprocess.call("sudo pigpiod", shell=True)
    subprocess.call("python3 /home/mrcoffee/move.py", shell=True)
    return "<p>move arm</p>"

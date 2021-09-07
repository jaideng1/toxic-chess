import threading
import time
from flask import Flask
app = Flask(__name__)

def run_job():
        while True:
            print("Run recurring task")
            #time.sleep(3)

@app.before_first_request
def activate_job():
    print("b4")
    

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    thread = threading.Thread(target=run_job)
    thread.start()
    app.run()
from flask import Flask, render_template, redirect, request
from threading import Thread
import random, smartcabinet

# TODO: Make sure to call the SmartCabinet functions
# in this file to streamline the process, and get to threads
# quickly

global rfid_mode, box_mode
rfid_mode = "Unknown"
box_mode = "Unknown"
app = Flask(__name__, static_folder='assets')

cameraThread = Thread(target = smartcabinet.useCamera)
keypadThread = Thread(target = smartcabinet.keypadOperate)
rfidThread = Thread(target = smartcabinet.rfidOperate)
loadCellThread = Thread(target = smartcabinet.loadCellOperate)

# Default Path
@app.route("/")
def start():
    return redirect("/templates/start")

@app.route("/templates/start")
def start_template():
    return render_template("start.html")

@app.route("/templates/selection")
def selection_template():
    cameraThread.start()
    keypadThread.start()
    rfidThread.start()
    loadCellThread.start()
    return render_template("selection.html")

# Keypad page just has one button, so we can simply 
# request the form and change the keypad code from here.
@app.route("/templates/keypadmode", methods=['POST', 'GET'])
def keypadmode_template():
    keypad_code = "No Passcode Yet"
    if request.method=="POST":
        keypad_code = request.form['virtual_keypad_input']
    return render_template("keypadmode.html", passcode_entered = keypad_code)

# Unlock page has two buttons in the website
@app.route("/templates/unlockedmode")
def unlockedmode_template():
    on = ""
    off = ""
    if box_mode == "ON":
        on = "disabled"
        off = ""
    elif box_mode == "OFF":
        on = ""
        off = "disabled"
    return render_template("unlockedmode.html", box_lock_state = box_mode, ondisabled = on, offdisabled = off)

@app.route("/templates/boxlock/<int:action>")
def boxlock_action(action):
    global box_mode
    # Unlocks the box
    if action == 1:
        box_mode = "ON"
        print("Box unlocked!")
        smartcabinet.servoOperate(1)
    # Locks the box
    elif action == 0:
        box_mode = "OFF"
        print("Box locked!")
        smartcabinet.servoOperate(0)
    return redirect("/templates/unlockedmode")

# Various options, with the ability to disable 
# someone out and checking the weight of the box.
@app.route("/templates/options", methods=['POST', 'GET'])
def options_template():
    #current_weight = smartcabinet.loadCellWeightMeasure()
    current_weight = random.randint(1, 20)
    if current_weight < 5:
        warn_msg = "WARNING!"
    else:
        warn_msg = ""
    
    d = [{'x': random.randint(1, 5), 'y': random.randint(6,9)}, {'x': random.randint(10, 14), 'y': random.randint(15,20)}]
    return render_template("options.html", weight_value = current_weight, warning_message = warn_msg, hist = d)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
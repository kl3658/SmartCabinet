from flask import Flask, render_template, redirect
import smartcabinet

app = Flask(__name__, static_folder='assets')

@app.route("/")
def start():
    return redirect("/start")

@app.route("/start")
def start_template():
    return render_template("start.html")

@app.route("/selection")
def selection_template():
    return render_template("selection.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
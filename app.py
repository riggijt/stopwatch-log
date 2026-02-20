from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

start_time = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    global start_time
    start_time = time.time()
    return jsonify({"status": "started"})


@app.route("/stop", methods=["POST"])
def stop():
    global start_time

    if start_time is None:
        return jsonify({"error": "Stopwatch not started"}), 400

    elapsed = time.time() - start_time
    start_time = None

    return jsonify({"elapsed": round(elapsed, 2)})


if __name__ == "__main__":
    app.run(debug=True)

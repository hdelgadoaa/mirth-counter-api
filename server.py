from flask import Flask, jsonify
from collections import defaultdict
import json
import os
from threading import Lock

app = Flask(__name__)

COUNTERS_FILE = "counters.json"
lock = Lock()
counters = defaultdict(int)


def load_counters():
    """Carga los contadores desde un archivo JSON si existe."""
    global counters
    if os.path.exists(COUNTERS_FILE):
        try:
            with open(COUNTERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                counters = defaultdict(int, data)
        except Exception:
            counters = defaultdict(int)
    else:
        counters = defaultdict(int)


def save_counters():
    """Guarda los contadores en un archivo JSON."""
    with open(COUNTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(counters, f)


def hit(key):
    with lock:
        counters[key] += 1
        save_counters()
        return jsonify({"value": counters[key]})


def get_value(key):
    with lock:
        value = counters.get(key, 0)
        return jsonify({"value": value})


@app.before_first_request
def init():
    load_counters()


@app.get("/api/visitas/hit")
def visitas_hit():
    return hit("visitas")


@app.get("/api/visitas/get")
def visitas_get():
    return get_value("visitas")


@app.get("/api/descargas/hit")
def descargas_hit():
    return hit("descargas")


@app.get("/api/descargas/get")
def descargas_get():
    return get_value("descargas")


@app.get("/")
def root():
    return jsonify({"status": "ok", "message": "Mirth Compare Counter API"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

"""
Flask REST API — Smart Agriculture System
Endpoints:
  POST /predict/crop      → crop recommendation
  POST /predict/yield     → yield estimate
  GET  /sensors/latest    → latest simulated readings
  GET  /tasks             → current heap task queue
  GET  /route/<src>/<dst> → shortest farm zone route
"""
import os, sys, time, random, math
import numpy as np
from flask import Flask, request, jsonify
import joblib

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from aads.heap      import MaxHeap, Task
from aads.dijkstra  import dijkstra, reconstruct_path, FARM_GRAPH

app        = Flask(__name__)
MODELS_DIR = "models"

# ── Load models (graceful fallback if not trained yet) ───────
def _load(path):
    return joblib.load(path) if os.path.exists(path) else None

crop_rf = _load(f"{MODELS_DIR}/crop_rf.pkl")
crop_sc = _load(f"{MODELS_DIR}/crop_scaler.pkl")
crop_le = _load(f"{MODELS_DIR}/crop_label_encoder.pkl")
yield_lr = _load(f"{MODELS_DIR}/yield_lr.pkl")
yield_sc = _load(f"{MODELS_DIR}/yield_scaler.pkl")

# ── In-memory task heap ──────────────────────────────────────
task_heap    = MaxHeap()
_task_id_ctr = 0

def _seed_tasks():
    global _task_id_ctr
    samples = [
        ("Irrigation",   "ZoneA", 18, 1, 0.1),
        ("Fertilize",    "ZoneB", 45, 3, 0.2),
        ("Pest Control", "ZoneC", 60, 2, 0.9),
        ("Irrigation",   "ZoneD", 22, 1, 0.1),
    ]
    for t, z, m, d, p in samples:
        _task_id_ctr += 1
        task_heap.insert(Task(_task_id_ctr, t, z, m, d, p))

_seed_tasks()

# ── Simulated live sensor readings ───────────────────────────
_moisture = {"A": 55.0, "B": 42.0, "C": 68.0, "D": 30.0}

def _live_reading(zone):
    _moisture[zone] = max(10, _moisture[zone] - random.uniform(0.1, 0.5))
    if _moisture[zone] < 15:
        _moisture[zone] = random.uniform(55, 70)
    h = (time.time() / 3600) % 24
    return {
        "zone":     zone,
        "temp":     round(22 + 8 * math.sin(math.pi * h / 12) + random.gauss(0, 0.5), 2),
        "humidity": round(65 + random.gauss(0, 3), 2),
        "moisture": round(_moisture[zone], 2),
        "N":        round(random.uniform(60, 120), 1),
        "P":        round(random.uniform(30, 80),  1),
        "K":        round(random.uniform(20, 60),  1),
        "ph":       round(random.uniform(5.5, 7.5), 2),
        "timestamp": round(time.time(), 2),
    }

# ── Routes ───────────────────────────────────────────────────

@app.route("/predict/crop", methods=["POST"])
def predict_crop():
    if not crop_rf:
        return jsonify({"error": "Model not trained. Run ml/train_crop.py first."}), 503
    body  = request.get_json(force=True)
    feats = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    try:
        inp  = crop_sc.transform([[body[f] for f in feats]])
        idx  = crop_rf.predict(inp)[0]
        conf = float(crop_rf.predict_proba(inp).max())
        return jsonify({"crop": crop_le.inverse_transform([idx])[0],
                        "confidence": round(conf, 3)})
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400


@app.route("/predict/yield", methods=["POST"])
def predict_yield():
    if not yield_lr:
        return jsonify({"error": "Model not trained. Run ml/train_yield.py first."}), 503
    body  = request.get_json(force=True)
    feats = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    try:
        inp  = yield_sc.transform([[body[f] for f in feats]])
        yld  = float(yield_lr.predict(inp)[0])
        return jsonify({"yield_quintals_per_ha": round(yld, 2)})
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400


@app.route("/sensors/latest", methods=["GET"])
def sensors_latest():
    return jsonify([_live_reading(z) for z in ["A", "B", "C", "D"]])


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = [{"task_id": t.task_id, "type": t.task_type,
               "zone": t.zone, "score": round(t.score, 4),
               "moisture": t.moisture}
             for t in task_heap.all_tasks()]
    return jsonify(tasks)


@app.route("/route/<src>/<dst>", methods=["GET"])
def get_route(src, dst):
    src, dst = src.upper(), dst.upper()
    graph_keys = list(FARM_GRAPH.keys())
    src_key = next((k for k in graph_keys if k.upper() == src), None)
    dst_key = next((k for k in graph_keys if k.upper() == dst), None)
    if not src_key or not dst_key:
        return jsonify({"error": "Invalid zone"}), 400
    dist, prev = dijkstra(FARM_GRAPH, src_key)
    path = reconstruct_path(prev, dst_key)
    return jsonify({"from": src_key, "to": dst_key,
                    "distance_m": dist[dst_key], "path": path})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "models_loaded": bool(crop_rf)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

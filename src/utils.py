import os, json, logging
from datetime import datetime

def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def write_json(obj, path):
    ensure_dirs(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)

def log_trace(trace_obj, path):
    write_json(trace_obj, path)
    logging.info(f"Wrote trace to {path}")

import yaml, os

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    cfg["data_csv"] = os.getenv("DATA_CSV", cfg.get("data_csv"))
    cfg["report_dir"] = os.getenv("REPORT_DIR", cfg.get("report_dir", "reports"))
    cfg["log_dir"] = os.getenv("LOG_DIR", cfg.get("log_dir", "logs"))
    cfg["random_seed"] = int(os.getenv("RANDOM_SEED", cfg.get("random_seed", 42)))
    cfg["confidence_min"] = float(os.getenv("CONFIDENCE_MIN", cfg.get("confidence_min", 0.6)))
    return cfg

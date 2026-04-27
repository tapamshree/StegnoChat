import hashlib
import json
import os

CONFIG_FILE = "config.json"

def set_pin(pin: str):
    h = hashlib.sha256(pin.encode()).hexdigest()
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
    cfg["pin_hash"] = h
    if "cover_text" not in cfg:
        cfg["cover_text"] = "👋"
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

def check_pin(pin: str) -> bool:
    if not os.path.exists(CONFIG_FILE):
        return False
    with open(CONFIG_FILE, "r") as f:
        cfg = json.load(f)
    return hashlib.sha256(pin.encode()).hexdigest() == cfg.get("pin_hash")

def has_pin() -> bool:
    if not os.path.exists(CONFIG_FILE):
        return False
    with open(CONFIG_FILE, "r") as f:
        cfg = json.load(f)
        return "pin_hash" in cfg

def get_cover_text() -> str:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("cover_text", "👋")
    return "👋"

class Session:
    unlocked = False

session = Session()

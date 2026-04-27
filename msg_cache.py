"""
Local cache for sent steganographic messages.
Since WhatsApp's UIA strips zero-width chars, we can't read them back
from the UI. Instead we cache every message we send so the overlay
can show the decoded plaintext when secure mode is active.
"""

import json
import os
import threading
import time

CACHE_FILE = "msg_cache.json"
_lock = threading.Lock()

def _load():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def _save(entries):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def add_message(plaintext: str, cover_text: str):
    """Store a sent message in the cache."""
    with _lock:
        entries = _load()
        entries.append({
            "plain": plaintext,
            "cover": cover_text,
            "time": time.time(),
        })
        # Keep only last 500 messages to avoid bloat
        if len(entries) > 500:
            entries = entries[-500:]
        _save(entries)

def get_messages() -> list[dict]:
    """Return all cached messages."""
    with _lock:
        return _load()

def clear():
    """Clear the entire cache."""
    with _lock:
        _save([])

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import stego

def test_encode_decode():
    msg = "Hello World!"
    encoded = stego.encode(msg)
    assert stego.decode(encoded) == msg

def test_empty_string():
    encoded = stego.encode("")
    assert stego.decode(encoded) is None

def test_unicode_string():
    msg = "안녕하세요 🌍"
    encoded = stego.encode(msg)
    assert stego.decode(encoded) == msg

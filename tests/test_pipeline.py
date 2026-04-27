import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import stego

def test_full_pipeline():
    # User message
    user_message = "This is a highly secret message 🤫"
    
    # 1. Encode
    encoded = stego.encode(user_message, cover="👋")
    assert encoded.startswith("👋")
    assert len(encoded) > len(user_message)
    
    # 2. Simulate transit (copy paste, WhatsApp network)
    received = encoded
    
    # 3. Decode
    decoded = stego.decode(received)
    
    assert decoded == user_message

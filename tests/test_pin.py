import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

def test_pin_workflow():
    if os.path.exists("config.json"):
        os.remove("config.json")
    
    assert not config.has_pin()
    config.set_pin("1234")
    assert config.has_pin()
    
    assert config.check_pin("1234")
    assert not config.check_pin("0000")

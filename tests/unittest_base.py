import unittest
import json

# Helper to fake an Azure Queue Message
class FakeQueueMessage:
    def __init__(self, msg):
        self._msg = msg
    
    def get_body(self):
        return self._msg
    
    def get_json(self):
        return json.loads(self.get_body().decode("utf-8"))

class TestCase(unittest.TestCase):

    def _use_adapters(self):
        return False

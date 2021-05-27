import unittest
import json

class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        from app.app import api
        self.app = api.app.test_client()
       
    
    def test_helloworld(self):

        response = self.app.get("/", headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual('world', response.json["hello"])

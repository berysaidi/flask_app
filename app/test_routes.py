import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from urllib.request import urlopen
import unittest
from flask import Flask
from flask_testing import LiveServerTestCase, TestCase
from werkzeug.datastructures import Headers

import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from app import app
from app.schema  import SCHEMA

# an example of good profile
# load it once because it will be used in many tests
with open("profile.json") as f :
    data = f.read()
    PROFILE = json.loads(data)

class TestAPI(TestCase):
    def create_app(self):
        # enable long diffs
        self.maxDiff = 99999
        app.config['TESTING'] = True
        # Default port is 5000, most likely to be used in debug
        app.config['LIVESERVER_PORT'] = 8943
        # Default timeout is 5 seconds
        app.config['LIVESERVER_TIMEOUT'] = 10
        return app

    def test_bad_format(self):
        headers = { 'x-client-id' : 'client',
        'Content-Type' : 'application/json'}

        # get token to communicate 
        response = self.client.post("/login", headers=headers)
        self.assertEqual(response.status, '200 OK')
        data = json.loads(response.data)
        token = data["access_token"]

        headers['x-authentication-token'] = 'Bearer %s' % token

        response = self.client.post("/profiles/clientId:09:08", headers=headers)
        # expect 401 and error codes
        self.assertEqual(response.status, '404 NOT FOUND')
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Not Found")
        self.assertEqual(data["statusCode"], 404)
        self.assertEqual(data["message"], "profile of client %s does not exist" % "09:08")

    def test_json_data_409(self):
        headers = { 'x-client-id' : 'client',
        'Content-Type' : 'application/json'}

        # get token to communicate 
        response = self.client.post("/login", headers=headers)
        self.assertEqual(response.status, '200 OK')
        data = json.loads(response.data)
        token = data["access_token"]
        # append it to the header
        headers['x-authentication-token'] = 'Bearer %s' % token

        response = self.client.post("/profiles/clientId:9c:eb:e8:8e:3b:00", headers=headers)

        self.assertEqual(response.status, '409 CONFLICT')
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Conflict")
        self.assertEqual(data["statusCode"], 409)

    def test_good_format_200(self):
        headers = { 'x-client-id' : 'client',
        'Content-Type' : 'application/json'}

        # get token to communicate 
        response = self.client.post("/login", headers=headers)
        self.assertEqual(response.status, '200 OK')
        data = json.loads(response.data)
        token = data["access_token"]

        # append it to the header
        headers['x-authentication-token'] = 'Bearer %s' % token

        response = self.client.post("/profiles/clientId:9c:eb:e8:8e:3b:00", headers=headers, data=json.dumps(PROFILE))

        self.assertEqual(response.status, '200 OK')
        res_data = json.loads(response.data)
        self.assertEqual(res_data, PROFILE)


    def test_profile_error_404(self):
        headers = { 'x-client-id' : 'client',
        'Content-Type' : 'application/json'}

        # get token to communicate 
        response = self.client.post("/login", headers=headers)
        self.assertEqual(response.status, '200 OK')
        data = json.loads(response.data)
        token = data["access_token"]

        headers['x-authentication-token'] = 'Bearer %s' % token

        response = self.client.post("/profiles/clientId:%s" % "823f3161ae4f4495bf0a90c00a7dfbff", headers=headers, data=json.dumps(PROFILE))

        data = json.loads(response.data)

        self.assertEqual(response.status, '404 NOT FOUND')
        self.assertEqual(data["error"], "Not Found")
        self.assertEqual(data["statusCode"], 404)
        self.assertEqual(data["message"], "profile of client %s does not exist" % "823f3161ae4f4495bf0a90c00a7dfbff")

    def test_schema(self):
        PROF = {"profile" : { "applicati": [
                    {
                        "application": "music_app",
                        "version": "v1.4.10",
                        },
                    {
                        "applicationId": "diagnostic_app",
                        "version": "v1.2.6",
                        },
                    {
                        "applicationId": "settings_app",
                        "version": "v1.1.5",
                        }]
                    }
                }

        self.assertEqual(validate(instance=PROFILE, schema=SCHEMA), None)


        with self.assertRaises(ValidationError):
            validate(instance={"applicationId" : "SomeId", "version" : 1234}, schema=SCHEMA)
            validate(instance=PROF, schema=SCHEMA)

    def test_mac(self):
        import csv
        with open("mac.csv", newline='') as f:
            reader = csv.reader(f, delimiter=',')
            macs = []
            for row in reader:
                macs.append(row[0])
            # get rid of title
            macs.pop(0)
            self.assertEqual(macs, ['a1:bb:cc:dd:ee:ff', 'a2:bb:cc:dd:ee:ff', 'a3:bb:cc:dd:ee:ff', 'a4:bb:cc:dd:ee:ff', 'a5:bb:cc:dd:ee:ff', '9c:eb:e8:8e:3b:00'])



if __name__ == '__main__':
    unittest.main()

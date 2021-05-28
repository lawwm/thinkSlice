from django.test import TestCase
import json
# Create your tests here.
# coverage run manage.py test .  -v 2
# coverage html

class AuthenticationWithUserRegistered(TestCase):
    @classmethod
    def setUpTestData(cls):
        registerData = {
            "username" : "jimjam",
            "email" : "jimjam@gmail.com",
            "password": "password"
        }
        loginData = {
            "username": "jimjam",
            "password": "password"            
        }
        cls.registerData = registerData
        cls.loginData = loginData

    def setUp(self):
        response = self.client.post("/api/auth/register", data=self.registerData)
        parsed = json.loads(response.content)
        self.token = parsed["token"]

    # Successful login should return status code 200 and authentication token
    def test_can_login(self):
        response = self.client.post("/api/auth/login", data=self.loginData)
        parsed = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(parsed["token"])

    # Returns a status code 200 when sending GET request with token
    def test_get_credentials(self):
        headers = {
            "HTTP_AUTHORIZATION": "Token " + self.token
        }
        response = self.client.get("/api/auth/user", **headers)
        self.assertEqual(response.status_code, 200)



class AuthenticationWithoutUserRegistered(TestCase):
    #Received status code 400 when logging in without account
    def test_cannot_login(self):
        data = {
            "username": "jimjam",
            "password": "password"            
        }
        response = self.client.post("/api/auth/login", data=data)
        self.assertEqual(response.status_code, 400)










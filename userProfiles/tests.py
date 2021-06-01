from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
import json

# Create your tests here.
# coverage run manage.py test .  -v 2
# coverage html
class GetPatchPutDeleteProfileAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        registerData = [{
            "username" : "jimjam",
            "email" : "jimjam@gmail.com",
            "password": "password"
        }, {
            "username" : "bingbong",
            "email" : "bingbong@gmail.com",
            "password": "password"
        }, {
            "username" : "buddy",
            "email" : "buddy@gmail.com",
            "password": "password"
        }]
        loginData = {
            "username": "jimjam",
            "password": "password"            
        }
        cls.registerData = registerData
        cls.loginData = loginData

    def setUp(self):
        response = self.client.post("/api/auth/register", data=self.registerData[0])
        self.client.post("/api/auth/register", data=self.registerData[1])
        self.client.post("/api/auth/register", data=self.registerData[2])

        parsed = json.loads(response.content)
        self.user_id = parsed["user"]["id"]
        # self.token = parsed["token"]
        self.headers = {
            "HTTP_AUTHORIZATION": "Token " + parsed["token"]
        }

    #Get all profiles
    def test_get_all_profile(self):
        response = self.client.get('/api/profiles')
        parsed = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(parsed), 3)

    #Get one profile by id
    def test_get_profile_id(self):
        response = self.client.get('/api/profiles/' + str(self.user_id))
        parsed = json.loads(response.content)
        user = User.objects.get(id=self.user_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed["username"], user.username)
        self.assertEqual(type(parsed), dict)
        
    #Get profile details by id
    def test_get_profile_details_id(self):
        response = self.client.get('/api/profiles/details/' + str(self.user_id))
        parsed = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

    # Patch profiles by id
    def test_edit_profile_id(self):
        editData = {
            "username" : "jimjam12",
            "is_tutor": "True"    
        }
        # PATCH profile without being the owner
        notOwnerResponse = self.client.patch('/api/profiles/' + str(self.user_id + 1), data=editData,  
            content_type='application/json' ,**self.headers)
        self.assertEqual(notOwnerResponse.status_code, 403)

        # PATCH profile while being the owner
        response = self.client.patch('/api/profiles/' + str(self.user_id), data=editData,  
            content_type='application/json' ,**self.headers)
        parsed = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed["username"], "jimjam12")
        self.assertEqual(parsed["is_tutor"], True)

    # Patch profile details by id
    def test_edit_profile_details_id(self):
        editData = {
            "tutor_contact": "12345678",
            "aggregate_star": "4.5",
        }

        # GET initial profile detail to compare wtih edited profile
        initialResponse = self.client.get('/api/profiles/details/' + str(self.user_id))
        initialParsed = json.loads(initialResponse.content)
        self.assertEqual(initialResponse.status_code, 200)

        # PATCH profile without being the owner
        notOwnerResponse = self.client.patch('/api/profiles/details/' + str(self.user_id + 1), data=editData,  
            content_type='application/json' ,**self.headers)
        self.assertEqual(notOwnerResponse.status_code, 403)

        # PATCH profile while being the owner
        response = self.client.patch('/api/profiles/details/' + str(self.user_id), data=editData,  
            content_type='application/json' ,**self.headers)
        parsed = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed["tutor_contact"], "12345678")
        self.assertEqual(parsed["aggregate_star"], 4.5)

        # PUT profile clear the profile details while not being the owner
        clearData = {
                "tutor_contact": "",
                "aggregate_star": None,
                "duration_classes": None,
                "subjects": None,
                "qualifications": ""
            }
        clearNotOwnerResponse = self.client.put('/api/profiles/details/' + str(self.user_id + 1), data=clearData,  
            content_type='application/json' ,**self.headers)
        self.assertEqual(clearNotOwnerResponse.status_code, 403)

        # PUT profile, clear the profile details while being owner
        clearResponse = self.client.put('/api/profiles/details/' + str(self.user_id), data=clearData,  
            content_type='application/json' ,**self.headers)
        clearParsed = json.loads(clearResponse.content)
        self.assertEqual(clearResponse.status_code, 200)
        self.assertEqual(initialParsed, clearParsed)


    # Delete profiles by id
    def test_delete_profile_id(self):

        # DELETE profile without being the owner
        response = self.client.delete('/api/profiles/' + str(self.user_id + 1), data='', 
            content_type='application/json',**self.headers)
        self.assertEqual(response.status_code, 403)

        # DELETE profile by id
        response = self.client.delete('/api/profiles/' + str(self.user_id), data='', 
            content_type='application/json',**self.headers)
        self.assertEqual(response.status_code, 200)

        # GET profile that has been deleted
        missingResponse = self.client.get('/api/profiles/' + str(self.user_id))
        self.assertEqual(missingResponse.status_code, 404)

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
        review_data = {
            "star_rating": "1",
            "review_title": "shit teacher",
            "review_essay": "No talent for teaching"    
        }
        cls.registerData = registerData
        cls.loginData = loginData
        cls.review_data = review_data

    def setUp(self):
        # Register test users
        response = self.client.post("/api/auth/register", data=self.registerData[0])
        studentResponse = self.client.post("/api/auth/register", data=self.registerData[1])
        self.client.post("/api/auth/register", data=self.registerData[2])

        # Parse data
        parsed = json.loads(response.content)
        studentParsed = json.loads(studentResponse.content)

        self.user_id = parsed["user"]["id"]
        self.headers = {
            "HTTP_AUTHORIZATION": "Token " + parsed["token"]
        }
        self.student_id = studentParsed["user"]["id"]
        self.student_headers = {
            "HTTP_AUTHORIZATION": "Token " + studentParsed["token"]
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
            "tutor_whatsapp": 12345678,
            "tutor_telegram": "@honestman",
            "aggregate_star": "4.5",
        }

        # POST post review so aggregate star changes
        self.client.post('/api/reviews/tutors/' + str(self.user_id), data=self.review_data,
            content_type='application/json', **self.student_headers )

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
        self.assertEqual(parsed["tutor_whatsapp"], 12345678)
        self.assertEqual(parsed["tutor_telegram"], "@honestman")
        # Aggregate star does not change
        self.assertEqual(parsed["aggregate_star"], 1)

        clearNotOwnerResponse = self.client.put('/api/profiles/details/' + str(self.user_id + 1), data="", 
            content_type='application/json' ,**self.headers)
        self.assertEqual(clearNotOwnerResponse.status_code, 403)

        # PUT profile, clear the profile details while being owner
        clearResponse = self.client.put('/api/profiles/details/' + str(self.user_id), data="",
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

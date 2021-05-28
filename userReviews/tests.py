from django.test import TestCase
from django.contrib.auth.models import User
import json

# Create your tests here.
# coverage run manage.py test .  -v 2
# coverage html
class GetPatchPutDeleteProfileAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        register_data = [{
            "username" : "jimjam",
            "email" : "jimjam@gmail.com",
            "password": "password"
        }, {
            "username" : "bingbong",
            "email" : "bingbong@gmail.com",
            "password": "password"
        }]
        review_data = {
            "star_rating": "1",
            "review_title": "shit teacher",
            "review_essay": "No talent for teaching"    
        }
        cls.register_data = register_data
        cls.review_data = review_data

    def setUp(self):
        student_response = self.client.post("/api/auth/register", data=self.register_data[0])
        tutor_response = self.client.post("/api/auth/register", data=self.register_data[1])

        student_parsed = json.loads(student_response.content)
        tutor_parsed = json.loads(tutor_response.content)

        self.student_id = student_parsed["user"]["id"]
        self.student_headers = {
            "HTTP_AUTHORIZATION": "Token " + student_parsed["token"]
        }
        self.tutor_id = tutor_parsed["user"]["id"]
        self.tutor_headers = {
            "HTTP_AUTHORIZATION": "Token " + tutor_parsed["token"]
        }

        #Post one review
        review_response =self.client.post('/api/reviews/tutors/' + str(self.tutor_id), data=self.review_data,
            content_type='application/json', **self.student_headers )
        review_parsed = json.loads(review_response.content)
        self.review_id = review_parsed['id']


    
    def test_post_review(self):
        # Ensure cannot post without credentials
        reviewResponse = self.client.post('/api/reviews/tutors/' + str(self.tutor_id), data=self.review_data,
            content_type='application/json')
        self.assertEqual(reviewResponse.status_code, 401)

        # Ensure cannot post twice
        reviewResponse = self.client.post('/api/reviews/tutors/' + str(self.tutor_id), data=self.review_data,
            content_type='application/json', **self.student_headers )
        self.assertEqual(reviewResponse.status_code, 400)

        # Gets status code 400 bad parameters when reviewing yourself
        reviewOwnResponse = self.client.post('/api/reviews/tutors/' + str(self.student_id), data=self.review_data,
            content_type='application/json', **self.student_headers )
        self.assertEqual(reviewOwnResponse.status_code, 400)

    def test_get_tutor_review(self):
        response = self.client.get('/api/reviews/tutors/' + str(self.tutor_id))
        self.assertEqual(response.status_code, 200)

    def test_get_student_review(self):
        response = self.client.get('/api/reviews/students/' + str(self.student_id))
        self.assertEqual(response.status_code, 200)

    def test_get_review_by_id(self):
        response = self.client.get('/api/reviews/' + str(self.review_id))
        self.assertEqual(response.status_code, 200)

    def test_edit_review_by_id(self):
        editData = {
            "star_rating": "2.0",
            "review_title": "Bad, just bad"
        }

        # Returns status 200 when editing own review
        response = self.client.patch('/api/reviews/' + str(self.review_id), data=editData,
            content_type='application/json', **self.student_headers )
        parsed = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(parsed["edited"], True)

        # Returns a status 403 when attempting to edit other's reviews
        forbiddenResponse = self.client.patch('/api/reviews/' + str(self.review_id), data=editData,
            content_type='application/json', **self.tutor_headers )
        self.assertEqual(forbiddenResponse.status_code, 403)

    def test_delete_review_by_id(self):

        # Returns a status 403 when attempting to delete other's reviews
        forbiddenResponse = self.client.delete('/api/reviews/' + str(self.review_id), data='', 
            content_type='application/json',**self.tutor_headers)
        self.assertEqual(forbiddenResponse.status_code, 403)

        # Returns a status 204 when deleting own review
        response = self.client.delete('/api/reviews/' + str(self.review_id), data='', 
            content_type='application/json',**self.student_headers)
        self.assertEqual(response.status_code, 204)
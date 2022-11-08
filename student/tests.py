from rest_framework.test import APITestCase
from rest_framework import status
import json


class TestStudent(APITestCase):

    def test_student(self):

        sample_data = {
            "base_profile": {
                "email": "smith@gmail.com",
                "first_name": "Smith",
                "password": "smith"
            },
            "role": "teacher"
        }
        path = "/teacher/"
        self.client.post(path, json.dumps(sample_data), content_type='application/json')

        path = "/course/"
        course_data = {
            'course_title': 'Circuit',
            'teacher_profile': 3,
            'user_id': 3
        }

        self.client.post(path, json.dumps(course_data), content_type='application/json')

        sample_data = {
            "base_profile": {
                "email": "abdulhadi@gmail.com",
                "first_name": "Hadi",
                "password": "abdulhadi"
            },
            "role": "student"
        }
        path = "/student_register/"
        response = self.client.post(path, json.dumps(sample_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        sample_data = {
            'email': "abdulhadi@gmail.com",
            'password': "abdulhadi"
        }

        path = "/get_token/"

        access_token = self.client.post\
            (path, json.dumps(sample_data), content_type='application/json').data.get("access")

        path = '/student_enroll/2'

        sample_data = {
            'enrolled_course': [3]
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.patch(path, json.dumps(sample_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


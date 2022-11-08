from rest_framework.test import APITestCase
from rest_framework import status
import json


class TestStudent(APITestCase):

    def test_result(self):

        sample_data = {
            "base_profile": {
                "email": "jason@gmail.com",
                "first_name": "Jason",
                "password": "jason"
            },
            "role": "teacher"
        }
        path = "/teacher/"
        self.client.post(path, json.dumps(sample_data), content_type='application/json')

        path = "/course/"
        course_data = {
            'course_title': 'Power',
            'teacher_profile': 2,
            'user_id': 2
        }

        self.client.post(path, json.dumps(course_data), content_type='application/json')

        sample_data = {
            "base_profile": {
                "email": "owais@gmail.com",
                "first_name": "Owais",
                "password": "owais"
            },
            "role": "student"
        }
        path = "/student_register/"
        self.client.post(path, json.dumps(sample_data), content_type='application/json')

        student_data = {
            'email': "owais@gmail.com",
            'password': "owais"
        }
        path = "/get_token/"
        access_token_student = self.client.post\
            (path, json.dumps(student_data), content_type='application/json').data.get("access")

        teacher_data = {
            'email': "jason@gmail.com",
            'password': "jason"
        }

        access_token_teacher = self.client.post\
            (path, json.dumps(teacher_data), content_type='application/json').data.get("access")

        path = '/student_enroll/1'

        sample_data = {
            'enrolled_course': [2]
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token_student}')
        self.client.patch(path, json.dumps(sample_data), content_type='application/json')

        sample_data = {
            'student': 1,
            'course': 2,
            'score': 100.0,
            'user_id': 2
        }
        path = '/result/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token_teacher}')
        response = self.client.post(path, json.dumps(sample_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
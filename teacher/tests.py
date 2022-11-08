from rest_framework.test import APITestCase
from rest_framework import status
import json


class TestTeacher(APITestCase):

    def test_teacher(self):
        sample_data = {
            "base_profile": {
                "email": "john@gmail.com",
                "first_name": "John",
                "password": "john"
            },
            "role": "teacher"
        }
        path = "/teacher/"
        response = self.client.post(path, json.dumps(sample_data), content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

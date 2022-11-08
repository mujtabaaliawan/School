from rest_framework.test import APITestCase
from rest_framework import status
import json


class TestCourse(APITestCase):

    def test_course(self):
        sample_data = {
            "base_profile": {
                "email": "abdullah@gmail.com",
                "first_name": "Abdullah",
                "password": "abdullah"
            },
            "role": "teacher"
        }
        path = "/teacher/"
        self.client.post(path, json.dumps(sample_data), content_type='application/json')

        path = "/course/"
        course_data = {
            'course_title': 'Mathematics',
            'teacher_profile': 1,
            'user_id': 1
        }
        response=self.client.post(path, json.dumps(course_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
from rest_framework.test import APITestCase
from rest_framework import status
import json
from course.models import Course
from .test_factory import TeacherFactory, StudentFactory, AdminFactory, CourseFactory


class TestResult(APITestCase):

    def test_create_result(self):
        self.course = CourseFactory.create()
        self.student = StudentFactory.create()
        path = '/enrollment/' + f'{self.student.id}'
        test_data = {
            "enrolled_course": [self.course.id]
            }
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_data = {
            "student": self.student.id,
            "course": self.course.id,
            "score": 90
        }

        path = "/results/new"

        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.login(email='student@gmail.com', password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_result(self):

        self.course = CourseFactory.create()
        self.student = StudentFactory.create()
        path = '/enrollment/' + f'{self.student.id}'
        test_data = {
            "enrolled_course": [self.course.id]
            }
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_data = {
            "student": self.student.id,
            "course": self.course.id,
            "score": 90.0
        }

        path = "/results/new"

        self.client.login(email='teacher@gmail.com', password='teacher')
        result_id = self.client.post(path, json.dumps(test_data), content_type='application/json').data.get('id')

        test_data = {
            "id": result_id,
            "student": self.student.id,
            "course": self.course.id,
            "score": 80.0
        }

        path = '/results/' + f'{result_id}'

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_result_list(self):

        path = '/results'

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


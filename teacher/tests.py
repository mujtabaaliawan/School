from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, AdminFactory


class TestTeacher(APITestCase):

    def test_create_teacher(self):

        test_data = {
            "user": {
                "email": "john@gmail.com",
                "first_name": "John",
                "password": "john"
            },
            "role": "teacher",
            "mobile_number": "03004567823"
        }
        path = "/faculty/new"

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_teacher(self):

        test_data = {
            "mobile_number": "03004567823"
        }
        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        path = '/faculty/' + f'{self.teacher.id}'
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_teacher(self):

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        path = '/faculty/' + f'{self.teacher.id}'
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_teacher_list(self):

        path = '/faculty'
        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_teacher_detail_list(self):

        path = '/faculty/detail'
        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
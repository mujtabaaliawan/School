from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, AdminFactory


class TestStaff(APITestCase):

    def test_create_staff(self):

        test_data = {
            "user": {
                "email": "john@gmail.com",
                "first_name": "John",
                "password": "john"
            },
            "role": "admin",
            "mobile_number": "03009644678"
        }
        path = "/staff/new"

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

    def test_update_staff(self):

        test_data = {
            "mobile_number": "03004567823"
        }
        self.admin = AdminFactory.create()
        path = '/staff/' + f'{self.admin.id}'
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_staff_list(self):

        path = '/staff'

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


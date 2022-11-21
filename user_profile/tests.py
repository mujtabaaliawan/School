from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, StaffFactory


class TestUser(APITestCase):

    def user_login(self, email, password):
        token_data = {
            'email': email,
            'password': password
        }
        token_path = "/token/get"
        access_token = self.client.post \
            (token_path, json.dumps(token_data), content_type='application/json').data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.login(email=email, password=password)
        self.assertEqual(response, True)

    def test_get_user_list(self):

        path = '/user'
        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('email'), self.admin.user.email)
        self.assertEqual(response.data[0].get('first_name'), self.admin.user.first_name)

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user(self):

        self.admin = StaffFactory.create()
        path = '/user/' + f'{self.admin.user.id}'

        test_data = {
            "first_name": "Khalid"
        }

        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('email'), self.admin.user.email)
        self.assertEqual(response.data.get('first_name'), test_data['first_name'])

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

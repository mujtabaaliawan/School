from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, AdminFactory


class TestStaff(APITestCase):

    def user_login(self, email, password):
        token_data = {
            'email': email,
            'password': password
        }
        token_path = "/get_token/"
        access_token = self.client.post \
            (token_path, json.dumps(token_data), content_type='application/json').data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.login(email=email, password=password)
        self.assertEqual(response, True)

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
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('Staff Email'), test_data['user'].get('email'))
        self.assertEqual(response.data.get('Staff Name'), test_data['user'].get('first_name'))
        self.assertEqual(response.data.get('Staff Mobile Number'), test_data['mobile_number'])

    def test_update_staff(self):
        test_data = {
            "mobile_number": "03004567823"
        }

        self.admin = AdminFactory.create()
        path = '/staff/' + f'{self.admin.id}'

        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('Staff Mobile Number'), test_data['mobile_number'])

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_staff_list(self):
        path = '/staff'

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Staff ID'), self.admin.id)
        self.assertEqual(response.data[0].get('Staff Email'), self.admin.user.email)
        self.assertEqual(response.data[0].get('Staff Name'), self.admin.user.first_name)
        self.assertEqual(response.data[0].get('Staff Mobile Number'), self.admin.mobile_number)

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Staff ID'), self.admin.id)
        self.assertEqual(response.data[0].get('Staff Email'), self.admin.user.email)
        self.assertEqual(response.data[0].get('Staff Name'), self.admin.user.first_name)
        self.assertEqual(response.data[0].get('Staff Mobile Number'), self.admin.mobile_number)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Staff ID'), self.admin.id)
        self.assertEqual(response.data[0].get('Staff Email'), self.admin.user.email)
        self.assertEqual(response.data[0].get('Staff Name'), self.admin.user.first_name)
        self.assertEqual(response.data[0].get('Staff Mobile Number'), self.admin.mobile_number)

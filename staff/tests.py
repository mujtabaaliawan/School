from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from staff.factories import TeacherFactory, StudentFactory, StaffFactory
import json


class TestStaff(APITestCase):

    def user_login(self, email, password):
        token_data = {
            'email': email,
            'password': password
        }
        token_path = reverse('token_new')
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
            "role": "staff",
            "mobile_number": "03009644678"
        }

        path = reverse('staff_new')

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('user').get('email'), test_data['user'].get('email'))
        self.assertEqual(response.data.get('user').get('first_name'), test_data['user'].get('first_name'))
        self.assertEqual(response.data.get('mobile_number'), test_data['mobile_number'])

    def test_update_staff(self):
        test_data = {
            "mobile_number": "03004567823"
        }

        self.admin = StaffFactory.create()
        path = reverse('staff_update', kwargs={'pk': self.admin.id})

        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('mobile_number'), test_data['mobile_number'])

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_staff_list(self):
        path = reverse('staff_list')

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('user').get('email'), self.admin.user.email)
        self.assertEqual(response.data[0].get('user').get('first_name'), self.admin.user.first_name)
        self.assertEqual(response.data[0].get('mobile_number'), self.admin.mobile_number)

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('user').get('email'), self.admin.user.email)
        self.assertEqual(response.data[0].get('user').get('first_name'), self.admin.user.first_name)
        self.assertEqual(response.data[0].get('mobile_number'), self.admin.mobile_number)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('user').get('email'), self.admin.user.email)
        self.assertEqual(response.data[0].get('user').get('first_name'), self.admin.user.first_name)
        self.assertEqual(response.data[0].get('mobile_number'), self.admin.mobile_number)

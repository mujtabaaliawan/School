from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from teacher.factories import TeacherFactory, StudentFactory, StaffFactory
import json


class TestTeacher(APITestCase):

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
        path = reverse('teacher_new')

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

    def test_update_teacher(self):

        test_data = {
            "mobile_number": "03004567823"
        }
        self.teacher = TeacherFactory.create()
        path = reverse('teacher_update', kwargs={'pk': self.teacher.id})

        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('mobile_number'), test_data['mobile_number'])

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_teacher_detail(self):

        self.teacher = TeacherFactory.create()
        path = reverse('teacher_update', kwargs={'pk': self.teacher.id})

        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('user').get('email'), self.teacher.user.email)
        self.assertEqual(response.data.get('user').get('first_name'), self.teacher.user.first_name)
        self.assertEqual(response.data.get('mobile_number'), self.teacher.mobile_number)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_teacher_list(self):

        path = reverse('teacher_list')

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('user').get('email'), self.teacher.user.email)
        self.assertEqual(response.data[0].get('user').get('first_name'), self.teacher.user.first_name)
        self.assertEqual(response.data[0].get('mobile_number'), self.teacher.mobile_number)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('user').get('email'), self.teacher.user.email)
        self.assertEqual(response.data[0].get('user').get('first_name'), self.teacher.user.first_name)
        self.assertEqual(response.data[0].get('mobile_number'), self.teacher.mobile_number)

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('user').get('email'), self.teacher.user.email)
        self.assertEqual(response.data[0].get('user').get('first_name'), self.teacher.user.first_name)
        self.assertEqual(response.data[0].get('mobile_number'), self.teacher.mobile_number)

from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, AdminFactory


class TestTeacher(APITestCase):

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

        self.assertEqual(response.data.get('Teacher Email'), test_data['user'].get('email'))
        self.assertEqual(response.data.get('Teacher Name'), test_data['user'].get('first_name'))
        self.assertEqual(response.data.get('Teacher Mobile Number'), test_data['mobile_number'])

    def test_update_teacher(self):

        test_data = {
            "mobile_number": "03004567823"
        }
        self.teacher = TeacherFactory.create()
        path = '/faculty/' + f'{self.teacher.id}'

        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('Teacher Mobile Number'), test_data['mobile_number'])

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_teacher_detail(self):

        self.teacher = TeacherFactory.create()
        path = '/faculty/' + f'{self.teacher.id}'

        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('Teacher Email'), self.teacher.user.email)
        self.assertEqual(response.data.get('Teacher Name'), self.teacher.user.first_name)
        self.assertEqual(response.data.get('Teacher Mobile Number'), self.teacher.mobile_number)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_teacher_list(self):

        path = '/faculty'

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Teacher ID'), self.teacher.id)
        self.assertEqual(response.data[0].get('Teacher Email'), self.teacher.user.email)
        self.assertEqual(response.data[0].get('Teacher Name'), self.teacher.user.first_name)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Teacher ID'), self.teacher.id)
        self.assertEqual(response.data[0].get('Teacher Email'), self.teacher.user.email)
        self.assertEqual(response.data[0].get('Teacher Name'), self.teacher.user.first_name)

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Teacher ID'), self.teacher.id)
        self.assertEqual(response.data[0].get('Teacher Email'), self.teacher.user.email)
        self.assertEqual(response.data[0].get('Teacher Name'), self.teacher.user.first_name)

    def test_get_teacher_detail_list(self):

        path = '/faculty/detail'

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Teacher ID'), self.teacher.id)
        self.assertEqual(response.data[0].get('Teacher Email'), self.teacher.user.email)
        self.assertEqual(response.data[0].get('Teacher Name'), self.teacher.user.first_name)
        self.assertEqual(response.data[0].get('Teacher Mobile Number'), self.teacher.mobile_number)

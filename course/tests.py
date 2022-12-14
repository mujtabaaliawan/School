from rest_framework.test import APITestCase
from rest_framework import status
import json
from django.urls import reverse
from .factories import TeacherFactory, StudentFactory, StaffFactory, CourseFactory


class TestCourse(APITestCase):

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

    def test_create_course(self):

        path = reverse('course_new')

        self.teacher = TeacherFactory.create()
        # teacher_data = {
        #     "id": self.teacher.id,
        #     "user": {
        #         "id": self.teacher.user.id,
        #         "email": self.teacher.user.email,
        #         "first_name": self.teacher.user.first_name,
        #         "password": 'teacher'
        #     },
        #     "role": self.teacher.role,
        #     "mobile_number": self.teacher.mobile_number
        # }
        # test_data = {
        #     "course_teacher": self.teacher,
        #     "course_title": "Django"
        #     }
        #
        # print(json.dumps(test_data))

        test_data = {
            "course_teacher_id": self.teacher.id,
            "course_title": "Django"
            }

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('course_title'), test_data['course_title'])
        self.assertEqual(response.data.get('course_teacher')['id'], self.teacher.id)

        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course(self):

        self.course = CourseFactory.create()

        test_data = {
            'course_title': 'Mathematics',
        }
        path = reverse('course_update', kwargs={'pk': self.course.id})

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('course_title'), test_data['course_title'])

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list(self):

        self.course = CourseFactory.create()
        path = reverse('course_list')

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('id'), self.course.id)
        self.assertEqual(response.data[0].get('course_title'), self.course.course_title)
        self.assertEqual(response.data[0].get('course_teacher').get('id'), self.course.course_teacher.id)
        self.assertEqual(response.data[0].get('course_teacher').get('user')['first_name'],
                         self.course.course_teacher.user.first_name)
        self.assertEqual(response.data[0].get('course_teacher').get('user')['email'],
                         self.course.course_teacher.user.email)

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('id'), self.course.id)
        self.assertEqual(response.data[0].get('course_title'), self.course.course_title)
        self.assertEqual(response.data[0].get('course_teacher').get('id'), self.course.course_teacher.id)
        self.assertEqual(response.data[0].get('course_teacher').get('user')['first_name'],
                         self.course.course_teacher.user.first_name)
        self.assertEqual(response.data[0].get('course_teacher').get('user')['email'],
                         self.course.course_teacher.user.email)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('id'), self.course.id)
        self.assertEqual(response.data[0].get('course_title'), self.course.course_title)
        self.assertEqual(response.data[0].get('course_teacher').get('id'), self.course.course_teacher.id)
        self.assertEqual(response.data[0].get('course_teacher').get('user')['first_name'],
                         self.course.course_teacher.user.first_name)
        self.assertEqual(response.data[0].get('course_teacher').get('user')['email'],
                         self.course.course_teacher.user.email)


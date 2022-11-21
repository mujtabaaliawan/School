from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, AdminFactory, CourseFactory


class TestCourse(APITestCase):

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

    def test_create_course(self):

        path = "/subject/new"

        self.teacher = TeacherFactory.create()
        test_data = {
            "course_title": "Mathematics",
            "course_teacher": self.teacher.id
            }

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('Course Title'), test_data['course_title'])
        self.assertEqual(response.data.get('Teacher ID'), test_data['course_teacher'])

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
        path = '/subject/' + f'{self.course.id}'

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('Course Title'), test_data['course_title'])

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list(self):

        self.course = CourseFactory.create()
        path = '/subject'

        self.admin = AdminFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Course ID'), self.course.id)
        self.assertEqual(response.data[0].get('Course Title'), self.course.course_title)
        self.assertEqual(response.data[0].get('Teacher ID'), self.course.course_teacher.id)
        self.assertEqual(response.data[0].get('Teacher Name'), self.course.course_teacher.user.first_name)
        self.assertEqual(response.data[0].get('Teacher Email'), self.course.course_teacher.user.email)

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Course ID'), self.course.id)
        self.assertEqual(response.data[0].get('Course Title'), self.course.course_title)
        self.assertEqual(response.data[0].get('Teacher ID'), self.course.course_teacher.id)
        self.assertEqual(response.data[0].get('Teacher Name'), self.course.course_teacher.user.first_name)
        self.assertEqual(response.data[0].get('Teacher Email'), self.course.course_teacher.user.email)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('Course ID'), self.course.id)
        self.assertEqual(response.data[0].get('Course Title'), self.course.course_title)
        self.assertEqual(response.data[0].get('Teacher ID'), self.course.course_teacher.id)
        self.assertEqual(response.data[0].get('Teacher Name'), self.course.course_teacher.user.first_name)
        self.assertEqual(response.data[0].get('Teacher Email'), self.course.course_teacher.user.email)

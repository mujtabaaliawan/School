from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, AdminFactory, CourseFactory


class TestCourse(APITestCase):

    def test_create_course(self):

        path = "/subject/new"

        self.teacher = TeacherFactory.create()
        test_data = {
            "course_title": "Mathematics",
            "course_teacher": self.teacher.id
            }

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course(self):

        self.course = CourseFactory.create()

        test_data = {
            'course_title': 'Mathematics',
        }
        path = '/subject/' + f'{self.course.id}'

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list(self):

        self.course = CourseFactory.create()
        path = '/subject'

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

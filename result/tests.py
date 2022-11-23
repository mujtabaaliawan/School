from rest_framework.test import APITestCase
from rest_framework import status
import json
from django.urls import reverse
from .factories import StaffFactory, CourseFactory
from .factories import EnrolledStudentFactory, ResultFactory


class TestResult(APITestCase):

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

    def test_create_result(self):

        self.course = CourseFactory.create()
        self.student = EnrolledStudentFactory.create(enrolled_course=self.course.id)

        test_data = {
            "student": self.student.id,
            "course": self.course.id,
            "score": 90
        }

        path = reverse('result_new')

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('student'), test_data.get('student'))
        self.assertEqual(response.data.get('course'), test_data.get('course'))
        self.assertEqual(response.data.get('score'), test_data.get('score'))

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_result(self):

        self.course = CourseFactory.create()
        self.student = EnrolledStudentFactory.create(enrolled_course=self.course.id)
        self.result = ResultFactory.create(course=self.course, student=self.student)

        test_data = {
            "student": self.result.student.id,
            "course": self.result.course.id,
            "score": 60.0
        }

        path = reverse('result_update', kwargs={'pk': self.result.id})

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('score'), test_data.get('score'))

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_result_list(self):

        self.course = CourseFactory.create()
        self.student = EnrolledStudentFactory.create(enrolled_course=self.course.id)
        self.result = ResultFactory.create(course=self.course, student=self.student)

        path = reverse('result_list')

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('student')['id'], self.result.student.id)
        self.assertEqual(response.data[0].get('course')['id'], self.result.course.id)
        self.assertEqual(response.data[0].get('score'), self.result.score)

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


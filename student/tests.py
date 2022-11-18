from rest_framework.test import APITestCase
from rest_framework import status
import json
from .test_factory import TeacherFactory, StudentFactory, AdminFactory, CourseFactory, EnrolledStudentFactory


class TestStudent(APITestCase):

    def test_create_student(self):

        path = "/student/new"

        test_data = {
            "user": {
                "email": "john@gmail.com",
                "first_name": "John",
                "password": "john"
            },
            "role": "student",
            "mobile_number": "03004567823"
        }

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student(self):

        self.student = StudentFactory.create()

        test_data = {
            'mobile_number': '0312765872',
        }
        path = '/student/' + f'{self.student.id}'

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_student_list(self):

        path = '/student'

        self.student = StudentFactory.create()
        self.client.login(email='student@gmail.com', password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher = TeacherFactory.create()
        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_student_enrollment(self):

        self.course = CourseFactory.create()
        self.student = StudentFactory.create()

        path = '/enrollment/' + f'{self.student.id}'

        test_data = {
            "enrolled_course": [self.course.id]
            }

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_student_enrollment(self):

        self.student = EnrolledStudentFactory.create()

        path = '/enrollment/update/' + f'{self.student.id}'

        test_data = {
            "enrolled_course": []
            }

        self.admin = AdminFactory.create()
        self.client.login(email='admin@gmail.com', password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.login(email='teacher@gmail.com', password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(email='student@gmail.com', password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

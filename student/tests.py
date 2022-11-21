from rest_framework.test import APITestCase
from rest_framework import status
import json
from student.test_factory import TeacherFactory, StudentFactory, StaffFactory, CourseFactory
from student.test_factory import CourseBulkFactory, EnrolledStudentFactory


class TestStudent(APITestCase):

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

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('Email'), test_data['user'].get('email'))
        self.assertEqual(response.data.get('Name'), test_data['user'].get('first_name'))
        self.assertEqual(response.data.get('Mobile Number'), test_data['mobile_number'])

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student(self):

        self.student = StudentFactory.create()

        test_data = {
            'mobile_number': '0312765872',
        }
        path = '/student/' + f'{self.student.id}'

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('Mobile Number'), test_data['mobile_number'])

    def test_get_student_list(self):

        path = '/student'

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('ID'), self.student.id)
        self.assertEqual(response.data[0].get('Email'), self.student.user.email)
        self.assertEqual(response.data[0].get('Name'), self.student.user.first_name)

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_student_enrollment(self):

        self.course = CourseFactory.create()
        self.student = StudentFactory.create()

        path = '/enrollment/' + f'{self.student.id}'

        test_data = {
            "enrolled_course": [self.course.id]
            }

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['Enrolled Courses'][1]['Course ID'], test_data['enrolled_course'][0])

    def test_update_clear_student_enrollment(self):

        self.course = CourseFactory.create()
        self.student = EnrolledStudentFactory.create(enrolled_course=self.course.id)

        test_data = {
            "enrolled_course": []
            }

        path = '/enrollment/update/' + f'{self.student.id}'

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['Number of Courses'], 0)

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_add_student_enrollment(self):

        self.course_one = CourseFactory.create()
        self.student = EnrolledStudentFactory.create(enrolled_course=self.course_one.id)
        self.course_two = CourseBulkFactory.create()

        test_data = {
            "enrolled_course": [self.course_one.id, self.course_two.id]
            }

        path = '/enrollment/update/' + f'{self.student.id}'

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['Enrolled Courses'][1]['Course ID'], test_data['enrolled_course'][0])
        self.assertEqual(response.data['Enrolled Courses'][2]['Course ID'], test_data['enrolled_course'][1])

        self.user_login(email=self.course_one.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

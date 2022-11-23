from rest_framework.test import APITestCase
from rest_framework import status
import json
from django.urls import reverse
from student.factories import TeacherFactory, StudentFactory, StaffFactory, CourseFactory
from student.factories import CourseBulkFactory, EnrolledStudentFactory


class TestStudent(APITestCase):

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

    def test_create_student(self):

        path = reverse('student_new')

        test_data = {
            "user": {
                "email": "john@gmail.com",
                "first_name": "John",
                "password": "john"
            },
            "role": "student",
            "mobile_number": "03004567823",
            "enrolled_course": []
        }

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.post(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('user')['email'], test_data['user'].get('email'))
        self.assertEqual(response.data.get('user')['first_name'], test_data['user'].get('first_name'))
        self.assertEqual(response.data.get('mobile_number'), test_data['mobile_number'])

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
        path = reverse('student_update', kwargs={'pk': self.student.id})

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

        self.assertEqual(response.data.get('mobile_number'), test_data['mobile_number'])

    def test_get_student_list(self):

        path = reverse('student_list')

        self.student = StudentFactory.create()
        self.user_login(email=self.student.user.email, password='student')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0].get('id'), self.student.id)
        self.assertEqual(response.data[0].get('user')['email'], self.student.user.email)
        self.assertEqual(response.data[0].get('user')['first_name'], self.student.user.first_name)

        self.teacher = TeacherFactory.create()
        self.user_login(email=self.teacher.user.email, password='teacher')
        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_enrollment(self):

        self.course = CourseFactory.create()
        self.student = StudentFactory.create()

        path = reverse('enrollment', kwargs={'pk': self.student.id})

        test_data = {
            "enrolled_course": [self.course.id]
            }

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('enrolled_course'), test_data['enrolled_course'])

        clear_data = {
            "enrolled_course": []
            }
        response = self.client.patch(path, json.dumps(clear_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('enrolled_course'), clear_data['enrolled_course'])

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('enrolled_course'), test_data['enrolled_course'])

    def test_clear_enrollment(self):

        self.course = CourseFactory.create()
        self.student = EnrolledStudentFactory.create(enrolled_course=self.course.id)

        test_data = {
            "enrolled_course": []
            }

        path = reverse('enrollment', kwargs={'pk': self.student.id})

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('enrolled_course'), test_data['enrolled_course'])

        self.user_login(email=self.course.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('enrolled_course'), test_data['enrolled_course'])

    def test_update_enrollment(self):

        self.course_one = CourseFactory.create()
        self.student = EnrolledStudentFactory.create(enrolled_course=self.course_one.id)
        self.course_two = CourseBulkFactory.create()

        test_data = {
            "enrolled_course": [self.course_one.id, self.course_two.id]
            }

        path = reverse('enrollment', kwargs={'pk': self.student.id})

        self.admin = StaffFactory.create()
        self.user_login(email=self.admin.user.email, password='admin')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('enrolled_course'), test_data['enrolled_course'])

        self.user_login(email=self.course_one.course_teacher.user.email, password='teacher')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user_login(email=self.student.user.email, password='student')
        response = self.client.patch(path, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('enrolled_course'), test_data['enrolled_course'])

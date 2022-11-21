import factory
from factory.django import DjangoModelFactory
from user_profile.models import User
from teacher.models import Teacher
from student.models import Student
from staff.models import Admin
from course.models import Course
from result.models import Result
from django.contrib.auth.hashers import make_password


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = 'Teacher'
    email = 'teacher@gmail.com'
    password = make_password('teacher')
    is_teacher = False
    is_student = False
    is_admin = False
    is_staff = True
    is_active = True


class TeacherFactory(DjangoModelFactory):
    class Meta:
        model = Teacher

    role = 'teacher'
    mobile_number = '0312121212'
    user = factory.SubFactory('student.test_factory.UserFactory', first_name='Teacher',
                              email='teacher@gmail.com', password=make_password('teacher'),
                              is_teacher=True)


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    role = 'student'
    mobile_number = '0313131313'
    user = factory.SubFactory('student.test_factory.UserFactory', first_name='Student',
                              email='student@gmail.com', password=make_password('student'),
                              is_student=True)


class AdminFactory(DjangoModelFactory):
    class Meta:
        model = Admin

    role = 'admin'
    mobile_number = '0314141414'
    user = factory.SubFactory('student.test_factory.UserFactory', first_name='Admin',
                              email='admin@gmail.com', password=make_password('admin'),
                              is_admin=True)


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = Course

    course_title = 'course'
    course_teacher = factory.SubFactory(TeacherFactory)


class EnrolledStudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    role = 'student'
    mobile_number = '0313131313'
    user = factory.SubFactory('student.test_factory.UserFactory', first_name='Student',
                              email='student@gmail.com', password=make_password('student'),
                              is_student=True)

    enrolled_course = factory.RelatedFactory(CourseFactory)

    @factory.post_generation
    def enrolled_course(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.enrolled_course.add(extracted)


class TeacherBulkFactory(DjangoModelFactory):
    class Meta:
        model = Teacher

    role = 'teacher'
    mobile_number = factory.Faker('phone_number')
    user = factory.SubFactory('student.test_factory.UserFactory', first_name=factory.Faker('name'),
                              email=factory.Faker('email'), password=make_password('teacher'),
                              is_teacher=True)


class CourseBulkFactory(DjangoModelFactory):
    class Meta:
        model = Course

    course_title = factory.Faker('name')
    course_teacher = factory.SubFactory(TeacherBulkFactory)


class ResultFactory(DjangoModelFactory):

    class Meta:
        model = Result

    course = factory.SubFactory(CourseFactory)
    student = factory.SubFactory(EnrolledStudentFactory)
    score = 90.0


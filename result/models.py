from django.db import models
from student.models import Student
from course.models import Course


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    score = models.FloatField()

    def __str__(self):
        return self.student.base_profile.email+' '+self.course.course_title

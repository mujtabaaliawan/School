from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('token/get', TokenObtainPairView.as_view(), name='token_new'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_update'),
    path('', include('user_profile.urls')),
    path('', include('teacher.urls')),
    path('', include('student.urls')),
    path('', include('staff.urls')),
    path('', include('course.urls')),
    path('', include('result.urls')),
]










"""""
router = DefaultRouter()

router.register('courses_list', course.views.CourseList.as_view(), basename='courses')
router.register('course_registration', course.views.CreateCourse.as_view(), basename='new_course')
router.register('teacher_list',teacher.views.TeacherListViewSet.as_view(), basename = 'teachers')
router.register('teacher_registration',teacher.views.CreateTeacherViewSet.as_view(), basename='new_teacher')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace= 'rest_framework'))
]
"""
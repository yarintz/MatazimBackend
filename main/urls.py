from django.urls import path
from rest_framework import routers
from django.conf.urls import include
# from .views import UserViewSet, CourseViewSet, LessonViewSet, UserCoursesViewSet,UserLessonsViewSet, UserProfileViewSet, ClassViewSet, SchoolViewSet, PlanViewSet, GroupViewSet, ForgetPasswordViewSet, FrontalLessonViewSet, FrontalCourseViewSet, UserFrontalCoursesViewSet, UserFrontalLessonsViewSet
from .views import *
# from .views import ResetPasswordView

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('courses', CourseViewSet)
router.register('lessons', LessonViewSet)
router.register('userCourses', UserCoursesViewSet)
router.register('userLessons', UserLessonsViewSet)
router.register('userProfile', UserProfileViewSet)
router.register('class', ClassViewSet)
router.register('school', SchoolViewSet)
router.register('plan', PlanViewSet)
router.register('group', GroupViewSet)
router.register('forgetPassword', ForgetPasswordViewSet)
router.register('frontalLesson', FrontalLessonViewSet)
router.register('frontalCourse', FrontalCourseViewSet)
router.register('userFrontalLessons', UserFrontalLessonsViewSet)
router.register('userFrontalCourses', UserFrontalCoursesViewSet)
router.register('classFrontalCourses', ClassFrontalCoursesViewSet)
router.register('frontalLessonFeedback', FrontalLessonFeedbackViewSet)
router.register('project', ProjectViewSet)
router.register('postImages', PostImagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
# urlpatterns = [
#     path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
# ]
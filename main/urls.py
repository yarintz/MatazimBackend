from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import UserViewSet, CourseViewSet, LessonViewSet, UserCoursesViewSet,UserLessonsViewSet, UserProfileViewSet, ClassViewSet, SchoolViewSet, PlanViewSet, GroupViewSet


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

urlpatterns = [
    path('', include(router.urls)),
]
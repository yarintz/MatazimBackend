from django.contrib import admin
from .models import Course, Lesson, UserCourses, UserLessons, UserProfile, Class, School , Plan, Group
# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(UserCourses)
admin.site.register(UserLessons)
admin.site.register(UserProfile)
admin.site.register(Class)
admin.site.register(School)
admin.site.register(Plan)
admin.site.register(Group)
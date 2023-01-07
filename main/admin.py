from django.contrib import admin
# from .models import Course, Lesson, UserCourses, UserLessons, UserProfile, Class, School , Plan, Group, FrontalLesson, FrontalCourse, UserFrontalCourses, UserFrontalLessons
from .models import *
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
admin.site.register(FrontalLesson)
admin.site.register(FrontalCourse)
admin.site.register(UserFrontalCourses)
admin.site.register(UserFrontalLessons)
admin.site.register(ClassFrontalCourses)
admin.site.register(FrontalLessonsFeedback)
# admin.site.register(MultipleImage)
class PostImageAdmin(admin.StackedInline):
    model = PostImages
 
@admin.register(Project)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]
 
    class Meta:
       model = Project
 
@admin.register(PostImages)
class PostImageAdmin(admin.ModelAdmin):
    pass
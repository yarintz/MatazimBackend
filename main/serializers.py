from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
# from .models import Course, Lesson, UserCourses, UserLessons ,UserProfile, Class, School ,Plan, Group, FrontalLesson, FrontalCourse, UserFrontalCourses, UserFrontalLessons

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('id', 'username', 'password', 'email','firstName', 'lastName')
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class PostImagesSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(many=True)
    class Meta:
        model = PostImages
        fields = ('id', 'images')


class ProjectSerializer(serializers.ModelSerializer):
    # images = PostImagestSerializer(many=True)
    class Meta:
        model = Project
        fields = ('id','user', 'title', 'briefDescription', 'link', 'description', 'approved', 'hide')  

# class PostImagesSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=True)
#     class Meta:
#         model = PostImages
#         fields = ('id', 'images', 'project')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields =  ('id', 'numOfLesson', 'name', 'link', 'assignment', 'course', 'answerType')

class FrontalLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontalLesson
        # fields = ('id', 'numOfLesson', 'name','description', 'presentation', 'frontalCourse') 
        fields = ('id', 'numOfLesson', 'name','description', 'presentation', 'frontalCourse') 
class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'lessons')

       
class FrontalCourseSerializer(serializers.ModelSerializer):
    frontalLessons = FrontalLessonSerializer(many=True)
    class Meta:
        model = FrontalCourse
        fields = ('id', 'name', 'description', 'frontalLessons')

class ClassFrontalCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassFrontalCourses
        fields = ('id', 'class', 'fronalCourse')

class UserCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourses
        fields = ('id', 'user', 'numOfLesson', 'course')

class UserLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLessons
        fields = ('id', 'user', 'answer','link','image','notes', 'lesson')

class UserFrontalCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFrontalCourses
        fields = ('id', 'user', 'numOfLesson', 'frontalCourse')

class FrontalLessonFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontalLessonsFeedback
        fields = ('id', 'user', 'frontalLesson','lessonClass', 'feedback')

class UserFrontalLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFrontalLessons
        fields = ('id', 'user', 'exercise','exerciseGrade','project','projectGrade', 'frontalLesson')
# class UserClassesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserClasses
#         fields = ('id', 'classname', 'numberofstudents')  

# class ClassSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Class
#         fields = ('id', 'className')  
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'className','school')  
        # fields = ('id', 'className')
class SchoolSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True)
    class Meta:
        model = School
        fields = ('id', 'schoolName','contact','contactPhone','comments', 'classes','plan')  

class PlanSerializer(serializers.ModelSerializer):
    schools = SchoolSerializer(many=True)
    class Meta:
        model = Plan
        fields = ('id', 'planName','schools')  

class GroupSerializer(serializers.ModelSerializer):
    # matatz = UserProfileSerializer(many=False)
    # groupStudents = UserProfileSerializer(many=True)
    class Meta:
        model = Group
        fields = ('id') 
        # fields = ('id', 'matatz','groupStudents') 


        
class UserProfileSerializer(serializers.ModelSerializer):
    studentClasses = ClassSerializer(many=True)
    matatzClasses = ClassSerializer(many=True)
    teacherClasses = ClassSerializer(many=True)
    coordinatorClasses = ClassSerializer(many=True)
    # mataz = UserProfileSerializer(many=False)
    # groupStudents = GroupSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ('id', 'user','username', 'firstName', 'lastName', 'aboutMe', 'hobbies', 'badges', 'myGoal','userType',
         'studentClasses','matatzClasses','teacherClasses', 'coordinatorClasses','mataz' )



                            
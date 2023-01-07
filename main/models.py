from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

TYPE_CHOICES = (("1", "student"),("2", "matatz"),("3", "teacher"),("4", "coordinator"),("5", "admin"),)
TYPE_OF_ANSWERS = (("1", "text"),("2", "link"),("3", "img"),)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username =  models.CharField(max_length=32)
    # email = models.CharField(max_length=32)
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)
    aboutMe = models.CharField(max_length=200,blank=True, null=True)
    hobbies = models.CharField(max_length=200,blank=True, null=True)
    badges = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(7)])
    myGoal = models.CharField(max_length=200,blank=True, null=True)
    mataz = models.ForeignKey(User, on_delete=models.CASCADE,related_name='matatz',blank=True, null=True)
    userType = models.CharField(
        max_length = 20,
        choices = TYPE_CHOICES,
        default = '1'
    )
    # classes = models.ManyToManyField(Class)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=360)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    numOfLesson = models.IntegerField()
    name = models.CharField(max_length=32)
    link = models.CharField(max_length=100)
    assignment = models.CharField(max_length=300)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    answerType = models.CharField(
        max_length = 20,
        choices = TYPE_OF_ANSWERS,
        default = '1'
    )
    class meta:
        unique_together = (('numOfLesson', 'course'),) 
        index_together = (('numOfLesson', 'course'),) 
def upload_presentaton(instance, filename):
    return '/'.join(['presentations', str(instance.name), filename])

class FrontalCourse(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=360,blank=True, null=True)

    def __str__(self):
        return self.name

class FrontalLesson(models.Model):
    numOfLesson = models.IntegerField()
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=360,blank=True, null=True,default='')
    presentation = models.FileField(blank=True, null=True, upload_to=upload_presentaton )
    frontalCourse = models.ForeignKey(FrontalCourse,blank=True, null=True, on_delete=models.CASCADE, related_name='frontalLessons')

class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    numOfLesson = models.IntegerField()
    class meta:
        index_together = (('numOfLesson', 'course', 'user'),) 

class UserFrontalCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frontalCourse = models.ForeignKey(FrontalCourse, on_delete=models.CASCADE)
    numOfLesson = models.IntegerField()
    class meta:
        index_together = (('numOfLesson', 'frontalCourse', 'user'),) 

def upload_path(instance, filename):
    return '/'.join(['answers', str(instance.user), filename])


class UserLessons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)
    link = models.URLField(max_length=200, blank=True, null=True, default=None)
    image = models.ImageField(blank=True, null=True, upload_to=upload_path )
    notes =  models.CharField(max_length=400)
    class meta:
        unique_together = (( 'lesson', 'user'),) 
        index_together = (( 'lesson', 'user'),) 

class UserFrontalLessons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frontalLesson = models.ForeignKey(FrontalLesson, on_delete=models.CASCADE)
    exercise = models.URLField(max_length=200, blank=True, null=True, default=None)
    exerciseGrade = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    project = models.URLField(max_length=200, blank=True, null=True, default=None)
    projectGrade = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    class meta:
        unique_together = (( 'frontalLesson', 'user'),) 
        index_together = (( 'frontalLesson', 'user'),) 



class Plan(models.Model):
    planName = models.CharField(max_length=32)
    # sdf = models.CharField(max_length=32)
    def __str__(self):
        return self.planName


class School(models.Model):
    schoolName = models.CharField(max_length=32)
    contact = models.CharField(max_length=32, blank=True, null=True, default=None)
    contactPhone = models.CharField(max_length=32, blank=True, null=True, default=None)
    comments = models.CharField(max_length=128, blank=True, null=True, default=None)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='schools', blank=True, null=True, default=None)

    def __str__(self):
        return self.schoolName

class Class(models.Model):
    className = models.CharField(max_length=32)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes', blank=True, null=True)
    # school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes', default='1')
    students = models.ManyToManyField(UserProfile, related_name='studentClasses')
    matazes = models.ManyToManyField(UserProfile, related_name='matatzClasses')
    teachers = models.ManyToManyField(UserProfile, related_name='teacherClasses')
    coordinators = models.ManyToManyField(UserProfile, related_name='coordinatorClasses')

    def __str__(self):
        return self.className

class FrontalLessonsFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frontalLesson = models.ForeignKey(FrontalLesson, on_delete=models.CASCADE)
    lessonClass = models.ForeignKey(Class, on_delete=models.CASCADE, default=None)
    feedback = models.TextField(blank=True, null=True, default=None)
    class meta:
        unique_together = (( 'frontalLesson', 'lessonClass'),) 
        index_together = (( 'frontalLesson', 'lessonClass'),) 

class ClassFrontalCourses(models.Model):
    frontalCourse = models.ForeignKey(FrontalCourse, on_delete=models.CASCADE)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)
    class meta:
        index_together = (('frontalCourse', 'classId'),) 

class Group(models.Model):
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='matatz')
    # user = models.OneToMany(UserProfile, on_delete=models.CASCADE,related_name='matatz')
    students = models.ManyToManyField(UserProfile, related_name='groupStudents')
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    title = models.CharField(max_length=32)
    briefDescription = models.CharField(null=True, blank=True, max_length=128)
    link = models.URLField(max_length=200, blank=True, null=True, default=None)
    description = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    # image = models.FileField(blank=True)
    # images = models.ManyToManyField(PostImages, related_name='images')
    def __str__(self):
        return self.title
 
class PostImages(models.Model):
    project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'projecttsImages/')
 
    def __str__(self):
        return self.project.title   
           
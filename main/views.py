from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication 
from django.contrib.auth.models import User 
# from .serializers import UserSerializer, CourseSerializer, LessonSerializer, UserCoursesSerializer, UserLessonsSerializer, UserProfileSerializer, ClassSerializer, SchoolSerializer, PlanSerializer, GroupSerializer, FrontalLessonSerializer, FrontalCourseSerializer, UserFrontalCoursesSerializer, UserFrontalLessonsSerializer
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
# from .models import Course, Lesson, UserCourses, UserLessons, UserProfile, Class, School , Plan, Group ,FrontalLesson, FrontalCourse, UserFrontalCourses, UserFrontalLessons
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.mail import send_mail
from django.http import JsonResponse
import hashlib
from django.contrib.auth.hashers import make_password
# from django.urls import reverse_lazy
# from django.contrib.auth.views import PasswordResetView
# from django.contrib.messages.views import SuccessMessageMixin

def blog_view(request):
    projects = Project.objects.all()
    return render(request, 'blog.html', {'projects':projects})
 
def detail_view(request, id):
    project = get_object_or_404(Project, id=id)
    photos = PostImages.objects.filter(project=project)
    return render(request, 'detail.html', {
        'project':project,
        'photos':photos
    })

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer 
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication, )
    parser_classes = (MultiPartParser,FormParser, JSONParser)

    # get all the projects that have been aproved for displaying
    @action (detail=True, methods = ['GET'])
    def getAprrovedProject(self, request, pk=None):
        print("inside getAprrovedProject!")
        allAprovedProject =[]
        projects= Project.objects.filter(approved=True) 
        print("im okay")
        for project in projects:
                 serializers = ProjectSerializer(project, many=False)
                 allAprovedProject.append(serializers.data)   
        response = {'message': 'found', 'results': allAprovedProject }
        return Response (response, status=status.HTTP_200_OK)

    # get all the projects that have not been approved yet
    @action (detail=True, methods = ['GET'])
    def getNotAprrovedProject(self, request, pk=None):
        print("inside getNotAprrovedProject!")
        allNotAprovedProject =[]
        projects= Project.objects.filter(approved=False) 
        print("im okay")
        for project in projects:
                 serializers = ProjectSerializer(project, many=False)
                 allNotAprovedProject.append(serializers.data)   
        response = {'message': 'found', 'results': allNotAprovedProject }
        return Response (response, status=status.HTTP_200_OK)

    # get all the projects that have not been approved yet and belongs to the user
    @action (detail=True, methods = ['GET'])
    def getallUnApprovedProjectOfUser(self, request, pk=None):
        print("inside getallUnApprovedProjectOfUser!")
        # get the user by token
        user = request.user  
        print(user)
        allNotAprovedProjectOfUser =[]
        projects= Project.objects.filter(approved=False, user=user) 
        print("im okay")
        for project in projects:
                 serializers = ProjectSerializer(project, many=False)
                 allNotAprovedProjectOfUser.append(serializers.data)   
        response = {'message': 'found', 'results': allNotAprovedProjectOfUser }
        return Response (response, status=status.HTTP_200_OK)

    # set project to be approved
    @action (detail=True, methods = ['POST'])
    def ApproveProject(self, request, pk=None):
        project = Project.objects.get(id=pk)
        project.approved = True
        project.save()

        serializers = ProjectSerializer(project, many=False)
        response = {'message': 'Updated', 'results': serializers.data }
        return Response (response, status=status.HTTP_200_OK)

    # set project to be hide which means it can not also be "approved"
    @action (detail=True, methods = ['POST'])
    def HideProject(self, request, pk=None):
        project = Project.objects.get(id=pk)
        project.hide = True
        project.approved = False
        project.save()

        serializers = ProjectSerializer(project, many=False)
        response = {'message': 'Updated', 'results': serializers.data }
        return Response (response, status=status.HTTP_200_OK)


    # create a project 
    @action (detail=True, methods = ['POST'])
    def createProject(self, request, pk=None):
        print("inside create project!")
        # get the user who create the project by token
        user = request.user  
        print(user)
        # The other parameters of project
        title = ' '
        briefDescription = ' '
        link = ' '
        description = ' '
        if 'title' in request.data:
            print("first if")
            title = request.data['title']
            print("im okay title")
        if 'briefDescription' in request.data:
            briefDescription = request.data['briefDescription']
            print("im okay briefDescription")
        if 'link' in request.data:
            link = request.data['link']
            print("im okay link")
        if 'description' in request.data:
            description = request.data['description']
            print("im okay description")
        print("also here")

        newProject = Project.objects.create(user = user, title=title, briefDescription=briefDescription, link=link,description=description, approved = False, hide = False)
        newProject.save()
        print("project is: ", newProject.id)
           
        response = {'message': 'created', 'results': newProject.id }
        return Response (response, status=status.HTTP_200_OK)
    
    #update the project 
    @action (detail=True, methods = ['POST'])
    def UpdateProject(self, request, pk=None):     
        # if getProject get a value (len(getProject) > 0) it means that 
        # this object exist in DB and the user is trying to update that object.
        getProject= Project.objects.get(id=pk)           
        try:
            # success if need to update  
  
            # get the new details
            title = request.data['title']
            briefDescription = request.data['briefDescription']
            description = request.data['description']
            link = request.data['link']
            #insert the new details in the new object
            getProject.title = title
            getProject.briefDescription = briefDescription
            getProject.description = description
            getProject.link = link
            getProject.approved = False

            getProject.save()
            print ("new project is: ", Project)
            serializers = ProjectSerializer(getProject, many=False)
            response = {'message': 'Updated', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)
        except:
            #requested profile not found in DB
            response = {'message': 'error'}
            return Response (response, status=status.HTTP_200_OK)

    # @action (detail=True, methods = ['GET'])
    # def getProjectImages(self, request, pk=None):
    #     print(pk)
    #     project= Project.objects.get(id=pk)
    #     # for userCourse in userCourses:
    #     #         serializers = UserCoursesSerializer(userCourse, many=False)
    #     #         arr.append(serializers.data)
    #     print("done")
    #     print(project.id)
    #     print(project.PostImages)
    #     print(project)


    #     response = {'message': 'found', 'results': project }
    #     return Response (response, status=status.HTTP_200_OK)

class PostImagesViewSet(viewsets.ModelViewSet):
    queryset = PostImages.objects.all()
    serializer_class = PostImagesSerializer 
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser,FormParser, JSONParser) 

    # get all images of specific project (pk is project id)
    @action (detail=True, methods = ['GET'])
    def getProjectImages(self, request, pk=None):
        postImages={}
        postImages= PostImages.objects.all()
        print(type(pk))
        images=[]
        for postImage in postImages:
                serializers = PostImagesSerializer(postImage, many=False)
                print(type(postImage.project.id))
                if(str(postImage.project.id)==pk):
                    print("inside if")
                    images.append(serializers.data)
        print("done")
        print(images)



        response = {'message': 'found', 'results': images }
        return Response (response, status=status.HTTP_200_OK)

    # add images to project
    @action (detail=True, methods = ['POST'])
    def addProjectImage(self, request, pk=None, format=None):
        print("im in add project image")
        # get the project instance by project id (pk)
        project = Project.objects.get(id=pk)
        print("project is: ", project)
        
        # get the image
        if 'img' in request.data: 
            print("there is an image")
            image = request.data['img']
            print("img is: ", image)
            projectImage = PostImages.objects.create(project = project, images= image)
            projectImage.save()
            print("projectImage is: ", projectImage)
        else:
            print("ffffff")  
            projectImage = PostImages.objects.create(project = project, images= None)
            projectImage.save() 
        response = {'message': 'created', 'results': projectImage }
        return Response (response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = (AllowAny,)

    @action (detail=True, methods = ['POST'])
    def getuser(self, request, pk=None):
        user = User.object.get(id=pk)
    
    # @action (detail=True, methods = ['POST'])
    # def getUserDetails(self, request, pk=None):
    #         print("im here in get user details")
    #         user = request.user
    #         print("user from query is: ", user)
    #         arr=[]
    #         u = User.objects.get(username='yarinAAA')
    #         print("user mail is: ", u.email)
    #         print("user name is: ", u.name)
    #         print("user surname is: ", u.lastName)
    #         userDetails= User.objects.filter(user=user.id, course=pk)
    #         for userCourse in userCourses:
    #             serializers = UserCoursesSerializer(userCourse, many=False)
    #             arr.append(serializers.data)
                
    #         response = {'message': 'Get', 'results': arr }
    #         return Response (response, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer 
    authentication_classes = (TokenAuthentication, )
    
    @action (detail=True, methods = ['POST'])
    def createUserProfile(self, request, pk=None):
        print("inside create user profile")
        # get the given username
        username = request.data['username']  
        # get the user from DB  by the given username
        getUser= User.objects.filter(username=username) 
        # get the values of first name and last name
        givenFirstName = ' '
        givenLastName = ' '
        if 'firstName' in request.data:
            givenFirstName = request.data['firstName']
        if 'lastName' in request.data:
            givenLastName = request.data['lastName']


        newUser = UserProfile.objects.create(user=getUser[0], username=username, firstName=givenFirstName,lastName=givenLastName,aboutMe= ' ', hobbies = ' ', badges=0, myGoal= '' )
        newUser.save()
        print("user is: ", newUser)
           
        response = {'message': 'created', 'results': newUser }
        return Response (response, status=status.HTTP_200_OK)


    @action (detail=True, methods = ['POST'])
    def getUserByUsername(self, request, pk=None):
            username = request.data['username']
            arr=[]
            u = UserProfile.objects.get(username=username)
           
            serializers = UserProfileSerializer(u, many=False)
            
                
            response = {'message': 'Get', 'results': serializers.data }
            print("response:", response)
            return Response (response, status=status.HTTP_200_OK)

     # get the user profile object by the user id in users table (not userProfile table)
    @action (detail=True, methods = ['GET'])
    def getUserProfileByUserId(self, request, pk=None):
            # pk is the user id
            user = UserProfile.objects.get(user=pk)
            serializers = UserProfileSerializer(user, many=False)
                
            response = {'message': 'Get', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)

    @action (detail=True, methods = ['POST'])
    def getUserDetails(self, request, pk=None):
            print("im here")
            user = request.user
            print("user from query is: ", user)
            arr=[]
            u = UserProfile.objects.get(user=user)
            # print("user mail is: ", u.email)
            print("user name is: ", u.firstName)
            print("user surname is: ", u.lastName)
            # userDetails= User.objects.filter(user=user.id, course=pk)
            # for userCourse in userCourses:
            u.username=user
            serializers = UserProfileSerializer(u, many=False)
            #     arr.append(serializers.data)
                
            response = {'message': 'Get', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)


#update the user's profile details 
    @action (detail=True, methods = ['POST'])
    def UpdateUserDetails(self, request, pk=None):
        
        # get the user by the authentication
        user = request.user
        # if getUserProfile get a value (len(getUserProfile) > 0) it means that 
        # this object exist in DB and the user is trying to update that object.
        getUserProfile= UserProfile.objects.filter(user=user.id)            
        try:
            # success if need to update 
            
            profile = UserProfile.objects.get(id=getUserProfile[0].id)
            print("aaabbb ",getUserProfile[0].id)
            profile.user = user
            # get the new details
            firstName = request.data['firstName']
            lastName = request.data['lastName']
            aboutMe = request.data['aboutMe']
            hobbies = request.data['hobbies']
            myGoal = request.data['myGoal']
            #insert the new details in the new object
            profile.firstName = firstName
            profile.lastName = lastName
            profile.aboutMe = aboutMe
            profile.hobbies = hobbies
            profile.myGoal = myGoal
           
            
            profile.save()
            print ("new profile is: ", profile)
            serializers = UserProfileSerializer(profile, many=False)
            response = {'message': 'Updated', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)
        except:
            #requested profile not found in DB
            response = {'message': 'error'}
            return Response (response, status=status.HTTP_200_OK)

    # get all the teacher registered in the system
    @action (detail=True, methods = ['GET'])
    def getAllTeachers(self, request, pk=None):
        arr=[]
        teachers= UserProfile.objects.filter(userType=3)
        for teacher in teachers:
            serializers = UserProfileSerializer(teacher, many=False)
            arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)     
            
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer    

class FrontalLessonViewSet(viewsets.ModelViewSet):
    queryset = FrontalLesson.objects.all()
    serializer_class = FrontalLessonSerializer    
    parser_classes = (MultiPartParser,FormParser, JSONParser) 
    #  Update presentation for frontal lesson 
    @action (detail=True, methods = ['POST'])
    def updateLessonPresentation(self, request, pk=None, format=None):
        print("here")
        lesson = FrontalLesson.objects.get(id=pk)
        # lesson= FrontalLesson.objects.filter(id=pk)    
        print("lesson.name") 
        print(lesson)  
        print(lesson.name)
        if 'presentation' in request.data:
            print("here2")
            presentation = request.data['presentation']



            print(presentations)
            lesson.presentation = presentations    
        lesson.save()        
        serializers = FrontalLessonSerializer(lesson, many=False)
        response = {'message': 'Updated', 'results': serializers.data }
        return Response (response, status=status.HTTP_200_OK)
        
          



class UserCoursesViewSet(viewsets.ModelViewSet):
    queryset = UserCourses.objects.all()
    serializer_class = UserCoursesSerializer 
    authentication_classes = (TokenAuthentication, )

# get all the courses belongs to the user by the user Id
    @action (detail=True, methods = ['GET'])
    def getAllCoursesByUserId(self, request, pk=None):
        # get the user by the pk
        user = pk
        arr=[]
        userCourses= UserCourses.objects.filter(user=user)
        for userCourse in userCourses:
            serializers = UserCoursesSerializer(userCourse, many=False)
            arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

# get all the courses belongs to the user by the token
    @action (detail=True, methods = ['POST'])
    def getAllUserCourses(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        arr=[]
        userCourses= UserCourses.objects.filter(user=user.id)
        for userCourse in userCourses:
            serializers = UserCoursesSerializer(userCourse, many=False)
            arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

    @action (detail=True, methods = ['POST'])
    def getUserCourses(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        arr=[]
        userCourses= UserCourses.objects.filter(user=user.id, course=pk)
        for userCourse in userCourses:
            serializers = UserCoursesSerializer(userCourse, many=False)
            arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

    #  Update or create a userLessons 
    @action (detail=True, methods = ['POST'])
    def addUserCourses(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        # if addUserCourses get a value (len(getUserLessons) > 0) it means that 
        # this object exist in DB and the user is trying to update that object.
        getUserCourses= UserCourses.objects.filter(user=user.id, course=pk)       
                
        try:
            # success if need to update 
            course = UserCourses.objects.get(id=getUserCourses[0].id)
            # print("printing: ",lesson.notes, lesson.answer)
            course.user = user
            # user trying to change the lesson
            if 'lesson' in request.data:
                lesson = request.data['lesson']
                course.numOfLesson = lesson
           
            
            course.save()
            print ("user is: ", user)
            serializers = UserCoursesSerializer(course, many=False)
            response = {'message': 'Updated', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)
        except:
            # need to create
            print("trying to create")
            print("pk ", pk)
            # user began a new course
            if 'lesson' in request.data:
                lesson = request.data['lesson']
           
               
            course = Course.objects.get(id=pk)
            courseVar = UserCourses.objects.create(user=user, course=course, numOfLesson=int(lesson))
            courseVar.save()
            print("course is: ", course)
            print(lesson)
            print(type(lesson))
            response = {'message': 'created', 'results': courseVar }
            return Response (response, status=status.HTTP_200_OK)

class UserFrontalCoursesViewSet(viewsets.ModelViewSet):
    queryset = UserFrontalCourses.objects.all()
    serializer_class = UserFrontalCoursesSerializer 
    authentication_classes = (TokenAuthentication, )

# get all the courses belongs to the user by the user Id
    @action (detail=True, methods = ['GET'])
    def getAllCoursesByUserId(self, request, pk=None):
        # get the user by the pk
        user = pk
        arr=[]
        userCourses= UserFrontalCourses.objects.filter(user=user)
        for userCourse in userCourses:
            serializers = UserFrontalCoursesSerializer(userCourse, many=False)
            arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

# get all the courses belongs to the user by the token
    @action (detail=True, methods = ['POST'])
    def getAllUserFrontalCourses(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        arr=[]
        userCourses= UserFrontalCourses.objects.filter(user=user.id)
        for userCourse in userCourses:
            serializers = UserCoursesSerializer(userCourse, many=False)
            arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

    @action (detail=True, methods = ['POST'])
    def getUserFrontalCourses(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        arr=[]
        userCourses= UserFrontalCourses.objects.filter(user=user.id, course=pk)
        for userCourse in userCourses:
            serializers = UserFrontalCoursesSerializer(userCourse, many=False)
            arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

    #  Update or create a userLessons 
    @action (detail=True, methods = ['POST'])
    def addUserFrontalCourses(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        # if addUserFrontalCourses get a value (len(getUserLessons) > 0) it means that 
        # this object exist in DB and the user is trying to update that object.
        getUserCourses= UserFrontalCourses.objects.filter(user=user.id, course=pk)       
                
        try:
            # success if need to update 
            course = UserFrontalCourses.objects.get(id=getUserCourses[0].id)
            # print("printing: ",lesson.notes, lesson.answer)
            course.user = user
            # user trying to change the lesson
            if 'lesson' in request.data:
                lesson = request.data['lesson']
                course.numOfLesson = lesson
           
            
            course.save()
            print ("user is: ", user)
            serializers = UserFrontalCoursesSerializer(course, many=False)
            response = {'message': 'Updated', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)
        except:
            # need to create
            print("trying to create")
            print("pk ", pk)
            # user began a new course
            if 'lesson' in request.data:
                lesson = request.data['lesson']
           
               
            course = FrontalCourse.objects.get(id=pk)
            courseVar = UserFrontalCourses.objects.create(user=user, course=course, numOfLesson=int(lesson))
            courseVar.save()
            print("course is: ", course)
            print(lesson)
            print(type(lesson))
            response = {'message': 'created', 'results': courseVar }
            return Response (response, status=status.HTTP_200_OK)

class FrontalLessonFeedbackViewSet(viewsets.ModelViewSet):
    queryset = FrontalLessonsFeedback.objects.all()
    serializer_class = FrontalLessonFeedbackSerializer 
    authentication_classes = (TokenAuthentication, )

    #  Update or create a feedback 
    @action (detail=True, methods = ['POST'])
    def addFeedback(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        #get the class related to this feedback
        # if 'class' in request.data:
        classId = request.data['class']
        print(classId)
        print("finish")
        # if getFeedback get a value (len(getUserLessons) > 0) it means that 
        # this object exist in DB and the user is trying to update that object.
        getFeedback= FrontalLessonsFeedback.objects.filter(frontalLesson=pk, lessonClass=classId, user=user)       
                
        try:
            # success if need to update 
            feedback = FrontalLessonsFeedback.objects.get(id=getFeedback[0].id)
            # print("printing: ",lesson.notes, lesson.answer)
            # course.user = user
            # user trying to change the lesson
            if 'feedback' in request.data:
                newFeedback = request.data['feedback']
                feedback.feedback = newFeedback
           
            
            feedback.save()
            print ("user is: ", user)
            serializers = FrontalLessonFeedbackSerializer(feedback, many=False)
            response = {'message': 'Updated', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)
        except:

            # user began a new course
            if 'feedback' in request.data:
                newFeedback = request.data['feedback']
           
               
            lesson = FrontalLesson.objects.get(id=pk)
            classObj = Class.objects.get(id=classId)
            feedbackObject = FrontalLessonsFeedback.objects.create(user=user, frontalLesson=lesson,lessonClass=classObj, feedback=newFeedback)
            feedbackObject.save()
           
            response = {'message': 'created', 'results': feedbackObject }
            return Response (response, status=status.HTTP_200_OK)

    @action (detail=True, methods = ['POST'])
    def getAllFeedbacks(self, request, pk=None):
        classId = request.data['class']
        arr=[]
        feedbacks= FrontalLessonsFeedback.objects.filter(frontalLesson=pk, lessonClass=classId)
        for feedback in feedbacks:
            serializers = FrontalLessonFeedbackSerializer(feedback, many=False)
            arr.append(serializers.data)   
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)
        
class UserLessonsViewSet(viewsets.ModelViewSet):
    queryset = UserLessons.objects.all()
    serializer_class = UserLessonsSerializer   
    parser_classes = (MultiPartParser,FormParser, JSONParser) 
    # parser_classes = (MultiPartParser, )   
    authentication_classes = (TokenAuthentication, )
    
    # #  Get all the userLessons details belonged to the requsted user by the authentication
    # @action (detail=True, methods = ['GET'])
    # def getUserLessons(self, request, pk=None):
    #     # get the user by the authentication
    #     user = request.user
    #     arr=[]
    #     userlessons= UserLessons.objects.filter(user=user.id)
    #     for userlesson in userlessons:
    #          serializers = UserLessonsSerializer(userlesson, many=False)
    #          arr.append(serializers.data)
            
    #     response = {'message': 'Get', 'results': arr }
    #     return Response (response, status=status.HTTP_200_OK)

 #  Get all the userLessons details belongs to the requsted user by the authentication
    @action (detail=True, methods = ['POST'])
    def getUserLessons(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        # lessonID = '4'
        if 'lesson' in request.data:
            lessonID = request.data['lesson']
        # else:
            # lessonID=4
        arr=[]
        userlessons= UserLessons.objects.filter(user=user.id, lesson=lessonID)
        for userlesson in userlessons:
             serializers = UserLessonsSerializer(userlesson, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

#  Get all the objects of UserLessons (include answers) belongs to the requsted user by his ID
    @action (detail=True, methods = ['POST'])
    def getUserAnswers(self, request, pk=None):
        # get the requested user
        if 'userId' in request.data:
            userID = request.data['userId']
            lessonID = request.data['lessonId']
        arr=[]
        userlessons= UserLessons.objects.filter(user=userID, lesson=lessonID)
        for userlesson in userlessons:
             serializers = UserLessonsSerializer(userlesson, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)


    #  Update or create a userLessons 
    @action (detail=True, methods = ['POST'])
    def addUserLessons(self, request, pk=None, format=None):
        # get the user by the authentication
        user = request.user
        # if getUserLessons get a value (len(getUserLessons) > 0) it means that 
        # this object exist in DB and the user is trying to update that object.
        getUserLessons= UserLessons.objects.filter(user=user.id, lesson=pk)       
                
        try:
            # success if need to update 
            # print("success 1")
            lesson = UserLessons.objects.get(id=getUserLessons[0].id)
            print("success 2")
            lesson.user = user
            # print(request.data['notes'])
            print("success 3")
            
            # user trying to change the note
            if 'notes' in request.data:
                print("needs to upfate a note") 
                notes = request.data['notes']             
                lesson.notes = notes
                print("the note is: ", notes)
            else:
                print("notes is not in request data")
             # user trying to change the answer
            if 'answer' in request.data:
                answer = request.data['answer']
                link = request.data['link']
                image = request.data['image']
                # .parser_classes(MultiPartParser,)
                print("needs to update the answer!")
                print(answer)
                print(link)
                print(image)
                # print(request.data['image'])
                lesson.answer = answer
                lesson.link = link
                lesson.image = image
                
            lesson.save()
            print ("user is: ", user)
            serializers = UserLessonsSerializer(lesson, many=False)
            response = {'message': 'Updated', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)
        except:
            # need to create
            print("trying to create 2")
            print("pk ", pk)
            # user trying to create a note
            if 'notes' in request.data:
                notes = request.data['notes']
                answer = ""
                link = ""
                image = ""
            # user trying to create an answer
            if 'answer' in request.data:
                answer = request.data['answer']
                print("i'm ok 1")
                link = request.data['link']
                print("i'm ok 2")
                image = request.data['image']
                # .parser_classes(MultiPartParser,)
                print("i'm ok 3")
                notes = ""
            print("i'm ok 4")   
            lesson = Lesson.objects.get(id=pk)
            lessonVar = UserLessons.objects.create(user=user,lesson=lesson, answer=answer,link=link, image=image, notes=notes )
            lessonVar.save()
            response = {'message': 'created', 'results': lessonVar }
            return Response (response, status=status.HTTP_200_OK)

class UserFrontalLessonsViewSet(viewsets.ModelViewSet):
    queryset = UserFrontalLessons.objects.all()
    serializer_class = UserFrontalLessonsSerializer   
    parser_classes = (MultiPartParser,FormParser, JSONParser) 
    # parser_classes = (MultiPartParser, )   
    authentication_classes = (TokenAuthentication, )
     

 #  Get all the userLessons details belongs to the requsted user by the authentication
    @action (detail=True, methods = ['POST'])
    def getUserFrontalLessons(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        if 'lesson' in request.data:
            lessonID = request.data['lesson']
        arr=[]
        userlessons= UserFrontalLessons.objects.filter(user=user.id, frontalLesson=lessonID)
        for userlesson in userlessons:
             serializers = UserFrontalLessonsSerializer(userlesson, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

 #  Get all the userLessons details belongs to the requsted user by the authentication
    @action (detail=True, methods = ['POST'])
    def getUserFrontalLessonsByLesson(self, request, pk=None):
        # if 'lesson' in request.data:
        #     lessonID = request.data['lesson']
        lessonID = pk 
        arr=[]
        userlessons= UserFrontalLessons.objects.filter(frontalLesson=lessonID)
        for userlesson in userlessons:
             serializers = UserFrontalLessonsSerializer(userlesson, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

#  Get all the objects of UserFrontalLessons (include links fro exercise and project) belongs to the requsted user by his ID
    @action (detail=True, methods = ['POST'])
    def getUserAnswers(self, request, pk=None):
        # get the requested user
        if 'userId' in request.data:
            userID = request.data['userId']
            lessonID = request.data['lessonId']
        arr=[]
        userlessons= UserFrontalLessons.objects.filter(user=userID, frontalLesson=lessonID)
        for userlesson in userlessons:
             serializers = UserFrontalLessonsSerializer(userlesson, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)


    #  Update or create a UserFrontalLessons 
    @action (detail=True, methods = ['POST'])
    def addUserFrontalLessons(self, request, pk=None, format=None):
        # get the user by the authentication
        user = request.user
        print(user)
        # if getUserLessons get a value (len(getUserLessons) > 0) it means that 
        # this object exist in DB and the user is trying to update that object.
        getUserLessons= UserFrontalLessons.objects.filter(user=user.id, frontalLesson=pk)       
        print(getUserLessons)      
        try:
            # success if need to update 
            lesson = UserFrontalLessons.objects.get(id=getUserLessons[0].id)
            print("success")
            lesson.user = user

            
            # user trying to change the exercise ilnk
            if 'exercise' in request.data:
                print("needs to update a exercise") 
                exercise = request.data['exercise']             
                lesson.exercise = exercise
                print("the note is: ", exercise)
            else:
                print("exercise is not in request data")
             # user trying to change the project link
            if 'project' in request.data:
                project = request.data['project']
                print("needs to update the project!")
                print(project)
                lesson.project = project

                
            lesson.save()
            print ("user is: ", user)
            serializers = UserFrontalLessonsSerializer(lesson, many=False)
            response = {'message': 'Updated', 'results': serializers.data }
            return Response (response, status=status.HTTP_200_OK)
        except:
            # need to create
            print("trying to create 2")
            print("pk ", pk)
            exercise = ""
            exerciseGrade = 0
            project = ""
            projectGrade = 0
            # user trying to create a note
            if 'exercise' in request.data:
                exercise = request.data['exercise']
            # user trying to create an answer
            if 'project' in request.data:
                project = request.data['project']

            print("i'm ok 4")   
            lesson = FrontalLesson.objects.get(id=pk)
            lessonVar = UserFrontalLessons.objects.create(user=user,frontalLesson=lesson, exercise=exercise,exerciseGrade=exerciseGrade, project=project, projectGrade=projectGrade )
            lessonVar.save()
            response = {'message': 'created', 'results': lessonVar }
            return Response (response, status=status.HTTP_200_OK)

    #  Update user's grade for frontal lesson
    @action (detail=True, methods = ['POST'])
    def updateUserGrade(self, request, pk=None):
        print(pk)
        userFrontalLesson= UserFrontalLessons.objects.get(id=pk)       
        print(userFrontalLesson.id)

        # teste = request.data['exercise']
        # print(teste)
        print("whattt")
        if 'exercise' in request.data:
            print("exercise")
            exercise = request.data['exercise']
            print(exercise)
            userFrontalLesson.exerciseGrade = exercise
        if 'project' in request.data:
            print("project")
            project = request.data['project']
            print(project)
            userFrontalLesson.projectGrade = project
           
        userFrontalLesson.save()
        serializers = UserFrontalLessonsSerializer(userFrontalLesson, many=False)
        response = {'message': 'Updated', 'results': serializers.data }
        return Response (response, status=status.HTTP_200_OK)
        

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer 

    @action (detail=True, methods = ['POST'])
    def addSchool(self, request, pk=None):
        # get the School data
        schoolName = request.data['schoolName']
        contact = request.data['contact']
        contactPhone = request.data['contactPhone']
        comments = request.data['comments']

        # create a new school with the given name
        newSchool = School.objects.create(schoolName=schoolName, contact=contact,contactPhone=contactPhone, comments=comments )
        newSchool.save()
        response = {'message': 'Updated', 'results': newSchool }
        return Response (response, status=status.HTTP_200_OK)   


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer 
    parser_classes = (MultiPartParser,FormParser, JSONParser)
    authentication_classes = (TokenAuthentication, )
    # get all the students of a class
    @action (detail=True, methods = ['POST'])
    def getClassStudents(self, request, pk=None):
     
        arr=[]
        userProfile= UserProfile.objects.filter(studentClasses=pk)
        for userProfile in userProfile:
             serializers = UserProfileSerializer(userProfile, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

    # get all the teachers of a class
    @action (detail=True, methods = ['POST'])
    def getClassTeachers(self, request, pk=None):
     
        arr=[]
        userProfile= UserProfile.objects.filter(teacherClasses=pk)
        for userProfile in userProfile:
             serializers = UserProfileSerializer(userProfile, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

    # get all the matatzes of a class
    @action (detail=True, methods = ['POST'])
    def getClassMatatzes(self, request, pk=None):
     
        arr=[]
        userProfile= UserProfile.objects.filter(matatzClasses=pk)
        for userProfile in userProfile:
             serializers = UserProfileSerializer(userProfile, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

     # get all the coordinators of a class
    @action (detail=True, methods = ['POST'])
    def getClassCoordinators(self, request, pk=None):
     
        arr=[]
        userProfile= UserProfile.objects.filter(coordinatorClasses=pk)
        for userProfile in userProfile:
             serializers = UserProfileSerializer(userProfile, many=False)
             arr.append(serializers.data)
            
        response = {'message': 'Get', 'results': arr }
        return Response (response, status=status.HTTP_200_OK)

    #  Add a user to class 
    @action (detail=True, methods = ['POST'])
    def addUserToClass(self, request, pk=None):
        # get the class by pk
        getUserClass= Class.objects.get(id=pk)  

        # trying to add a student
        if 'student' in request.data:   
            # get the username by the data
            username = request.data['student']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.students.add(user)

        # trying to add a matatz
        if 'matatz' in request.data:   
            # get the username by the data
            username = request.data['matatz']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.matatzes.add(user)

        # trying to add a teacher
        if 'teacher' in request.data:   
            # get the username by the data
            username = request.data['teacher']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.teachers.add(user)

         # trying to add a coordinator
        if 'coordinator' in request.data:   
            # get the username by the data
            username = request.data['coordinator']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.coordinators.add(user)

        getUserClass.save()
        serializers = ClassSerializer(getUserClass, many=False)
        response = {'message': 'Updated', 'results': serializers.data }
        return Response (response, status=status.HTTP_200_OK)

#  remove user from class
    @action (detail=True, methods = ['POST'])
    def removeUserFromClass(self, request, pk=None):
        # get the class by pk
        getUserClass= Class.objects.get(id=pk)  

        # trying to remove a student
        if 'student' in request.data:   
            # get the username by the data
            username = request.data['student']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.students.remove(user)

        # trying to remove a matatz
        if 'matatz' in request.data:   
            # get the username by the data
            username = request.data['matatz']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.matatzes.remove(user)

        # trying to remove a teacher
        if 'teacher' in request.data:   
            # get the username by the data
            username = request.data['teacher']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.teachers.remove(user)

         # trying to remove a coordinator
        if 'coordinator' in request.data:   
            # get the username by the data
            username = request.data['coordinator']
            # get the user by the given username
            user = UserProfile.objects.get(username=username)
            getUserClass.coordinators.remove(user)

        getUserClass.save()
        serializers = ClassSerializer(getUserClass, many=False)
        response = {'message': 'Updated', 'results': serializers.data }
        return Response (response, status=status.HTTP_200_OK)
    
    @action (detail=True, methods = ['POST'])
    def addClass(self, request, pk=None):
        # get the user by the authentication
        user = request.user
        # get the School name by the data
        schoolName = request.data['school']
        school = School.objects.get(schoolName=schoolName)
        # get the Class name by the data
        className = request.data['className']
        # create a new class with the given name

        #test 
        print(schoolName)
        print(school)


        newClass = Class.objects.create(className=className, school=school)
        newClass.save()
        # get the type of the user who created the class in order
        # to check whether it needs to be assigned to the class or not
        typeOfUser = request.data['typeOfUser']
        print("typeOfUser: ", typeOfUser)
        if(typeOfUser == '4'): # the user who created the class is coordinator
            # find the userProfile Object of the auth and assign it as a coordinator for the new class
            coordinator = UserProfile.objects.get(user=user)
            newClass.coordinators.add(coordinator)
            newClass.save()
        response = {'message': 'Updated', 'results': newClass }
        return Response (response, status=status.HTTP_200_OK)   


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = GroupSerializer 
    parser_classes = (MultiPartParser,FormParser, JSONParser)
    authentication_classes = (TokenAuthentication, )            
       
    # get matatz of a student by the group table
    @action (detail=True, methods = ['POST'])
    def getStudentsMatatz(self, request, pk=None):
        # find the group that the given user belongs to
        group= Group.objects.filter(students=pk)
        # extract the matatz username from the group
        matatz = group[0].user
        #get the matatzProfie object and send it as response
        matatzProfile= UserProfile.objects.get(username=matatz)
        serializers = UserProfileSerializer(matatzProfile, many=False)       
        response = {'message': 'Get', 'results': serializers.data }
        return Response (response, status=status.HTTP_200_OK)

# class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
#     template_name = 'users/password_reset.html'
#     email_template_name = 'users/password_reset_email.html'
#     subject_template_name = 'users/password_reset_subject'
#     success_message = "We've emailed you instructions for setting your password, " \
#                       "if an account exists with the email you entered. You should receive them shortly." \
#                       " If you don't receive an email, " \
#                       "please make sure you've entered the address you registered with, and check your spam folder."
#     success_url = reverse_lazy('users-home') 
class ForgetPasswordViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    # serializer_class = GroupSerializer 
    parser_classes = (MultiPartParser,FormParser, JSONParser)
    authentication_classes = (TokenAuthentication, )   

    @action (detail=True, methods = ['POST'])
    def forgot_password(self, request, pk=None):
        print("forgot password")
        # schoolName = request.data['school']
        email = request.data['email']
        print(email)
        verify = User.objects.filter(username=email).first()
        if verify:
            link = f"http://localhost:3000/ChangePassword?user={verify.id}"
            send_mail(
                'Verify Account',
                'Please Verify Your Acoount',
                'qwqwqw12121256@outlook.com',
                # 'codeartisanlab2607@gmail.com',
                [email],
                fail_silently=False,
                html_message=f'<p>Please verify your account</p><p>{link}</p>'
            ) 
            return JsonResponse({'bool': True, 'msg': 'check email'})
        else:
            return JsonResponse({'bool': False, 'msg': 'invalid email'})

    @action (detail=True, methods = ['POST'])
    def change_password(self, request, pk=None):
        print("change password")
        # schoolName = request.data['school']
        user = request.data['user']
        print(user)
        password = request.data['password']
        print(password)
        # verify = User.objects.filter(user=user).first()
        # if verify:
        # password = password.encode('utf-8')
        # assert password
        User.objects.filter(id=user).update(password=make_password(password))
        return JsonResponse({'bool': True, 'msg': 'password has been changed'})
        # else:
        #     return JsonResponse({'bool': False, 'msg': 'invalid email'})
       
class FrontalCourseViewSet(viewsets.ModelViewSet):
    queryset = FrontalCourse.objects.all()
    serializer_class = FrontalCourseSerializer 
    authentication_classes = (TokenAuthentication, )

class ClassFrontalCoursesViewSet(viewsets.ModelViewSet):
    queryset = ClassFrontalCourses.objects.all()
    serializer_class = ClassFrontalCourseSerializer 
    authentication_classes = (TokenAuthentication, )

    # get all the frontal courses belongs to specific class
    @action (detail=True, methods = ['POST'])
    def getFrontalCourseByClass(self, request, pk=None):
        print("im here")
        print(pk)
        # get the classId by the pk
        classId = pk
        print(classId)
        print("now")
        #get the ClassFrontalCourses objects of this class
        classFrontalCourses= ClassFrontalCourses.objects.filter(classId=classId)
        # print(classFrontalCourses[0].frontalCourse)
        allFrontalCourses=[]
        #get all the objects of frontal courses belongs to the class
        for classFrontalCourse in classFrontalCourses:
            frontalCourses= FrontalCourse.objects.get(id=classFrontalCourse.frontalCourse.id)
            print(frontalCourses.description)
            serializers = FrontalCourseSerializer(frontalCourses, many=False)
            allFrontalCourses.append(serializers.data)    
        response = {'message': 'Get', 'results': allFrontalCourses }
        return Response (response, status=status.HTTP_200_OK)



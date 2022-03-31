from django.shortcuts import get_object_or_404, redirect, render

from email import message
from urllib import request
from coreapi import Object
from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Answer, Course, Department, Instructor, Notes, Question, Quiz, Specialization, Student, Tutorial, User, Announcement, TakenQuiz, UserProfile
from .forms import AnswerForm, NotesForm, QuestionForm, TutorialForm, UserProfileForm, UserRegistrationForm, StudentForm, CourseForm, AnnouncementForm, QuizForm, TakeQuizForm, AnswerFormset
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import views as auth_view
from django.db import transaction
from django.db.models import Count
# Import mimetypes module
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse
# Import render module
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.conf import settings
from utils import sendEmail, sendEmailOnUesrRegistration
# Create your views here.

def home(request):
    return render(request, 'e_learn/home.html')

def dashboard(request):
    
    courses = Course.objects.all().count()
    students = User.objects.filter(is_student=True).count()
    instructors = User.objects.filter(is_instructor=True).count()
    users = User.objects.all().count()
    print("asd", courses)
    print("asd", students)
    print("asd", instructors)
    print("asd", users)
    context = {
        "courses" : courses,
        "students" : students,
        "instructors " : instructors,
        "users " : users,
    }
    return render(request, 'e_learn/dashboard.html', context)

def register_instructor(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        print("Form : ", form)
        if form.is_valid():
            instructor = form.save(commit=False)
            instructor.is_instructor = True
            instructor.save()
            messages.success(request, 'Instructor is added successfully')
            return redirect('register_instructor')
        else:
            return render(request, 'e_learn/admin/register_instructor.html', {"form":form})

    form = UserRegistrationForm()
    context = {
        "form" : form
    }
    return render(request, 'e_learn/admin/register_instructor.html', context)

class RegisterStudent(View):
    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.is_student = True
            user.save()
            subjects = student_form.cleaned_data['subjects']
            instance = Student.objects.create(user = user)
            instance.subjects.set(subjects) 
            messages.success(request, "Student is Added Successfully")
            sendEmailOnUesrRegistration(user)
            return redirect("login")
        else:
            context={
                "user_form" : user_form,
                "student_form" : student_form
            }
            user = str(request.user)
            if user == "AnonymousUser":
                return render(request, 'e_learn/register_student.html', context)   
            else:
                return render(request, 'e_learn/admin/register_student.html', context)   

    def get(self, request):
        user_form = UserRegistrationForm()
        student_form = StudentForm()
        print("Student_form : ", student_form)
        context={
            "user_form" : user_form,
            "student_form" : student_form
        }
        user = str(request.user)
        if user == "AnonymousUser":
            return render(request, 'e_learn/register_student.html', context)   
        else:
            return render(request, 'e_learn/admin/register_student.html', context)   

class RegisterCourse(View):
    def get(self, request):
        form = CourseForm()
        context = {
            "form" : form
        }
        return render(request, 'e_learn/admin/register_course.html', context)
    
    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Course is Added Successfully")
            return redirect("register_course")
        else:
            context = {
                "form" : form
            }
            return render(request, 'e_learn/admin/register_course.html', context)

class AnnouncementList(View):
    def get(self, request):
        announcements = Announcement.objects.all()
        context = {
            "announcements" : announcements
        }
        return render(request, 'e_learn/admin/announcement_list.html', context)

class AnnouncementCreate(View):
    def get(self, request):
        form = AnnouncementForm()
        context = {
            "form" : form
        }
        return render(request, 'e_learn/admin/announcement_create.html', context)
  
    def post(self, request):
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = User.objects.get(id=1)
            instance.save()
            messages.success(request, 'Announcement is Posted Successfully')
            return redirect('announcement_list')
        else:
            context = {
                "form" : form
            }
            return render(request, 'e_learn/admin/announcement_create.html', context)

class AnnouncementUpdate(View):
    def get(self, request, id):
        obj = Announcement.objects.get(id=id)
        form = AnnouncementForm(instance=obj)
        print("Form_ :", form)
        context = {
            "form" : form
        }
        return render(request, 'e_learn/admin/announcement_create.html', context)
    def post(self, request, id):
        obj = Announcement.objects.get(id=id)
        form = AnnouncementForm(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = User.objects.get(id=1)
            instance.save()
            messages.success(request, 'Updated Successfully')
            return redirect("announcement_list")
        else:
            context = {
                "form" : form
            }
            return render(request, 'e_learn/admin/announcement_create.html', context)

class AnnouncementDelete(View):
    def get(self, request, id):
        Announcement.objects.get(id=id).delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('announcement_list')
    
class ManageUsers(View):
    def get(self, request):
        users = User.objects.all()
        context = {
            "users" : users
        }
        return render(request, 'e_learn/admin/manage_users.html', context)

class RegisterAdmin(View):
    def get(self, request):
        form = UserRegistrationForm()
        context = {
            "user_form" : form
        }
        return render(request, 'e_learn/admin/register_admin.html', context)
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.is_admin = True
            user.save()
            messages.success(request, "Admin User is Added Successfully")
            return redirect('register_admin')
        else:
            context = {
                "user_form" : form
            }
            return render(request, 'e_learn/admin/register_admin.html', context)
class UserDelete(View):
    def get(self, request, id):
        try:
            User.objects.get(id=id).delete()
            return redirect('manage_users')
        except:
            users = User.objects.all()
            context = {
                "users" : users
            }
            messages.warning(request, 'User does not exists')
            return render(request, 'e_learn/admin/manage_users.html', context)


class ManageQuiz(View):
    def get(self, request):
        quizzes =  Quiz.objects.all()
        context = {
            "quizzes" : quizzes
        }
        return render(request, 'e_learn/instructor/quiz_list.html', context)

class QuizAdd(View):
    def get(self, request):
        form =  QuizForm()
        context = {
            "form" : form
        }
        return render(request, 'e_learn/instructor/quiz_add.html', context)

    def post(self, request):
        form =  QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            messages.success(request, 'Quiz Added Successfully')
            return redirect('manage_quiz')
        context = {
            "form" : form
        }
        return render(request, 'e_learn/instructor/quiz_add.html', context)
        

class QuizQuestion(View):
    def get(self, request, id):
        q_form =  QuestionForm()
        a_form =  AnswerFormset()
        context = {
            "q_form" : q_form,
            "a_form" : a_form
        }
        return render(request, 'e_learn/instructor/questions_add.html', context)

    def post(self, request, id):
        q_form =  QuestionForm(request.POST)
        a_form =  AnswerFormset(request.POST)
        if q_form.is_valid() and a_form.is_valid():
            question = q_form.save(commit=False)
            question.quiz_id = id
            question.save()
            
            answers = a_form.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, 'Question is added successfully')
            return redirect('quiz_details', id )
        context = {
            "q_form" : q_form,
            "a_form" : a_form
        }
        return render(request, 'e_learn/instructor/questions_add.html', context)

class QuizQuestionUpdate(View):
    def get(self, request, id):
        question = Question.objects.get(id=id)
        q_form =  QuestionForm(instance=question)
        a_form =  AnswerFormset(instance=question)
        context = {
            "q_form" : q_form,
            "a_form" : a_form
        }
        return render(request, 'e_learn/instructor/questions_update.html', context)

    def post(self, request, id):
        question = Question.objects.get(id=id)
        q_form =  QuestionForm(request.POST)
        a_form =  AnswerFormset(request.POST, instance=question)
        print("hi__post")
        print("q_form.is_valid() : ",q_form.is_valid())
        print("a_form.is_valid() : ",a_form.is_valid())
        print("a_form : ",a_form)
        if q_form.is_valid() and a_form.is_valid():
            print("hi__valid")
            question = q_form.save(commit=False)
            question.quiz_id = id
            question.save(instance=question)
            
            answers = a_form.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save(instance=question)
            # answer.instance = question
            # answer.save()
            messages.success(request, 'Question is added successfully')
            return redirect('quiz_details', id )
        context = {
            "q_form" : q_form,
            "a_form" : a_form
        }
        return render(request, 'e_learn/instructor/questions_update.html', context)
  

class QuizDetails(View):
    def get(self, request, id):
        answers_list = []
        questions = Question.objects.filter(quiz_id=id)
        for question in questions:
            answers = Answer.objects.filter(question = question)
            answers_list.append(answers)
        context = {
            "questions" : questions,
            "answers_list" : answers_list,
            "quiz_id" : id ,
        }
        return render(request, 'e_learn/instructor/quiz_details.html', context)

class TutoialList(View):
    def get(self, request):
        tutorials =  Tutorial.objects.all()
        context = {
            'tutorials' : tutorials
        }
        return render(request, 'e_learn/instructor/tutorials_list.html', context)

class TutorialAdd(View):
    def get(self, request):
        form =  TutorialForm()
        context = {
            'form' : form
        }
        return render(request, 'e_learn/instructor/tutorial_add.html', context)

    def post(self, request):
        form =  TutorialForm(request.POST)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.user = request.user
            tutorial.save()
            messages.success(request, 'Tutorial Added Successfully')
            return redirect('tutorial_add')
        context = {
            'form' : form
        }
        return render(request, 'e_learn/instructor/tutorial_add.html', context)

class TutoialDetails(View):
    def get(self, request, id):
        tutorial = Tutorial.objects.get(id=id)
        context = {
            "tutorial" : tutorial
        }
        return render(request, 'e_learn/instructor/tutorial_details.html', context)

class TutoialDelete(View):
    def get(self, request, id):
        try:
            Tutorial.objects.get(id=id).delete()
            messages.success(request, 'Turorial is deleted Deleted Successfully')
            return redirect('tutorial_list')
        except:
            messages.warning(request, 'Turorial does not exists')
            return redirect('tutorial_list')

class TutoialUpdate(View):
    def get(self, request, id):
        obj = Tutorial.objects.get(id=id)
        form =  TutorialForm(instance=obj)
        context = {
            'form' : form,
            'action' : 'update' 
        }
        return render(request, 'e_learn/instructor/tutorial_add.html', context)

    def post(self, request, id):
        obj = Tutorial.objects.get(id=id)
        form =  TutorialForm(request.POST, instance=obj)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.user = request.user
            tutorial.save()
            messages.success(request, 'Tutorial Update Successfully')
            return redirect('tutorial_list')
        context = {
            'form' : form
        }
        return render(request, 'e_learn/instructor/tutorial_add.html', context)

# ******************* Manage Notes ***********************

class NotesList(View):
    def get(self, request):
        notes =  Notes.objects.all()
        context = {
            'notes' : notes
        }
        return render(request, 'e_learn/instructor/notes_list.html', context)

class NotesAdd(View):
    def get(self, request):
        form =  NotesForm()
        print("Notes_add_form : ", form)
        context = {
            'form' : form
        }
        return render(request, 'e_learn/instructor/notes_add.html', context)

    def post(self, request):
        form =  NotesForm(request.POST, request.FILES)
        if form.is_valid():
            print("form : ", form)
            tutorial = form.save(commit=False)
            tutorial.user = request.user
            tutorial.save()
            messages.success(request, 'Note Added Successfully')
            return redirect('notes_add')
        context = {
            'form' : form
        }
        return render(request, 'e_learn/instructor/notes_add.html', context)

class NotesDetails(View):
    def get(self, request, id):
        tutorial = Tutorial.objects.get(id=id)
        context = {
            "tutorial" : tutorial
        }
        return render(request, 'e_learn/instructor/tutorial_details.html', context)

class NotesDelete(View):
    def get(self, request, id):
        try:
            Notes.objects.get(id=id).delete()
            messages.success(request, 'Turorial is deleted Deleted Successfully')
            return redirect('notes_list')
        except:
            messages.warning(request, 'Notes does not exists')
            return redirect('notes_list')

class NotesUpdate(View):
    def get(self, request, id):
        obj = Notes.objects.get(id=id)
        form =  NotesForm(instance=obj)
        context = {
            'form' : form,
            'action' : 'update' 
        }
        return render(request, 'e_learn/instructor/notes_add.html', context)

    def post(self, request, id):
        obj = Notes.objects.get(id=id)
        form =  NotesForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            tutorial = form.save(commit=False)
            tutorial.user = request.user
            tutorial.save()
            messages.success(request, 'Tutorial Update Successfully')
            return redirect('notes_list')
        context = {
            'form' : form
        }
        return render(request, 'e_learn/instructor/notes_add.html', context)


# Define function to download pdf file using template
def download_pdf_file(request, id):
    note = Notes.objects.get(id=id)
    filename = note.file
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define the full file path
    filepath = BASE_DIR + '/media/' + str(filename)
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response

class CourseUpdate(View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        form = StudentForm(instance=student)
        context = {
            "form" : form
        }
        return render(request, 'e_learn/student/course_update.html', context)
        
    def post(self, request):
        student = Student.objects.get(user=request.user)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            subjects = form.cleaned_data['subjects']
            student = form.save(commit=False)
            student.user = request.user
            student.subjects.set(subjects)
            student.save()

            messages.success(request, 'Courses updated successfully!')
            return redirect('course_update')
        context = {
            "form" : form
        }
        return render(request, 'e_learn/student/course_update.html', context)


class QuizListStudent(View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        queryset = Quiz.objects.all()
        subjects = student.subjects.all()
        quizzes = [ qs for qs in queryset if qs.course in subjects]
        context = {
            "quizzes" : quizzes,
            "subjects" : subjects,
        }
        return render(request, 'e_learn/student/quiz_list.html', context)

def take_quiz(request, id):
    quiz = get_object_or_404(Quiz, pk=id)
    student = request.user.student
    if student.quizzes.filter(pk=id).exists():
        print("Strong__")
        return render(request, 'e_learn/student/quiz_taken.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()
    
    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('take_quiz', id)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.title, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.title, score))
                    return redirect('active_quiz')
    else:
        form = TakeQuizForm(question=question)
        print("form : ", form)
    return render(request, 'e_learn/student/quiz_take.html', {
        'subject' : quiz.course.title,
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress,
    })       

class TakenQuizListStudent(View):
    def get(self, request):
        student = request.user.student
        subjects = student.subjects.all()
        quizzes = student.taken_quiz.all()
        context = {
            "subjects" : subjects,
            "quizzes" : quizzes
        }
        return render(request, 'e_learn/student/quiz_taken.html', context)

class ViewProfile(View):
    def get(self, request):
        try:
            user = UserProfile.objects.get(custom_user=self.request.user)
        except UserProfile.DoesNotExist:
            user = UserProfile()
        context = {
            "user" : user
        }
        return render(request, 'e_learn/admin/profile_view.html', context)

class CreateProfile(View):
    def get(self, request):
        try:
            user = UserProfile.objects.get(custom_user=request.user)
        except UserProfile.DoesNotExist:
            user = None
        form = UserProfileForm(instance=user)
        context = {
            "form" : form
        }
        return render(request, 'e_learn/admin/profile_create.html', context)

    def post(self, request):
        try: 
            print("try__")
            profile = UserProfile.objects.get(custom_user = self.request.user)
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
        except:
            print("except")
            form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.custom_user = self.request.user
            profile.save()
            messages.success(request, 'Profile Created Successfully')
            return redirect('view_profile')
        context = {
            "form" : form
        }
        return render(request, 'e_learn/admin/profile_create.html', context)

def load_department(request):
    if request.method == "GET":    
        id = request.GET.get('campusID', None)
        departments = Department.objects.filter(campus_id=id)
        return render(request, "e_learn/admin/load_departments.html", {"departments":departments})

def load_specialization(request):
    dep_id = request.GET.get("dep_id", None)
    dep = Department.objects.get(id=dep_id)
    specializations =  Specialization.objects.filter(department=dep)
    return JsonResponse(list(specializations.values('id', 'name')), safe=False)
    
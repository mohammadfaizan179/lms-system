from unicodedata import name
from django.urls import path
from . import views
# Import mimetypes module
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse
# Import render module
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='home'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-instructor/', views.register_instructor, name='register_instructor'),
    path('register-student/', views.RegisterStudent.as_view(), name='register_student'),
    path('register-course/', views.RegisterCourse.as_view(), name='register_course'),
    
    path('announcement-list/', views.AnnouncementList.as_view(), name='announcement_list'),
    path('announcement-create/', views.AnnouncementCreate.as_view(), name='announcement_create'),
    path('announcement-update/<int:id>/', views.AnnouncementUpdate.as_view(), name='announcement_update'),
    
    path('annomanage_usersuncement-delete/<int:id>/', views.AnnouncementDelete.as_view(), name='announcement_delete'),
    path('manage-users/', views.ManageUsers.as_view(), name='manage_users'),
    path('delete-user/<int:id>/', views.UserDelete.as_view(), name='user_delete'),
    path('register-admin/', views.RegisterAdmin.as_view(), name='register_admin'),
    
    # quiz-urls for instructor    
    path('quiz-list/', views.ManageQuiz.as_view(), name='manage_quiz'),
    path('quiz/<int:id>/details/', views.QuizDetails.as_view(), name='quiz_details'),
    path('quiz/<int:id>/add/question/', views.QuizQuestion.as_view(), name='quiz_questions'),
    path('quiz/<int:id>/update/question/', views.QuizQuestionUpdate.as_view(), name='quiz_questions_update'),
    path('quiz/add/', views.QuizAdd.as_view(), name='quiz_add'),
    
    path('tutorials/', views.TutoialList.as_view(), name='tutorial_list'),
    path('tutorial/add', views.TutorialAdd.as_view(), name='tutorial_add'),
    path('tutorial/<int:id>/details/', views.TutoialDetails.as_view(), name='tutorial_details'),
    path('tutorial/<int:id>/delete/', views.TutoialDelete.as_view(), name='tutorial_delete'),
    path('tutorial/<int:id>/update/', views.TutoialUpdate.as_view(), name='tutorial_update'),

    path('notes/', views.NotesList.as_view(), name='notes_list'),
    path('notes/add', views.NotesAdd.as_view(), name='notes_add'),
    path('notes/<int:id>/delete/', views.NotesDelete.as_view(), name='notes_delete'),
    path('notes/<int:id>/update/', views.NotesUpdate.as_view(), name='notes_update'),
    path('download-file/<int:id>/', views.download_pdf_file, name='download_pdf_file'),

    # quiz-urls for student 
    path('course/update/', views.CourseUpdate.as_view(), name='course_update'),
    path('quiz/active/', views.QuizListStudent.as_view(), name='active_quiz'),
    path('quiz/taken/', views.TakenQuizListStudent.as_view(), name='taken_quiz'),
    path('quiz/<int:id>/attempt/', views.take_quiz, name='take_quiz'),

    path('profile-view/', views.ViewProfile.as_view(), name='view_profile'),
    path('profile-create/', views.CreateProfile.as_view(), name='create_profile'),
    path('departments/load/', views.load_department, name='load_departments'),
    path('specialization/load/', views.load_specialization, name='load_specialization'),
]

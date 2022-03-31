from email.policy import default
from enum import unique
from pyexpat import model
from tabnanny import verbose
from tkinter import CASCADE
from tokenize import blank_re
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape, mark_safe
from embed_video.fields import EmbedVideoField
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is Required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active = True'))
        self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"), unique=True)
    username = models.CharField(_("Username"), max_length=100, blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=True) 
    is_staff = models.BooleanField(_("Is Staff"), default=False) 
    is_superuser = models.BooleanField(_("Is SuperUser"), default=False) 
    is_admin = models.BooleanField(_("Is Admin "), default=False) 
    is_instructor = models.BooleanField(_("Is Instructor"), default=False) 
    is_student = models.BooleanField(_("Is Student"), default=False) 
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
   
    USERNAME_FIELD = 'email'
    objects = UserManager()
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

class Campus(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name="department")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Specialization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="specialization")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    custom_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150, blank=True, null=True)
    mobile = models.PositiveBigIntegerField(_("Mobile"), unique=True, blank=True, null=True)
    email = models.EmailField(_("Email"), unique=True, blank=True, null=True)
    dob = models.DateField(_("Date of Birth"))
    address = models.CharField(_("Address"), max_length=150, blank=True, null=True)
    city = models.CharField(_("City"), max_length=150, blank=True, null=True)
    province = models.CharField(_("Province"), max_length=150, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to = 'user', blank=True, null=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name="campus")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="department")
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name="user_profile_specialization")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return '/static/dist/img/avatar5.png'

class Course(models.Model):
    title = models.CharField(_("Title"), max_length=150, unique=True)
    color = models.CharField(_("Color Code"), max_length=7, default="#007bff")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f'{self.title}'

    @property
    def get_html_badge(self):
        title = escape(self.title)
        color = escape(self.color)
        html = f'<span class="badge badge-primary" style="background-color:{color}>{title}</span>'
        return mark_safe(html)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(_("Title"), max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.email} - {self.course.title} - {self.title}'

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
    
    @property
    def get_quiz_questions_number(self):
        question_count = Question.objects.filter(quiz=self).count()
        return question_count

    @property
    def is_quiz_taken(self):
        return self.taken_quiz.filter(quiz=self).exists()
        

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    subjects = models.ManyToManyField(Course, related_name='student_subjects')
    quizzes = models.ManyToManyField(Quiz, through="TakenQuiz", related_name='student_quizzes')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers.filter(answer__question__quiz=quiz).values_list('answer__question__pk', flat=True)
        print("answered_questions : ", answered_questions)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('question_text')
        print("questions : ", questions)
        
        return questions

    def __str__(self):
        return f'{self.user.email}'

   

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    
class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quiz')
    score = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
   

class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(_("Announcement"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.description[:30]}'

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(_("Question"), max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.question_text} - {self.quiz.title}'

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Question'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(_("text"), max_length=255)
    is_correct = models.BooleanField(_("Correct Answer"), default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text} - {self.question.question_text}'

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class Tutorial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=155)
    content = models.TextField(_("Content"), max_length=155)
    video = EmbedVideoField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Tutorial'
        verbose_name_plural = 'Tutorials'


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=155)
    cover = models.ImageField(upload_to = "notes", blank=True, null=True)
    file = models.FileField(upload_to = "notes", blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Notes'
        verbose_name_plural = 'Notes'
    
    """
    def delete(self, *args, **kwargs):
        self.file.delete()
        self.cover.delete()
        super().delete(*args, **kwargs) 
    """

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interest = models.ManyToManyField(Course, related_name="more_locations")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

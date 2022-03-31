
from email.policy import default
from attr import attr, field, fields
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from .models import Announcement, Answer, Campus, Department, Notes, Question, Quiz, Student, StudentAnswer, Tutorial, User, Course, UserProfile
from e_learn import models
from django.forms import inlineformset_factory

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['email']
        
class StudentForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Student
        fields = ['subjects']
    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'color' : forms.TextInput(attrs={'class':'form-control'})
        }
        labels = {
            'color' : "Course Color Code, Default Color #007bff"
        }
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['description']
        widgets = {
            'description' : forms.Textarea(attrs={'class':'form-control'})
        }

class QuizForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Quiz
        fields = ['course', 'title']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    # course = forms.ModelChoiceField(queryset=Quiz.objects.all(), widget=forms.Select(attrs={'class':'form-control'})),
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text' : forms.TextInput(attrs={'class':'form-control'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text' : forms.TextInput(attrs={'class':'form-control'}),
            'is_correct' : forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class TutorialForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Tutorial
        exclude = ['user']
        widgets = {
            "title"     : forms.TextInput(attrs={'class':'form-control'}),
            "content"   : forms.Textarea(attrs={'class':'form-control'}),
            "video"     : forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'video' : 'Youtube video link'
        }

class NotesForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Notes
        exclude = ['user']
        widgets = {
            "title"     : forms.TextInput(attrs={'class':'form-control'}),
            "cover"  : forms.FileInput(attrs={'class': 'form-control'}),
            "file"  : forms.FileInput(attrs={'class': 'form-control'}),
        }

class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset = Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        print("question.answers", question.answers)
        self.fields['answer'].queryset = question.answers.order_by('text')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['custom_user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].queryset = Department.objects.none()

        if 'campus' in self.data:
            try:
                campus_id = int(self.data.get('campus'))
                self.fields['department'].queryset = Department.objects.filter(campus_id=campus_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['department'].queryset = self.instance.campus.department.all()
            
AnswerFormset = inlineformset_factory(Question, Answer, fields=['text', 'is_correct'], extra=3, max_num=3)
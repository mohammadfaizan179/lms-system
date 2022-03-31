from attr import attrs, fields
from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from e_learn.models import User

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password' ,'class' : 'form-control'}))

class UserPasswordChange(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class UserPasswordResetForm(PasswordResetForm):
    class Meta:
        model = User
        fields = '__all__'
    
class UserSetPasswordForm(SetPasswordForm):
    # new_password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={'autocomplete' : 'new-passowrd', 'autofocus':True, 'class' : 'form-control'}))
    # new_password2 = forms.CharField(label='Confirm Passowrd', strip=False, widget=forms.PasswordInput(attrs={'auto-complete':'new-passowrd', 'class':'form-control'}))

    new_password1 = forms.CharField(label='New Password', strip =False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'autofocus':True ,'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', strip =False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

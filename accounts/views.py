from re import template
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import UserPasswordChange, UserPasswordResetForm, UserSetPasswordForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import SetPasswordForm

# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            pd = form.cleaned_data['password']
            user = authenticate(username = email, password=pd)
            if user:
                login(request, user)
                return redirect('dashboard')
        else:
            context = {
                "form" : form 
            }
            return render(request, 'accounts/login.html', context)
    else:
        form = LoginForm()
        context = {
            "form" : form 
        }
        return render(request, 'accounts/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('home')


def change_password(request):
    if request.method == "POST":
        form = UserPasswordChange(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password is successfully updated!')
            return redirect('view_profile')    
        else:
            context = {
                "form" : form
            }
            return render(request, 'accounts/change_password.html', context)
    
    form = UserPasswordChange(request.user) 
    context = {
        "form" : form
    }
    return render(request, 'accounts/change_password.html', context)

class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/reset_password.html'
    form_class = UserPasswordResetForm
    # success_url = ''

class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'
    form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
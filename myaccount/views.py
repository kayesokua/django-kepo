from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, UserProfileForm

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


def homepage(request):
    return redirect('feed')

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'myaccount/signup.html', {'form':UserRegisterForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('myjournal:journal_today')
            except IntegrityError:
                return render(request, 'myaccount/signup.html', {'form':UserRegisterForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'myaccount/signup.html', {'form':UserRegisterForm(), 'error':'Passwords did not match'})

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'myaccount/signin.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'myaccount/signin.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('myjournal:journal_today')

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign_in')

@login_required
def account_settings(request):
    return render(request, 'myaccount/settings.html')

@login_required
def account_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.save()
            return render(request, 'myaccount/account_update.html', {'form': form, 'success':"Profile been changed"})
        else:
            return render(request, 'myaccount/account_update.html', {'form': form, 'error':" Bad data passed in. Report error"})   
    else:
        form = UserUpdateForm(instance=request.user)
        return render(request, 'myaccount/account_update.html', {'form': form})   

@login_required
def password_update(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request, 'myaccount/password_update.html', {'form': form, 'success':"Your password has been successfully changed."})   
        else:
            return render(request, 'myaccount/password_update.html', {'form': form, 'error':"Bad data passed in. Try again"})   
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'myaccount/password_update.html', {'form': form})
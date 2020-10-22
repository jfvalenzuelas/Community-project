from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'community_main/home.html')

def signup_user(request):
    if request.method == 'GET':
        # Send the sign up form
        return render(request, 'community_main/signup.html', {
            'form':UserCreationForm()
        })
    else:
        # Passwords match
        if request.POST['password1'] == request.POST['password2']:
            # Create a new user
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            try:
                user.save()
                login(request, user)
                return redirect('community_home')
            except IntegrityError:
                 return render(request, 'community_main/signup.html', {
                    'form':UserCreationForm(),
                    'error': 'The username has already been taken. Please, use a different username.'
                })
        else:
            # Passwords do not match
            return render(request, 'community_main/signup.html', {
                'form':UserCreationForm(),
                'error': 'Passwords do not match.'
            })

def login_user(request):
    if request.method == 'GET':
        # Send the sign up form
        return render(request, 'community_main/login.html', {
            'form':AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('community_home')
        else:
            return render(request, 'community_main/login.html', {
                'form':AuthenticationForm(),
                'error':'Username and password do not match.'
            })

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('community_home')
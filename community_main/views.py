from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserForm, UserProfileForm, UserProfilePictureForm
from .models import Profile
from market.models import Product, Image, Category
from wall.models import Post, UserPostLike
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django_ajax.decorators import ajax
from django.core import serializers

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
                profile = Profile(user=request.user)
                profile.save()

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

@login_required
def profile(request):
    if request.method == 'GET':
        userFormContext = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

        profile = get_object_or_404(Profile, user=request.user)

        profileFormContext = {
            'birth_date': profile.birth_date
        }

        products_list = []
        products = Product.objects.filter(created_by=request.user)
        for product in products:
            thumbnail = Image.objects.filter(product=product)[0]
            product_data = {
                "product": product,
                "thumbnail": thumbnail
            }
            products_list.append(product_data)

        posts = Post.objects.filter(created_by=request.user).order_by('-created_at')

         # If the User is authenticated, search for liked posts
        if request.user.is_authenticated:
            user_post_likes = UserPostLike.objects.filter(user=request.user, post__in=posts)
            liked_posts = [user_post_like.post.id for user_post_like in user_post_likes]
        else: # If the User is not authenticated, send an empty array
            liked_posts = []

        return render(request, 'community_main/profile.html', {
            'user': request.user,
            'products_list': products_list,
            'posts': posts,
            'liked_posts': liked_posts,
            'user_form': UserForm(userFormContext),
            'profile_form': UserProfileForm(profileFormContext),
        })

@ajax
@login_required
def update_profile(request):
    if request.method == 'POST':
        userFormInfo = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email']
        }

        userProfileInfo = {
            'birth_date': request.POST['birth_date']
        }

        userForm = UserForm(userFormInfo, instance=request.user)

        userProfile = get_object_or_404(Profile, user=request.user)

        userProfileForm = UserProfileForm(userProfileInfo, instance=userProfile)

        if userForm.is_valid():
            if userProfileForm.is_valid():
                userForm.save()
                userProfileForm.save()
                data = {
                    "message": "Profile information updated successfully."
                }

                return JsonResponse(data, status=200)
            else:
                data = {
                    "error": {
                        "user_form": userForm.errors,
                        "profile_form": userProfileForm.errors
                    }
                }

                return JsonResponse(data, status=400)
        else:
            data = {
                "error": {
                    "user_form": userForm.errors,
                    "profile_form": userProfileForm.errors
                }
            }

            return JsonResponse(data, status=400)

@ajax
@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        userProfile = get_object_or_404(Profile, user=request.user)

        profilePictureForm = UserProfilePictureForm(request.POST or None, request.FILES or None, instance=userProfile)

        if profilePictureForm.is_valid():
            profilePictureForm.save()
            
            data = {
                "message": "Profile picture updated successfully.",
                "data": {
                    "picture_url": userProfile.picture.url
                },
            }

            return JsonResponse(data, status=200)
        else:
            data = {
                "error": {
                    "message": "Profile picture could not be updated.",
                    "form_error": profilePictureForm.errors
                }
            }
        
            return JsonResponse(data, status=400)
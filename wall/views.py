from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Create your views here.
def home(request):
    if request.method == 'GET':

        posts = Post.objects.all().order_by('-created_at')

        context = {
            'form': PostForm(),
            'posts': posts
        }

        return render(request, 'wall/home.html', context)

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)

        if form.is_valid():
            post = Post(text=form['text'].data, created_by=request.user)
            post.save()

            data = {
                "message": "Post was created successfully",
                "redirect": reverse("wall_home")
            }

            return JsonResponse({'data':data}, status=200)

        else:

            data = {
                "error": form.errors
            }

            return JsonResponse({'data':data}, status=400)

def view_post(request, post_pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_pk)
        
        context = {
            'post': post
        }

        return render(request, 'wall/view-post-modal.html', context)

@login_required
def delete_post(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()

        return redirect('wall_home')
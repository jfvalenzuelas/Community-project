from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, UserPostLike, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def home(request):
    if request.method == 'GET':

        posts = Post.objects.all().order_by('-created_at')
        user_post_like = UserPostLike.objects.filter(user=request.user)
        liked_posts = [user_post_like.post.id for user_post_like in user_post_like]

        context = {
            'form': PostForm(),
            'posts': posts,
            'liked_posts': list(liked_posts)
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
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        liked_post = UserPostLike.objects.filter(post=post, user=request.user)
        is_liked_post = False

        if (liked_post): is_liked_post = True

        context = {
            'post': post,
            'liked_post': is_liked_post,
            'comment_form': CommentForm(),
            'comments': comments
        }

        return render(request, 'wall/view-post-modal.html', context)

@login_required
def delete_post(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.delete()

        return redirect('wall_home')

@login_required
def like_post(request, post_pk):
    if request.method == 'POST':
        # Get liked Post
        post = get_object_or_404(Post, pk=post_pk)

        # Search if user already has liked the post
        user_post_like = UserPostLike.objects.filter(post=post, user=request.user)

        # If there is a like, then unlike the post
        if (user_post_like):
            user_post_like.delete()

            # Decrease Post's Likes counter
            post.likes -= 1
            post.save()

            data = {
                "message": "Post unliked successfully",
                "likes": post.likes
            }

            return JsonResponse({'data': data}, status=200)

        else:
            # Create a new UserPostLike object
            user_post_like = UserPostLike(post=post, user=request.user)
            user_post_like.save()

            # Increment Post's Likes counter
            post.likes += 1
            post.save()

            data = {
                "message": "Post liked successfully",
                "likes": post.likes
            }

            return JsonResponse({'data':data}, status=200)

@login_required
def new_comment(request, post_pk):
    if request.method == 'POST':
        form = PostForm(request.POST or None)

        # Comment was successfully validated
        if form.is_valid():
            # Get commented Post
            post = get_object_or_404(Post, pk=post_pk)

            # Create Comment object
            comment = Comment(post=post, text=form['text'].data, created_by=request.user)
            comment.save()

            post.comments += 1
            post.save()

            data = {
                "message": "Comment created successfully",
                "comments_count": post.comments,
                "get_comments": reverse("get_wall_post_comments", kwargs={'post_pk':post_pk})
            }

            return JsonResponse({'data':data}, status=200)
        else:
            # Send 400 if comment is invalid

            data = {
                "error": form.errors
            }

            return JsonResponse({'data':data}, status=400)

@login_required
def delete_comment(request, comment_pk):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_pk)
        post = get_object_or_404(Post, pk=comment.post.id)

        comment.delete()

        post.comments -= 1
        post.save()

        data = {
            "message": "Comment deleted successfully",
            "comments_count": post.comments,
            "get_comments": reverse("get_wall_post_comments", kwargs={'post_pk':post.id})
        }

        return JsonResponse({'data':data}, status=200)

def get_post_comments(request, post_pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_pk)
        comments = Comment.objects.filter(post=post).order_by('-created_at')

        context = {
            "comments": comments,
        }

        return render(request, 'wall/post-comments.html', context)
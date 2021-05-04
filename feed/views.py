from django.views import generic
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def post_create(request, author):
    author=request.user
    if request.method == 'GET':
        return render(request, 'feed/post_create.html', {'form':PostForm()})
    else:
        try:
            form = PostForm(data=request.POST, files=request.FILES)
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return render(request, 'feed/feed.html', {'info':'Post created!'})
        except ValueError:
            return render(request, 'feed/post_create.html', {'form':PostForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return render(request, 'feed/feed.html', {'post':post, 'error':'The post has been deleted'})

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "feed/feed.html"
    paginate_by = 9

    # Function to test whether the current user is the author of the post he wants to edit
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#Allow public to see
def post_by_user(request, author):
    user = request.user

    posts = Post.objects.filter(author__username=author,status=1).order_by("-created_on")
    drafts = Post.objects.filter(author__username=author,status=0).order_by("-created_on")
    return render(request, 'feed/post_user.html', {'posts':posts,'drafts':drafts,'author':author})

def post_detail(request, slug, author):
    template_name = "feed/post_detail.html"
    post = get_object_or_404(Post, author__username=author, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None

    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.commenter = request.user
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

@login_required
def post_update(request, slug, author):
    post = get_object_or_404(Post, slug=slug, author__username=author)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'feed/post_update.html', {'form':form})
    else:
        try:
            form = PostForm(request.POST, request.FILES, instance=post)
            form.save()
            #Redirecting to main feed page because if slug has been changed, the url reverse will not work
            messages.success(request, 'Profile details updated.')
            return redirect('post_detail', author=author, slug=slug)
        except ValueError:
            return render(request, 'feed/post_update.html', {'form':form, 'error':'Bad info passed in. Try again?'})


@login_required
def post_delete(request, post_pk):
    form = get_object_or_404(Post, pk=post_pk, author=request.user)
    if request.method == 'POST':
        form.delete()
        return HttpResponseRedirect('feed/post_detail.html')

@login_required
def comment_delete(request, author, slug, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, commenter=request.user)
    post = get_object_or_404(Post, slug=slug, author__username=author)
    if request.method == 'POST':
        comment.delete()
        #To fix: adding message that the comment has been deleted
        return redirect('post_detail', author=author, slug=slug)
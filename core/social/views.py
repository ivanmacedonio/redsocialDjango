from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def feed (request):
    posts = Post.objects.all()
    context  = {'posts':  posts}
    return render(request,'feed.html',context)
@login_required
def profile(request):
    return render(request,'profile.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} ha sido creado!')
            return redirect('feed')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit = False)
            post.user = current_user
            post.save()
            messages.success(request,'Post enviado')
            return redirect('feed')
    else:
        form =PostForm()
    return render(request, 'post.html', {'form': form})

@login_required
def profile(request,username=None):
    current_user = request.user
    if username and username!= current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts= current_user.posts.all()
        user = current_user
    return render (request,'profile.html',{'user':user, 'posts': posts})

@login_required
def follow(request,username=None):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'sigues a {username}')
    return redirect ('feed')

@login_required
def unfollow(request,username=None):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a {username}')
    return redirect ('feed')

def like(request,id):
    current_user = request.user
    to_post = Post.objects.get(id=id)
    to_post_id = to_post
    rel = RelationshipLike(from_user = current_user, to_post = to_post_id)
    rel.save
    messages.success(request, f'Te ha gustado la publicacion!')
    return redirect('feed')

def unlike(request,id):
    current_user = request.user
    to_post = Post.objects.get(id=id)
    to_post_id = to_post
    rel = RelationshipLike.objects.filter(from_user = current_user, to_post = to_post_id).get()
    rel.delete()
    messages.success(request, f'Ya no te gusta la publicacion!')
    return redirect('feed')





from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from . models import Room, Topic, Message
from . forms import RoomForm
# Create your views here.
# lang = [
#     {"id": 1, "name": "Python"},
#     {"id": 2, "name": "JavaScript"},
#     {"id": 3, "name": "Java"},
#     {"id": 4, "name": "C++"},
#     {"id": 5, "name": "Ruby"},
#     {"id": 6, "name": "Swift"}
#     # Add more programming languages as needed
# ]

def registerFirst(request):
    
    page = 'registerPage'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'form':form}
    return render(request, 'register.html', context)


def register(request):
    page = 'login'
    # Stops user from logging in twice
    if request.user.is_authenticated:
        return redirect('index')
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('register')
            
        user = authenticate(request, username=username, password=password)
        
        if user != None:
            login(request, user)
            messages.success(request, 'User logged in')
            
            return redirect('index')
        else:
            messages.error(request, 'Password is incorrect')
            
    context = {'page':page}
    return render(request, 'register.html', context)

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    lang = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        
        )
    topics = Topic.objects.all()
    room_count = lang.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'langs': lang, 'topics':topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'index.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    langs = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'langs':langs, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)

@login_required(login_url='register')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('index')
    context = {'form':form}
    return render(request, 'form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form' : form }
    return render(request, 'form.html', context)

def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('index')
    context = {'obj' : room}
    return render(request, 'delete.html', context)

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('index')
    context = {'obj' : message}
    return render(request, 'delete.html', context)


def logoutUser(request):
    logout(request)
    return redirect('register')
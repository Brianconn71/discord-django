from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.

# rooms = [
#     {
#         'id': 1,
#         'name': 'Lets learn python'
#     },
#     {
#         'id': 2,
#         'name': 'maths is great'
#     },
#     {
#         'id': 3,
#         'name': 'java'
#     },
# ]


def loginPage(request):
    page ='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist.')

    template = 'base/login_register.html'
    context = {'page': page,}
    return render(request, template, context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Form data is invalid, please try again')

    template = 'base/login_register.html'
    context = {'form': form}

    return render(request, template, context)


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # if query contains some of the letters then it will return it i.e. py = python
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}

    template = 'base/home.html'

    return render(request, template, context)


def room(request, pk):

    room = Room.objects.get(id=pk)
    # message_set.all() finds all the children of the parent i.e. all the messages for a room.
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}

    template = 'base/room.html'

    return render(request, template, context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    template = 'base/profile.html'
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}

    return render(request, template, context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        # adding a way to create a new topic in form
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form,
               'topics': topics}

    template = 'base/room_form.html'

    return render(request, template, context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here.')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        # adding a way to create a new topic in form
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        
        return redirect('home')

    context = {'form': form,
               'topics': topics,
               'room': room}

    template = 'base/room_form.html'

    return render(request, template, context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    template = 'base/delete.html'
    
    return render(request, template, {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    template = 'base/delete.html'
    
    return render(request, template, {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    template = 'base/update-user.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    
    template = 'base/topics.html'
    context = {
        'topics': topics,
    }
    return render(request, template, context)


def activityPage(request):
    room_messages = Message.objects.all()
    template = 'base/activity.html'
    context = {
        'room_messages': room_messages,
        
    }
    return render(request, template, context)
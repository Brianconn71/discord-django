from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

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

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # if query contains some of the letters then it will return it i.e. py = python
    rooms = Room.objects.filter(topic__name__icontains=q)

    topics = Topic.objects.all()

    context = {'rooms': rooms, 'topics': topics}

    template = 'base/home.html'

    return render(request, template, context)


def room(request, pk):

    room = Room.objects.get(id=pk)

    context = {'room': room}

    template = 'base/room.html'

    return render(request, template, context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form }

    template = 'base/room_form.html'

    return render(request, template, context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form }

    template = 'base/room_form.html'

    return render(request, template, context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    template = 'base/delete.html'
    
    return render(request, template, {'obj': room})

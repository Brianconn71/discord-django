from django.shortcuts import render, redirect
from .models import Room
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
    rooms = Room.objects.all()
    context = {'rooms': rooms}
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


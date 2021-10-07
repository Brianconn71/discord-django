from django.shortcuts import render
from .models import Room

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

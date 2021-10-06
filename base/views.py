from django.shortcuts import render

# Create your views here.

rooms = [
    {
        'id': 1,
        'name': 'Lets learn python'
    },
    {
        'id': 2,
        'name': 'maths is great'
    },
    {
        'id': 3,
        'name': 'java'
    },
]

def home(request):
    context = {'rooms': rooms}
    template = 'base/home.html'
    return render(request, template, context)


def room(request, pk):
    room = None
    for x in rooms:
        if x['id'] == int(pk):
            room = i
    
    context = {'room': room}

    template = 'base/room.html'
    return render(request, template, context)

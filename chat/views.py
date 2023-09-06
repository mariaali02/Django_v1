from django.shortcuts import render


def indext(request):
    return render(request, 'flipcart/indext.html', {})


def room(request, room_name):
    return render(request, 'flipcart/chatroom.html', {
        'room_name': room_name
    })
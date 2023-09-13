from django.shortcuts import render
from django.contrib.auth.models import User
from flipcart.models import UserProfile
from apitest.serializers import UserSerializer,UserProfileSerializer
from django.http import HttpResponseNotFound

def indext(request):
    return render(request, 'flipcart/indext.html', {})



def room(request, room_name):
    data = {}
    if request.user.is_authenticated:
        userId = request.GET.get('userId')
        if userId:
            try:
                objUser = User.objects.get(pk=userId)
                serializer_user = UserSerializer(objUser)
                data['user'] = serializer_user.data['username']
            except User.DoesNotExist:
                # Handle the case where the user does not exist
                data['user'] = 'User not found'
        else:
            # Handle the case where 'userId' is not provided in the request
            data['user'] = 'User ID not provided'

        return render(request, 'flipcart/chatroom.html', {
            'room_name': room_name,
            'data': data,  # Pass the data to the template
        })
    else:
        # Handle the case where the user is not authenticated
        return HttpResponseNotFound('Authentication required')
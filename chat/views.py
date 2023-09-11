from django.shortcuts import render
from django.contrib.auth.models import User
from flipcart.models import UserProfile
from apitest.serializers import UserSerializer,UserProfileSerializer

def indext(request):
    return render(request, 'flipcart/indext.html', {})



def room(request, room_name):
    # Initialize an empty data dictionary
    data = {}

    # Check if the user is authenticated
    if request.user.is_authenticated:
        userId = request.GET.get('userId')

        # Check if userId is provided in the request
        if userId:
            try:
                # Attempt to retrieve the user by primary key (userId)
                objUser = User.objects.get(User, pk=userId)
                serializer_user = UserSerializer(objUser)
                data['user'] = serializer_user.data['username']
            except User.DoesNotExist:
                # Handle the case where the user does not exist
                data['user'] = 'User not found'

    return render(request, 'flipcart/chatroom.html', {
        'room_name': room_name,
        'data': data,  # Pass the data to the template
    })
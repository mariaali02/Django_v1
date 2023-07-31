# apitest/api/views.py
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDetail1(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, format=None):
        
        userId = request.GET['userId']
        userId = int(userId)
        if userId:
            queryset = User.objects.filter(pk=userId)
        else:
            queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        
        return Response(serializer.data)

class Hello(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        content = {
            'message': 'Hello World'
        }
        return Response(content)
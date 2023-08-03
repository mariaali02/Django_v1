# apitest/api/views.py
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status

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

    def put(self, request, format=None):        
        userId = int(request.query_params['userId']) if request.query_params['userId'] else None
        dicUser = {}
        dicUser["email"] = request.data['email']
        dicUser["username"] = request.data['username']
        try:
            if userId:
                objUser = User.objects.filter(pk=userId)
                res = objUser.update(**dicUser)
                if res:
                # serializer = UserSerializer(objUser, data=request.data)
                # if serializer.is_valid():
                #     serializer.save(5)
                    return Response({'message': 'saved successfully.'}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({'message': 'error.'}, status=status.HTTP_400_BAD_REQUEST)

            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'message': 'error.'}, status=status.HTTP_400_BAD_REQUEST)


class Hello(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        content = {
            'message': 'Hello World'
        }
        return Response(content)
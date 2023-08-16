# apitest/api/views.py
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer,ChangePasswordSerializer,RegisterSerializer,ResetPasswordEmailSerializer,SignInSerializer
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django_rest_passwordreset.signals import reset_password_token_created
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
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
    
    """def get(self, request, format=None):

        userId = request.GET['userId']
        userId = int(userId)
        if userId:
            queryset = User.objects.filter(pk=userId)
        else:
            queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)"""
        
    def get(self, request, format=None):
        
        userId = int(request.GET['userId']) if 'userId' in request.GET else None

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

    def delete(self, request, format=None):   
        if request.method == "DELETE":
            try:
                user_id = int(request.GET.get('userId'))
                objuser = User.objects.get(id=user_id)
                objuser.delete()
                return Response({"message": "User deleted successfully"}, status=200)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=404)
            except ValueError:
                return Response({"message": "Invalid user ID"}, status=400)
        else:
            return Response({"message": "Invalid request method"}, status=400)
    def post(self, request, format=None):  
        if request.method == 'POST':
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('old_password')):
                    user.set_password(serializer.data.get('new_password'))
                    user.save()
                    update_session_auth_hash(request, user)  # To update session after password change
                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
                return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
        """
        Handles password reset tokens
        When a token is created, an e-mail needs to be sent to the user
        :param sender: View Class that sent the signal
        :param instance: View Instance that sent the signal
        :param reset_password_token: Token Model Object
        :param args:
        :param kwargs:
        :return:
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}?token={}".format(
                instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
                reset_password_token.key)
        }

        # render email text
        email_html_message = render_to_string('email/password_reset_email.html', context)
        email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {title}".format(title="Your Website Title"),
            # message:
            email_plaintext_message,
            # from:
            "noreply@yourdomain.com",
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

@api_view(['POST'])
@permission_classes([AllowAny])
def registeruser(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)  # Return a JSON response
        return JsonResponse(serializer.errors, status=400)  # Return errors as JSON response

    return JsonResponse({'detail': 'Invalid request method'}, status=405)  # Return an error for other request methods


class SignIn(APIView):
    authentication_classes = ()

    def post(self, request, format=None):
        _userName = request.data['username'] if 'username' in request.data else None
        _password = request.data['password'] if 'password' in request.data else None
        if _userName and _password:
            objUser = authenticate(username=_userName, password=_password)
            if objUser:
                if objUser.is_authenticated:
                    if objUser.is_superuser:  # Admin sign-in
                        login(request, objUser)
                        url_success = reverse('SuperuserDashboard')  # Use correct URL name
                        return Response({'message': 'Admin sign-in successful', 'url': url_success})
                    else:  # Regular user sign-in
                        login(request, objUser)
                        url_success = reverse('UserDashboard')  # Use correct URL name
                        return Response({'message': 'User sign-in successful', 'url': url_success})

            return Response({'message': 'Sign-in failed'}, status=status.HTTP_401_UNAUTHORIZED)
def UserDashboard(request):
    users = User.objects.all()

    context = {
        'users': users

    }

    return render(request, 'flipcart/db.html', context)
def SuperuserDashboard(request):
    users = User.objects.all()

    context = {
        'users': users,
        'can_delete_update': True,  # Set a flag to indicate the superuser can delete and update

    }

    return render(request, 'flipcart/db.html', context)
"""
def user_dashboar(request):
    users = User.objects.all()
    # Serialize users data to JSON
    
    
    users_json = UserSerializer.serialize('json', users)
    
    context = {
        'users': users

    } 
    return JsonResponse(context)
def superuser_dashboard(request):
    users = User.objects.all()
    
    # Serialize users data to JSON
    users_json = UserSerializer.serialize('json', users)
    
    context = {
        'users': users_json,
        'can_delete_update': True,  # Set a flag to indicate the superuser can delete and update
    }
    
    return JsonResponse(context)"""
def userlogout(request):
        if request.method == 'POST':
            try:
                # Delete the user's token to logout
                request.user.auth_token.delete()
                return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class Hello(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        content = {
            'message': 'Hello World'
        }
        return Response(content)
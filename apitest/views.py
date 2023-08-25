# apitest/api/views.py
from datetime import datetime
from flipcart.models import UserProfile
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer,ChangePasswordSerializer,UserProfileSerializer,RegisterSerializer,ResetPasswordEmailSerializer,SignInSerializer
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
from django.contrib.auth import logout


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDetail1(APIView):
    authentication_classes = ()
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        userId = request.GET.get('userId')

        if userId:
            try:
                objUser = User.objects.get(pk=userId ,deleted=False)
                objUserProfile = UserProfile.objects.filter(user=objUser).first()

                serializer_user = UserSerializer(objUser)
                serializer_profile = UserProfileSerializer(objUserProfile)
                content = {
                    'user' : serializer_user.data['username'],
                    'email' : serializer_user.data['email'],
                    'date_of_birth' : serializer_profile.data['date_of_birth'],
                    'gender': serializer_profile.data['gender'],
                    'phone_number':serializer_profile.data['phone_number'],
                }
                return Response({'data' : content}, status=200)

            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        else:
            try:
                collectionUser = User.objects.all().exclude(deleted = True)
                data = []
                for objUser in collectionUser:
                    objUserProfile = UserProfile.objects.filter(user=objUser.id).first()
                    content = {
                        
                        'userId':objUser.id,
                        'user' : objUser.username,
                        'email' : objUser.email,
                        'date_of_birth' : objUserProfile.date_of_birth if objUserProfile else None,
                        'gender': objUserProfile.gender if objUserProfile else None,
                        'phone_number': str(objUserProfile.phone_number) if objUserProfile else None
                    }
                    data.append(content)
                return Response({'data': data}, status=200)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)

    """     
    def get(self, request, format=None):
        
        userId = int(request.GET['userId']) if 'userId' in request.GET else None

        if userId:
            objuser = User.objects.filter(pk=userId)
        else:
            objuser = User.objects.all()
        serializer = UserSerializer(objuser, many=True)

        return Response(serializer.data)"""












        
    """"""    
    """
    
    
                if 'user' in request.data:
                    objUser.username = request.data['user']
                if 'email' in request.data:
                    objUser.email = request.data['email']
                if 'date_of_birth' in request.data:
                    objUserProfile.date_of_birth = request.data['date_of_birth']
                if 'gender' in request.data:
                    objUserProfile.gender = request.data['gender']
                if 'phone_number' in request.data:
                    objUserProfile.phone_number = request.data['phone_number']

                objUser.save()
                objUserProfile.save()"""
                
                
    def put(self, request, format=None):        
        userId = int(request.query_params['userId']) if request.query_params['userId'] else None
        dicUser = {}
        if 'email' in request.data:
            dicUser["email"] = request.data['email']
        if 'username' in request.data:
            dicUser["username"] = request.data['username']
        proUser = {}
        if 'date_of_birth' in request.data:
            proUser["date_of_birth"] = request.data['date_of_birth']
        if 'gender' in request.data:
            proUser["gender"] = request.data['gender']
        if 'phone_number' in request.data:
            proUser["phone_number"] = request.data['phone_number']
        
            if userId:
                collectionUser = User.objects.filter(pk=userId)
                res = collectionUser.update(**dicUser)
                objUserProfile =  UserProfile.objects.filter(user= collectionUser.first().id)
                if  objUserProfile.exists():
                    res =  objUserProfile.update(**proUser)
                else:
                    collectionUser = UserProfile.objects.create(user=collectionUser.first(),**proUser)
                    res =  objUserProfile.update(**proUser)
                if res:
                # serializer = UserSerializer(objUser, data=request.data)
                # if serializer.is_valid():
                #     serializer.save(5)
                    return Response({'message': 'saved successfully.'}, status=status.HTTP_200_RESET_CONTENT)
            else:
                return Response({'message': 'error.'}, status=status.HTTP_400_BAD_REQUEST)

            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
        
class registeruser(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()

    def post(self, request, format=None):
        if request.method == 'POST':
            objUser = User.objects.create_user(
                username=request.data["username"],
                password=request.data["password"],
                email=request.data["email"]
            )

            email = request.data.get('email')
            date_of_birth_str = request.data.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
            gender = request.data.get('gender')
            phone_number = request.data.get('phone_number')

            objUserProfile = UserProfile.objects.create(
                user=objUser,
                Email=email,
                date_of_birth=date_of_birth ,
                gender=gender,
                phone_number=phone_number
            )

            objUserProfile.save()

            return JsonResponse({'message': 'User profile created successfully.'}, status=201)
        
        return JsonResponse({'detail': 'Invalid request method'}, status=405)


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

class SignOut(APIView):

    permission_classes = [permissions.AllowAny]
    authentication_classes = ()
    
    def post(self, request, format=None):
        
        logout(request)
        url_success = reverse('logout')  # Use correct URL name
        return Response({'message': 'Successfully logged out.', 'url': url_success }, status=status.HTTP_200_OK)
    
            
def logout(request):
    
    return render(request, "flipcart/signout.html")




            
class Hello(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        content = {
            'message': 'Hello World'
        }
        return Response(content)
    
class SoftDeleteUser(APIView):
    def delete(self, request, format=None):
        if request.method == "DELETE":
            try:
                user_id = int(request.GET.get('userId'))
                deleted_by_user = request.user  # Get the user who is performing the deletion
                objUserProfile = UserProfile.objects.get(id=user_id)
                objUserProfile.soft_delete(deleted_by_user)
                return Response({"message": "User soft deleted successfully"}, status=200)
            except UserProfile.DoesNotExist:
                return Response({"message": "User not found"}, status=404)
            except ValueError:
                return Response({"message": "Invalid user ID"}, status=400)
        else:
            return Response({"message": "Invalid request method"}, status=400)
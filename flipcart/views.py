from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    return render(request, "flipcart/home.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        dbirth = request.POST['date_of_birth']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password != cpassword:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists. Please choose a different username.")
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email is already registered. Please use a different email.")

            # Create a new user
            myuser = User.objects.create_user(username, email, password,)
            # Save the user
            myuser.save()

            # Redirect to the home page or any other desired page
            return redirect('msg')

    return render(request, "flipcart/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            users = User.objects.all()

            context = {
                'users': users,
                'can_delete_update': True,  # Set a flag to indicate the superuser can delete and update
            }
            return render(request, "flipcart/db.html", context)
        elif user is not None and user.is_authenticated:
            login(request, user)
            return render(request, "flipcart/db.html")
        else:
            error_message = "Invalid username or password."
            return render(request, "flipcart/invalid.html", {'error_message': error_message})

    return render(request, "flipcart/signin.html")



@login_required(login_url="/signin")
def page1(request):   
    return render(request, "flipcart/hello.html")
def hello_world(request):
    users = User.objects.all()

    context = {
        'users': users

    }




    return render(request, 'flipcart/db.html', context)


def signout(request):
    logout(request)
    
    return render(request, "flipcart/signout.html")
def msg(request):
    return render(request, "flipcart/msg.html")
"""
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('hello_world')
        else:
            error_message = "Invalid username or password."
            return HttpResponse("invalid user")

    return render(request, 'flipcart/login.html')

"""
""""
@login_required(login_url="/signin")
def create_user(request):
    if request.method == "POST":
        username = request.POST['username']
        dbirth = request.POST['date_of_birth']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password != cpassword:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists. Please choose a different username.")
            if User.objects.filter(email=email).exists():
                return HttpResponse("Email is already registered. Please use a different email.")

            # Create a new user
            myuser = User.objects.create_user(username, email, password,)
            # Save the user
            myuser.save()

            # Redirect to the home page or any other desired page
            return redirect('msg')
"""
@login_required
def dlt_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, "The user is deleted.")
    except User.DoesNotExist:
        messages.error(request, "The user does not exist.")
    return redirect('signin')


@login_required
def update_user(request,user_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to update users.")
        return redirect('signin')

    if request.method == "POST":
        try:
            user = User.objects.get(user=user_id)
            username = request.POST.get('username')
            email = request.POST.get('email')
            date_of_birth = request.POST.get('date_of_birth')

            user.username = username
            user.email = email
            user.date_of_birth = date_of_birth
            user.save()
            messages.success(request, "User updated successfully.")
            return redirect('signin')
        except User.DoesNotExist:
            messages.error(request, "The user does not exist.")
    return redirect('signin')

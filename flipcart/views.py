from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
def home(request):
    return render(request, "flipcart/home.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        dbirth = request.POST['date_of_birth']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password!=cpassword:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            myuser = User.objects.create_user(username, email, password)
            myuser.save()
        return redirect('signin')
    return render(request, "flipcart/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect ('hello_world')
        else:
            error_message = "Invalid username or password."  # Add an error message if authentication fails
            return render(request, "flipcart/invalid.html", {'error_message': error_message})

    return render(request, "flipcart/signin.html")
@login_required(login_url="/signin")
def hello_world(request):
    return render(request, "flipcart/hello.html")


def signout(request):
    logout(request)
    messages.success(request, "logout successfully")
    return render(request, "flipcart/home.html")

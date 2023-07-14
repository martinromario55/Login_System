from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):

    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        # Get data from form
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # validation
        password = ''
        if password1 == password2:
            password = password1
        else:
            messages.warning(request, 'Passwords don\'t match.')
            return redirect('signup')
        
        # Check if username already taken
        if User.objects.filter(username=username):
            messages.warning(request, "Username already taken!")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.warning(request, "Email address already registered!")
            return redirect('signup')
        
        if len(username) > 10:
            messages.warning(request, "Username cannot be longer than ten characters")
            return redirect('signup')
        
        if not username.isalnum():
            messages.warning(request, "Username must be alpha numeric")
            return redirect('signup')

        # Get User model
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name

        myuser.save()

        # message
        messages.success(request, "Your Account has been successfully created")
        
        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):
    # Get input data
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(username=username, password=password)

        # Check if user exists
        if user is not None:
            login(request, user)
            first_name = user.first_name

            messages.success(request, "You've successfully logged in!")

            return render(request, "authentication/index.html", {'first_name': first_name})
        else:
            messages.warning(request, "Invalid username or password!")
            return redirect('signin')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.info(request, "Logged Out Successful")

    return redirect("home")
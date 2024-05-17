from .models import Profile

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import EditProfileForm


# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponse(f"You are logged in with a username <b> {request.user.username} </b> you are a login!")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse(f"You successfully with the user <b> {user.username} </b> you were logged in!")
            else:
                return HttpResponse('Invalid username or password')

    return render(request, "account_module/login-page.html")


def logout_user(request):
    logout(request)
    return HttpResponse("You got out of the account!")


def register_user(request):
    if request.user.is_authenticated:
        return HttpResponse(f"You are logged in with a username <b> {request.user.username} </b> you are a login!")
    else:
        if request.method == 'POST':
            context = {
                'errors': [],
                'message': []
            }
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if password != confirm_password:
                context['errors'].append("passwords don't match")
                return render(request, "account_module/register-page.html", context)
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                context["message"].append(f'Account created for {username}')
                return render(request, "account_module/register-page.html", context)

        else:
            return render(request, "account_module/register-page.html")

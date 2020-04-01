from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from commuters.models import Commuters

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def drivers(request):
    return render(request, 'drivers.html')

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def login_user(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            try:
                if user.groups.get().name == "commuter":
                    login(request, user)
                    try:
                        Commuters.objects.get(user_id=request.user)
                        if user.is_active:
                            return HttpResponseRedirect(reverse('commuters:announcements'))
                    except:
                        return HttpResponseRedirect(reverse('commuters:create_commuter'))
            except:
                message = "Invalid username or password. Please try again."
        message = "Invalid username or password. Please try again."
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('commuters:view_my_routes'))
    return render(request, 'login.html', {'message':message})


def signup_user(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            commuter_group = Group.objects.get(name='commuter') 
            commuter_group.user_set.add(user)
            user.save()
            message = "Kindly Sign In"
            return render(request, 'login.html', {'message':message})
        else:
            pass
    else:
        user_form = UserForm()
    return render(request, 'signup_user.html', {
            'form':user_form,
            'registered':registered,
        })
from django.shortcuts import render

def home(request):
    return render(request, 'help_home.html')

def pasahero(request):
    return render(request, 'help_pasahero.html')

def admin(request):
    return render(request, 'help_admin.html')

def super_admin(request):
    return render(request, 'help_super_admin.html')
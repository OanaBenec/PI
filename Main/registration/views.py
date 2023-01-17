from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .register import register
from .passReset import sendPasswordResetLink

def acc_login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', content_type="text/html")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/main/" + user.last_name)

        return render(request, 'error.html', {'err': 401}, content_type="text/html", status=401)
    
def acc_register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html', content_type="text/html")
    return register(request)

def reset_pass_form(request, rand):
    pass
    
def reset_pwd(request):
    if request.method == 'GET':
        return render(request, 'registration/password_reset.html', content_type="text/html")
    
    mail = request.POST['email']
    sendPasswordResetLink(request, mail)
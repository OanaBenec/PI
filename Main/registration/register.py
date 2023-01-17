from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def register(request):
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    cpassword = request.POST['cpassword']
    
    if password == cpassword:
        try:
            User.objects.get(username=username)
            
            return render(request, 'registration/register.html', {'err': 'userExists'}, content_type="text/html", status=409)
        except User.DoesNotExist:
            user = User.objects.create_user(username, username, password)
            user.last_name = name
            user.save()
            
            auth = authenticate(request, username=username, password=password)
            if auth is not None:
                login(request, user)
                return redirect("/main/" + auth.last_name)

            return render(request, 'error.html', {'err': 500}, content_type="text/html", status=500)
    return render(request, 'registration/register.html', {'err': 'password'}, content_type="text/html", status=409)
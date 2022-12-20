from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from random import randint

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
    
def demo(request, name, id):
    if request.method == 'GET':
        return render(request, 'demo.html', {'name': name, 'id' : id})
    
def isPrime(x):
    if x % 2 == 0:
        return 0
    i = 3
    while(i * i <= x):
        if(x % i == 0):
            return 0
        i+=2
    return 1
    
def run_evaluation(request, name, id):
    if request.method == 'GET':
        data = ""
        code = request.GET.get('code')
        for i in range(6):
            X = randint(0, 10000)

            data += str(X) + ";" + str(isPrime(X)) + "\n"
        return render(request, 'passed_failed_tests.html', {'data': data, 'id' : id, 'code': code})
    
def welcome(request, name):
    if request.method == 'GET':
        return render(request, 'welcome.html', {'name': name})
    
def reset_pwd(request):
    if request.method == 'GET':
        return render(request, 'registration/password_reset.html', content_type="text/html")
    
    mail = request.POST['email']
    try:
        user = User.objects.get(username=mail)
    
        subject = "Password Reset Requested"
        email_template_name = "registration/password_reset_email.html"
        c = {
            "email":user.email,
            'domain':'127.0.0.1:8000',
            'site_name': 'Website',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        email = render_to_string(email_template_name, c)
        try:
            send_mail(subject, email, 'david.bnicolae@gmail.com' , [user.email], fail_silently=False)
            print(email)
            return redirect("/login")
        except BadHeaderError:
            return render(request, 'error.html', {'err': 500}, content_type="text/html", status=500)
    except User.DoesNotExist:
        return render(request, 'error.html', {'err': 404}, content_type="text/html", status=404)
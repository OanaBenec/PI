from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.shortcuts import render, redirect

def sendPasswordResetLink(request, mail):
    try:
        user = User.objects.get(username=mail)
    
        subject = "Password Reset Requested"
        email_template_name = "registration/password_reset_email.html"
        c = {
            "email":user.email,
            'domain':'127.0.0.1:8000',
            'site_name': 'AnonTester',
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
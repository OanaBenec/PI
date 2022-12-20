from django.urls import path

from . import views

urlpatterns = [
    path('', views.acc_login),
    path('register', views.acc_register),
    path('password_reset', views.reset_pwd),
    path('main/<str:name>', views.welcome),
    path('main/<str:name>/tests/<int:id>', views.demo),
    path('main/<str:name>/tests/<int:id>/evaluate', views.run_evaluation)
]
from django.urls import path

from . import views
from .registration import views as authViews

urlpatterns = [
    path('', authViews.acc_login),
    path('register', authViews.acc_register),
    path('password_reset', authViews.reset_pwd),
    path('password_reset/<str:rand>', authViews.reset_pass_form),
    
    path('main/<str:name>', views.welcome),
    
    path('main/<str:name>/courses', views.show_courses),
    path('main/<str:name>/courses/view', views.view_course),
    path('main/<str:name>/courses/add', views.add_course),
    path('main/<str:name>/courses/add_lesson', views.add_lesson),
    path('main/<str:name>/courses/add_lesson/post', views.add_lesson2),
    path('main/<str:name>/courses/add_exercise', views.add_ex),
    path('main/<str:name>/courses/add_exercise/post', views.add_ex2),
    path('main/<str:name>/courses/add_homework', views.add_hw),
    path('main/<str:name>/courses/add_homework/post', views.add_hw2),
    path('main/<str:name>/courses/browse', views.show_courses),

    path('main/<str:name>/tests/<int:id>', views.demo),
    path('main/<str:name>/tests/', views.show_tests),
    path('main/<str:name>/tests/add', views.add_test),

    path('tests/generateOutput/<int:id>', views.get_output)
]
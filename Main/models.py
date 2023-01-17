from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lesson(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

class Lecture(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class Test(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=255)
    output_generator = models.CharField(max_length=255)
    no_test_cases = models.IntegerField()
    save_sources = models.IntegerField()
    homework = models.IntegerField()
    exercise = models.IntegerField()
    due_date = models.DateTimeField()
    start_date = models.DateTimeField()

class Linkage(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Input(models.Model):
    data_type = models.CharField(max_length=30)
    values = models.CharField(max_length=255)
    name = models.CharField(max_length=30)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
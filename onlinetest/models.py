from django.contrib.auth.models import Permission, User
from django.db import models
from django.utils import timezone
import os
import random

# funcion for renaming uploaded files before storing them in the database
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s%s%s.%s" % (instance.user.username, instance.user.id + 1000, instance.test_title, ext)
    return os.path.join('', filename)

class Test(models.Model):
    user = models.ForeignKey(User, default=1)
    test_title = models.CharField(max_length=250)
    test_marks = models.CharField(max_length=30)
    test_questions = models.CharField(max_length=30)
    test_time = models.CharField(max_length=30)
    test_file = models.FileField(default='', upload_to=content_file_name)
    test_number = models.CharField(max_length=30)
    def __str__(self):
        return self.test_title

class studentProfile(models.Model):
    """Profile for a user to store roll number and other details."""
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=120, unique=True)
    password = models.CharField(max_length=50, default=None)
    institute = models.CharField(max_length=50, default=None)
    client = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.email   

class question(models.Model):
    """questions in ques paper"""
    question_id = models.CharField(max_length=30)
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=500)
    questionType = models.CharField(max_length=10)

class quesFile(models.Model):
    """ques paper"""
    ques_paper_id = models.CharField(max_length=50, unique=True)
    client = models.CharField(max_length=50)

class studentMark(models.Model):
    """student marks"""
    ques_paper_id = models.CharField(max_length=50)
    email = models.EmailField(max_length=120, unique=True)
    marks = models.CharField(max_length=50)


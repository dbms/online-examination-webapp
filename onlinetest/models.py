from django.db import models
from django.utils import timezone


class clientsTable(models.Model):
    orgname = models.CharField(max_length=30)
    email = models.CharField(max_length=120, unique=True)
    orgSize = models.CharField(max_length=20)
    orgType = models.CharField(max_length=100)
    contactNumber = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    pwd= models.CharField(max_length=80)
   
    def __str__(self):
        return self.email

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


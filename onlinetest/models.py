from django.contrib.auth.models import Permission
from django.db import models
from datetime import datetime
import os
import random


class clientsTable(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=120, unique=True)
    contactNumber = models.CharField(max_length=15)
    pwd = models.CharField(max_length=80)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.email


class testDetails(models.Model):
    test_id = models.CharField(max_length=50, unique=True)
    client_id = models.CharField(max_length=100, default=0)
    testtitle = models.CharField(max_length=250)
    testduration = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.test_id


class studentProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=120, unique=True)
    password = models.CharField(max_length=50, default=None)
    rollno = models.CharField(max_length=50, default=None)
    client = models.CharField(max_length=50, default=None)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.email


class question(models.Model):
    question_id = models.CharField(max_length=30)
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.question    

class studentMark(models.Model):
    studentid = models.CharField(max_length=120,default=0)
    ques_paper_id = models.CharField(max_length=50)
    marks = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    testtitle = models.CharField(max_length=50)
    client = models.CharField(max_length=50, default=None)
    date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.email 
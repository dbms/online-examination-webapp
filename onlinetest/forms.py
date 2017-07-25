import datetime
from django import forms
from django.contrib.auth.models import User

# for client registration
class clientRegisterForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=120)
    contactNumber = forms.CharField(max_length=15)
    pwd= forms.CharField(max_length=80)

# for saving test detials
class savetestdetails(forms.Form):
    testtitle = forms.CharField(max_length=100)
    testduration = forms.CharField(max_length=10)

#for submitting marks
class saveMarks(forms.Form):
    totalmarks = forms.CharField(max_length=20)

# for client login
class LoginForm(forms.Form):
    email=forms.CharField(max_length = 80)
    pwd= forms.CharField(max_length=80)

#for student login
class StudenLoginForm(forms.Form):
    email = forms.CharField(max_length=120)
    password = forms.CharField(max_length=50)

#for student registration
class StudentRegForm(forms.Form):
    email = forms.CharField(max_length=120)
    name = forms.CharField(max_length=100)
    rollno = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    client = forms.CharField(max_length=50)

# for validating test ID
class TestIdVal(forms.Form):
    test_id=forms.CharField(max_length = 250)

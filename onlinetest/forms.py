import datetime
from django import forms
from django.contrib.auth.models import User

# for saving test details
# class TestForm(forms.ModelForm):

#     class Meta:
#         model = Test
#         fields = ['test_title', 'test_marks', 'test_questions', 'test_time', 'test_file','client_id']

# for client registration
class clientRegisterForm(forms.Form):
    email = forms.CharField(max_length=120)
    contactNumber = forms.CharField(max_length=15)
    pwd= forms.CharField(max_length=80)

# for saving test detials
class savetestdetails(forms.Form):
    testtitle = forms.CharField(max_length=100)
    NumberOfQue = forms.CharField(max_length=10)
    testduration = forms.CharField(max_length=10)

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

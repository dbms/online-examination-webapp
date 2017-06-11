import datetime
from django import forms


class clientRegister(forms.Form):
    orgname = forms.CharField(max_length=50)
    email = forms.CharField(max_length=120)
    orgSize = forms.CharField(max_length=10)
    orgType = forms.CharField(max_length=50)
    contactNumber = forms.CharField(max_length=15)
    address = forms.CharField(max_length=200)
    pwd= forms.CharField(max_length=80)

class LoginForm(forms.Form):
    email=forms.CharField(max_length = 80)
    pwd= forms.CharField(max_length=80)

class studenLoginForm(forms.Form):
    email = forms.CharField(max_length=120)
    password = forms.CharField(max_length=50)

class StudentInfo(forms.Form):
    email = forms.CharField(max_length=120)
    name = forms.CharField(max_length=30)
    institute = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    client = forms.CharField(max_length=50)

"""
class AddTopicForm(forms.Form):
    topic_text=forms.CharField(max_length = 250)
    topic_desc=forms.CharField(max_length = 700)
    tag_text=forms.CharField(max_length = 250)

class AddOpinionForm(forms.Form):
    opinion_text=forms.CharField(max_length = 500)
    topic = forms.CharField(max_length = 5)
"""


class SearchForm(forms.Form):
    topic_text=forms.CharField(max_length = 250)
    #symptom=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,required=False)


class TestIdVal(forms.Form):
    test_id=forms.CharField(max_length = 250)

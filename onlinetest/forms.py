import datetime
from django import forms
from django.contrib.auth.models import User
from .models import Test

class TestForm(forms.ModelForm):

    class Meta:
        model = Test
        fields = ['test_title', 'test_marks', 'test_questions', 'test_time', 'test_file']

class ClientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudenLoginForm(forms.Form):
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

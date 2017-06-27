from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, render_to_response
# This may be used instead of Users.DoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .forms import clientRegisterForm, StudenLoginForm, TestIdVal, LoginForm, StudentRegForm, StudenLoginForm, savetestdetails
from django.views.decorators.csrf import csrf_protect
# for older versoins of Django use:
# from django.core.urlresolvers import reverse
import ast
from .models import studentProfile, question, testDetails, studentMark, clientsTable
import onlinetest.file_reader
from django.utils.timezone import datetime

import random
# from Crypto.cipher import AES

# from main.forms import SignupForm,LoginForm,SearchForm#,AddTopicForm,AddOpinionForm,

EXCEL_FILE_TYPES = ['xlsx']


marks = 0
ques_no = 0
questions = []

# for redirecting to home page


def index(request):
    return render(request, 'onlinetest/index.html')

# for redirecting to student login page


def studentlogin(request):
    return render(request, 'onlinetest/studentlogin.html')

# for redirecting to client registration page


def clientregister(request):
    return render(request, 'onlinetest/clientregister.html')

# for redirecting to client login page


def clientlogin(request):
    return render(request, 'onlinetest/clientlogin.html')


def addtest(request):
    uid = request.session['user_id']
    client = clientsTable.objects.get(pk=uid)
    return render(request, 'onlinetest/addtest.html', {'client_id': client})

# for redirecting to testID page


def studenthome(request):
    return render(request, 'onlinetest/studenthome.html')


def home(request):
    if request.session.has_key('user_id'):
        uid = request.session['user_id']
        try:
            clientobj = clientsTable.objects.get(pk=uid)
            testinfo = testDetails.objects.filter(client_id=uid)
            return render(request, 'onlinetest/clientadmin.html', {'client_id': clientobj, 'test': testinfo})
        except clientsTable.DoesNotExist:
            return HttpResponse("User not found")
    else:
        return render(request, 'onlinetest/index.html')

# for validating client login and redirecting to admin panel


def clientloginVal(request):
    if request.method == 'POST':
        log = LoginForm(request.POST)
        if log.is_valid():
            try:
                user = clientsTable.objects.get(email=log.cleaned_data.get(
                    'email'), pwd=log.cleaned_data.get('pwd'))
                request.session['user_id'] = user.id
                useremail = user.email
                return HttpResponseRedirect(reverse('onlinetest:home'))
            except clientsTable.DoesNotExist:
                return HttpResponse("Wrong Username or Password")

# for client registration and redirecting to admin panel


def adminhome(request):
    try:
        if request.method == 'POST':
            signup = clientRegisterForm(request.POST)
            if signup.is_valid():
                p = clientsTable(
                    email=signup.cleaned_data.get('email'),
                    contactNumber=signup.cleaned_data.get('contactNumber'),
                    pwd=signup.cleaned_data.get('pwd'),
                )
                p.save()
                request.session['user_id'] = p.id
        return HttpResponseRedirect(reverse('onlinetest:home'))
    except:
        return HttpResponse("error occured")

# for adding test details


def simple_upload(request):
    form = savetestdetails(request.POST or None, request.FILES or None)
    if request.method == 'POST' and request.FILES['myfile'] and form.is_valid:
        now = str(datetime.now().strftime("%Y%m%d%H%M"))
        myfile = request.FILES['myfile']
        ext = myfile.name[myfile.name.rfind('.'):]
        fs = FileSystemStorage()
        filename = fs.save(now + ext, myfile)
        onlinetest.file_reader.file_to_db(
            filename, str(request.session['user_id']), now)
        uploaded_file_url = fs.url(filename)
        p = testDetails(
            test_id=now,
            client_id=str(request.session['user_id']),
            testtitle='testtitle',
            NumberOfQue='NumberOfQue',
            testduration='testduration',
        )
        p.save()
        return render(request, 'onlinetest/addtest.html', {
            'uploaded_file_url': now,
        })
    return render(request, 'onlinetest/addtest.html', {'client_id': client})

# for deleting test


def deletetest(request, test_id):
    test = Test.objects.get(pk=test_id)
    test.delete()
    tests = Test.objects.filter(user=request.user)
    return render(request, 'onlinetest/clientadmin.html', {'tests': tests})


def clientadmin(request):
    if not request.user.is_authenticated():
        return render(request, 'onlinetest/clientlogin.html')
    else:
        tests = Test.objects.filter(user=request.user)
        return render(request, 'onlinetest/clientadmin.html', {'tests': tests})

def paper_submit(request):
    global marks
    if request.method == 'POST':
        # marks = request.POST.get('kks')
        # return HttpResponse(marks)
        marks = random.randint(0, 4)

    test_id = request.session['test_id']
    student_id = request.session['studentuid']
    student = studentProfile.objects.get(pk=student_id)
    studentMark.objects.create(ques_paper_id=test_id,
                               email=student.email, marks=marks)
    return HttpResponseRedirect(reverse('onlinetest:index'))
# for logout


def clientlogout(request):
    try:
        del request.session['user_id']
        return HttpResponseRedirect(reverse('onlinetest:index'))
    except:
        pass
    return HttpResponseRedirect(reverse('onlinetest:index'))


# for validating test ID and redirecting to student home
def studentReg(request):
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        try:
            testfile_id = testDetails.objects.get(test_id=test_id)
            request.session['test_id'] = test_id
        except quesFile.DoesNotExist:
            return HttpResponse("Invalid test ID")
        return render(request, 'onlinetest/studenthome.html', {'testid': testfile_id})


# for validating student
def studentLogincheck(request):
    global questions
    if request.method == 'POST':
        log = StudenLoginForm(request.POST)
        if log.is_valid():
            try:
                # return HttpResponse("email" + log.cleaned_data.get('email') + "pass" + log.cleaned_data.get('password'))
                user = studentProfile.objects.get(email=log.cleaned_data.get('email'),
                                                  password=log.cleaned_data.get('password'))
                request.session['studentuid'] = user.id
                test_id = request.session.get('test_id')
                return HttpResponseRedirect(reverse('onlinetest:yourtest'))
            except clientsTable.DoesNotExist:
                return HttpResponse("Wrong Username Password")

# for student registration


def studentRegSave(request):
    try:
        if request.method == 'POST':
            addstudent = StudentRegForm(request.POST)
            test_id = request.session.get('test_id')
            testid = testDetails.objects.filter(test_id=test_id)
            if addstudent.is_valid():
                p = studentProfile(
                    name=addstudent.cleaned_data.get('name'),
                    email=addstudent.cleaned_data.get('email'),
                    rollno=addstudent.cleaned_data.get('rollno'),
                    password=addstudent.cleaned_data.get('password'),
                    client=addstudent.cleaned_data.get('client'),
                )
                p.save()
                request.session['studentuid'] = p.id
        return HttpResponseRedirect(reverse('onlinetest:yourtest'))
    except:
        return HttpResponse("error occured")

def yourtest(request):
    if request.session.has_key('studentuid') and request.session.has_key('test_id'):
        studentid = request.session['studentuid']
        testid = request.session['test_id']
        # try:
        user = studentProfile.objects.get(pk=studentid)
        ques = question.objects.filter(question_id=testid)
        return render(request, 'onlinetest/yourtest.html', {'user_id': user, 'ques': ques})
        # except:
        return HttpResponse("User not found")
    else:
        return render(request, 'onlinetest/index.html')


def studentmarksdisplay(request):
    sinfo = studentProfile.objects.all()
    smarks = studentMark.objects.all()
    return render(request, 'onlinetest/studentmarks.html', {'smarks': smarks, 'sinfo': sinfo})

# for displaying student info in admin panel


def studentInfo(request):
    sinfo = studentProfile.objects.all()
    smarks = studentMark.objects.all()
    return render(request, 'onlinetest/studentmarks.html', {'smarks': smarks, 'sinfo': sinfo})

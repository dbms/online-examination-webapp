from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist  # This may be used instead of Users.DoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .forms import LoginForm
from .forms import clientRegister, studenLoginForm, StudentInfo, TestIdVal
# for older versoins of Django use:
# from django.core.urlresolvers import reverse
import ast
from .models import clientsTable, studentProfile, question, quesFile, studentMark
import onlinetest.file_reader
from django.utils.timezone import datetime

import random
#from Crypto.cipher import AES

# from main.forms import SignupForm,LoginForm,SearchForm#,AddTopicForm,AddOpinionForm,

marks = 0
ques_no = 0
questions = []

def index(request):
    return render(request, 'onlinetest/index.html')


def studentlogin(request):
    return render(request, 'onlinetest/studentlogin.html')


def clientlogin(request):
    return render(request, 'onlinetest/clientlogin.html')


def clientregister(request):
    return render(request, 'onlinetest/clientregister.html')


def clientadmin(request):
    if request.session.has_key('user_id'):
        uid = request.session['user_id']
        try:
            user = clientsTable.objects.get(pk=uid)
            ques_paper = quesFile.objects.get(client=str(request.session['user_id']))
            clientid = ques_paper.client
            tabledata = studentProfile.objects.all()
            return render(request, 'onlinetest/clientadmin.html', {'user_id': user, 'tabledata': tabledata, 'clientid': clientid})
        except clientsTable.DoesNotExist:
            return render(request, 'onlinetest/clientlogin.html')
        except quesFile.DoesNotExist:
            return render(request, 'onlinetest/clientadmin.html')
    else:
        return render(request, 'onlinetest/clientlogin.html')


def studenthome(request):
    return render(request, 'onlinetest/studenthome.html')


def yourtest(request):
    global questions
    global marks
    global ques_no
    total = len(questions)
    marks = 0
    #return HttpResponse(total)
    if request.method == 'POST':
        if request.POST.get('prev') != None:
            ques_no = ques_no - 1
        elif request.POST.get('next') != None:
            ques_no = ques_no + 1
        elif request.POST.get('marks') != None:
            marks = request.POST.get('marks')
        
    #return HttpResponse(str(ques_no) + " " + str(total))             
    if ques_no >= total:
        #return HttpResponse(questions[total-1].question)
        return render(request, 'onlinetest/yourtest.html',{'question': questions[total-1], 'marks': marks})
    elif ques_no < 0:
        #return HttpResponse(questions[0].question)
        return render(request, 'onlinetest/yourtest.html',{'question': questions[0], 'marks': marks})
    else:
        #return HttpResponse(questions[ques_no].question)
        return render(request, 'onlinetest/yourtest.html',{'question': questions[ques_no], 'marks': marks})


def paper_submit(request):
    global marks
    if request.method == 'POST':
        #marks = request.POST.get('kks')
        #return HttpResponse(marks)
        marks = random.randint(0,4)
    
    test_id = request.session['test_id']
    student_id = request.session['studentuid']
    student = studentProfile.objects.get(pk=student_id)
    studentMark.objects.create(ques_paper_id=test_id, email=student.email, marks=marks)
    return HttpResponseRedirect(reverse('onlinetest:index')) 

def clientloginval(request):
    if request.method == 'POST':
        log = LoginForm(request.POST)
        if log.is_valid():
            try:
                user = clientsTable.objects.get(email=log.cleaned_data.get('email'), pwd=log.cleaned_data.get('pwd'))
                request.session['user_id'] = user.id
                useremail = user.email
                return HttpResponseRedirect(reverse('onlinetest:clientadmin'))
            except clientsTable.DoesNotExist:
                return HttpResponse("Wrong Username or Password")


def clientlogout(request):
    try:
        del request.session['user_id']
        return HttpResponseRedirect(reverse('onlinetest:index'))
    except:
        pass
    return HttpResponseRedirect(reverse('onlinetest:index'))


# for validating test ID

def testIdVal(request):
    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        try:
            testfile_id = quesFile.objects.get(ques_paper_id=test_id)
            request.session['test_id'] = test_id
        except quesFile.DoesNotExist:
            return HttpResponse("Wrong Username Password")
        # return HttpResponse("car " + test_id)
        return render(request, 'onlinetest/studenthome.html', {'testfile_id': testfile_id})


def studentLogincheck(request):
    global questions
    if request.method == 'POST':
        log = studenLoginForm(request.POST)
        if log.is_valid():
            try:
                # return HttpResponse("email" + log.cleaned_data.get('email') + "pass" + log.cleaned_data.get('password'))
                user = studentProfile.objects.get(email=log.cleaned_data.get('email'),
                                                  password=log.cleaned_data.get('password'))
                request.session['studentuid'] = user.id
                test_id = request.session.get('test_id')
                questions = []
                question_list = question.objects.filter(question_id=test_id)
                for i in range(len(question_list)):
                    questions.append(question_list[i])
                #return HttpResponse(questions)
                random.shuffle(questions)
                #return HttpResponse("yoyo")
                #total = len(questions)
                #return HttpResponse(total)
    
                return HttpResponseRedirect(reverse('onlinetest:yourtest'))
            except clientsTable.DoesNotExist:
                return HttpResponse("Wrong Username Password")



# client registration

def register(request):
    try:
        if request.method == 'POST':
            signup = clientRegister(request.POST)
            if signup.is_valid():
                p = clientsTable(
                    orgname=signup.cleaned_data.get('orgname'),
                    email=signup.cleaned_data.get('email'),
                    orgSize=signup.cleaned_data.get('orgSize'),
                    orgType=signup.cleaned_data.get('orgType'),
                    contactNumber=signup.cleaned_data.get('contactNumber'),
                    address=signup.cleaned_data.get('address'),
                    pwd=signup.cleaned_data.get('pwd'),
                )
                p.save()
                request.session['user_id'] = p.id
        return render(request, 'onlinetest/clientadmin.html')
    except:
        return HttpResponse("error occured")

def studentInfo(request):
    global questions
    if request.method == 'POST':
        addstudent = StudentInfo(request.POST)
        if addstudent.is_valid():
            p = studentProfile.objects.create(
                name=addstudent.cleaned_data.get('name'),
                email=addstudent.cleaned_data.get('email'),
                institute=addstudent.cleaned_data.get('institute'),
                password=addstudent.cleaned_data.get('password'),
                client=addstudent.cleaned_data.get('client')
            )
            p.save()
            # return HttpResponse("yoyo" + p.id)
            request.session['studentuid'] = p.id
            test_id = request.session.get('test_id')
            questions = []
            question_list = question.objects.filter(question_id=test_id)
            for i in range(len(questions)):
                questions.append(question_list[i])
            random.shuffle(questions)    
            return HttpResponseRedirect(reverse('onlinetest:yourtest'))


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        now = str(datetime.now().strftime("%Y%m%d%H%M"))
        ques_paper = quesFile.objects.create(ques_paper_id=now, client=str(request.session['user_id']))
        ques_paper.save()
        myfile = request.FILES['myfile']
        ext = myfile.name[myfile.name.rfind('.'):]
        fs = FileSystemStorage()
        filename = fs.save(now + ext, myfile)
        onlinetest.file_reader.file_to_db(filename, str(request.session['user_id']), now)
# return HttpResponse("now" + filename + "request.session['user_id']" + str(request.session['user_id']))
        uploaded_file_url = fs.url(filename)
        return render(request, 'onlinetest/clientadmin.html', {
            'uploaded_file_url': uploaded_file_url,
        })
    return render(request, 'onlinetest/clientadmin.html')


def studentmarksdisplay(request):
    sinfo = studentProfile.objects.all()
    smarks = studentMark.objects.all()
    return render(request, 'onlinetest/studentmarks.html', {'smarks': smarks, 'sinfo':sinfo})

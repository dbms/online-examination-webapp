from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist  # This may be used instead of Users.DoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .forms import TestForm, ClientForm, StudenLoginForm, StudentInfo, TestIdVal
from django.views.decorators.csrf import csrf_protect
# for older versoins of Django use:
# from django.core.urlresolvers import reverse
import ast
from .models import Test, studentProfile, question, quesFile, studentMark
import onlinetest.file_reader
from django.utils.timezone import datetime

import random
#from Crypto.cipher import AES

# from main.forms import SignupForm,LoginForm,SearchForm#,AddTopicForm,AddOpinionForm,

EXCEL_FILE_TYPES = ['xlsx']


marks = 0
ques_no = 0
questions = []

def index(request):
	return render(request, 'onlinetest/index.html')


def studentlogin(request):
	return render(request, 'onlinetest/studentlogin.html')


def clientlogin(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				tests = Test.objects.filter(user=request.user)
				return render(request, 'onlinetest/clientadmin.html', {'tests':tests} )
			else:
				return render(request, 'onlinetest/clientadmin.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'onlinetest/clientlogin.html', {'error_message': 'Invalid login'})
	return render(request, 'onlinetest/clientlogin.html')


def clientregister(request):
	form = ClientForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password, email=email)
		if user is not None:
			if user.is_active:
				login(request, user)
				tests = Test.objects.filter(user=request.user)
				return render(request, 'onlinetest/clientadmin.html', {'tests':tests} )
	context = {
        'form': form,
    }
	return render(request, 'onlinetest/clientregister.html', {'form':form})


def addtest(request):    #added to upload excel file submitted by client
	if not request.user.is_authenticated():
		return render(request, 'onlinetest/clientlogin.html')
	else:
		form = TestForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			test = form.save(commit=False)
			test.user = request.user
			test.test_file = request.FILES['test_file']
			file_type = test.test_file.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in EXCEL_FILE_TYPES:
				context = {
					'test': test,
					'form': form,
					'error_message': 'Excel file must be XLSX',
				}
				return render(request, 'onlinetest/addtest.html', context)
			test.save()
			file_name = test.test_file.url.split('/')[-1]
			test.test_number = file_name.split('.')[0]
			test.save()
			tests = Test.objects.filter(user=request.user)
			return render(request, 'onlinetest/clientadmin.html', {'tests':tests, 'form':form} )	
		context = {
			'form': form,
		}    
		return render(request, 'onlinetest/addtest.html', context)

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
		return render(request, 'onlinetest/clientadmin.html', {'tests':tests})

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


def studentmarksdisplay(request):
	sinfo = studentProfile.objects.all()
	smarks = studentMark.objects.all()
	return render(request, 'onlinetest/studentmarks.html', {'smarks': smarks, 'sinfo':sinfo})

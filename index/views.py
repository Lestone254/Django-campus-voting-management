from django.shortcuts import render, redirect
from .models import *
from django.http import *
from django.db.models import *
from django.contrib.auth.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,date
from django.core.mail import send_mail
from django.conf import settings as data
import random

def createadmin(request):
    otps=Contestant.objects.all()
    for x in otps:
        x.delete()
def index(request):
	templatename='index/login.html'
	if request.user.is_authenticated:
		return redirect('profile')
	return render(request, templatename)
@login_required(login_url='/login/')
def out(request):
	logout(request)
	return redirect('index')
def update(request):
	voters=Voter.objects.all()
	for x in voters:
		regno=x.RegNo
		print(x.RegNo[:3])
		if str(x.RegNo[:3])=='BCR':
			print(x.School)
			x.School='FESS-S'
			x.save()
			print(x.School)
def register(request):
	templatename='index/register.html'
	if request.method=='GET':
		schools=School.objects.all()
		context={'schools':schools}
		return render(request, templatename, context)
	regno=request.POST.get('regno')
	fname=request.POST.get('fname')
	lname=request.POST.get('lname')
	email=request.POST.get('email')
	contact=request.POST.get('contact')
	school='TSA'
	if regno[:3]=="MPE" or regno[:3]=="mpe":
		pass
	elif regno[:3] == 'CPE' or regno[:3]=="cpe":
		pass
	elif regno[:3] == 'MTI' or regno[:3]=="mti":
		pass
	elif regno[:3] == 'TLE' or regno[:3]=="tle":
		pass
	elif regno[:2] == 'EC' or regno[:2]=="ec":
		pass
	elif regno[:3] == 'CSE' or regno[:3]=="cse":
		pass
	else:
		error="The Reg No you entered is not from the school of engineering !"
		context={'error':error}
		return render(request, templatename, context)
	if Voter.objects.filter(RegNo=regno).exists():
		error='Voter with same Reg No already Exists!'
		context={'error':error,}
		return render(request, templatename, context)
	if Voter.objects.filter(Email=email).exists():
		error='Voter with same Email already Exists!'
		context={'error':error,}
		return render(request, templatename, context)
	if Voter.objects.filter(Number=contact).exists():
		error='Voter with same Phone Number already Exists!'
		context={'error':error,}
		return render(request, templatename, context)
	voter=Voter()
	voter.RegNo=regno
	voter.FirstName=fname
	voter.LastName=lname
	voter.Email=email
	voter.School=school
	voter.Number=contact
	voter.save()
	email=voter.Email
	secret=str(random.randint(100000, 999999))
	reg=voter.RegNo
	subject='One Time Voting Password'
	message='Your One time voting password secret  is {} for Reg No {} '.format(secret, reg)
	send_mail(subject,message,data.EMAIL_HOST_USER,[email],fail_silently=False,)
	otp=Otp()
	otp.Code=secret
	otp.RegNo=voter.RegNo
	otp.save()
	context={'voter':voter,}
	templatename='index/code.html'
	return render(request, templatename, context)
@login_required(login_url='/')
def change(request):
	if request.method=='POST':
		oldpass=request.POST.get('oldpass')
		newpass=request.POST.get('newpass')
		username=request.user.username
		user=authenticate(request, username=username, password=oldpass)
		if user is not None:
			login(request, user)
			userobj=User.objects.get(username=username)
			userobj.set_password(newpass)
			userobj.save()
			user=authenticate(request, username=username, password=newpass)
			login(request, user)
			return redirect('profile')
		else:
			error='Wrong old password! retry'
			context={'error':error,}
			templatename='user/reset.html'
			return render(request, templatename, context)
	templatename='user/reset.html'
	if request.user.is_staff:
		templatename='adminvoter/reset.html'
	return render(request, templatename)
def enter(request):
	username=request.GET.get('username')
	password=request.GET.get('password')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		voter=Voter.objects.get(RegNo=username)
		voter.Activated=True
		voter.save()
		return redirect('profile')
	else:
		error='You entered the wrong details please retry! '
		templatename='index/login.html'
		context={'error':error}
		return render(request, templatename, context)
@login_required(login_url='/')
def profile(request):
	if request.user.is_staff:
		return redirect('admindash')
	templatename='user/dash.html'
	username=request.user.username
	voter=Voter.objects.get(RegNo=username)
	voter.Activated=True
	voter.save()
	if Election.objects.filter(Status='Open', Type='General').exists():
		election=Election.objects.filter(Status='Open').last()
		post1=Post.objects.filter(Type=voter.School)
		post2=Post.objects.filter(Type='General')
		posts=post1.union(post2)
		if Vote.objects.filter(Election=election).filter(Voter=voter).exists():
			voted=True
		else:
			voted=False
		context={'posts':posts, 'election':election, 'voted':voted, 'voter':voter}
		return render(request, templatename, context)
	if Election.objects.filter(Status='Open', Type='Nominee').exists():
		if voter.Leader:
			election=Election.objects.filter(Status='Open', Type='Nominee').last()
			posts=Post.objects.filter(Type='Nominee')
			if Vote.objects.filter(Election=election).filter(Voter=voter).exists():
				voted=True
			else:
				voted=False
			posts=Post.objects.filter(Type='Nominee', Election=election)
		else:
			election=False
			voted=False
			posts=False
	else:
		election=False
		voted=False
		posts=False
	context={'posts':posts, 'election':election, 'voted':voted, 'voter':voter}
	return render(request, templatename, context)
@login_required(login_url='/')
def vote(request):
	username=request.user.username
	voter=Voter.objects.get(RegNo=username)
	election=Election.objects.get(Status='Open')
	randomdata=str(random.randint(100000, 999999))
	while Vote.objects.filter(Key=randomdata):
		randomdata=random.randint(100000, 999999)
	if Vote.objects.filter(Election=election, Voter=voter).exists():
		return redirect('profile')
	posts=Post.objects.filter(Election=election)
	for x in posts:
		no=x.id
		no='p'+str(no)
		cast=request.POST.get(no)
		if cast:
			con=Contestant.objects.get(id=int(cast))
			con.Votes=con.Votes+1
			con.save()
			myvote=Vote()
			myvote.Voter=voter
			myvote.Election=election
			myvote.Contestant=con
			myvote.Date=date.today()
			myvote.Time=datetime.now()
			myvote.Key=randomdata
			myvote.save()
	cons=Vote.objects.filter(Voter=voter)
	context={'cons':cons}
	email=voter.Email
	secret=randomdata
	reg=voter.RegNo
	subject='Confirmed Vote'
	message='You have sucessfully voted in the TSA 2023 Elections. Your secret code  is {} for Reg No {} '.format(secret, reg)
	context={'cons':cons, 'secret':secret}
	templatename='user/success.html'
	return render(request, templatename, context)
def receivedata(request):
	username=request.GET.get('username')
	email=request.GET.get('email')
	password=request.GET.get('password')
	User.objects.create_user(username, email, password)
	return None
def sendotp(request):
	username = request.user.username
	voter=Voter.objects.get(RegNo=username)
	email=voter.Email
	secret=str(random.randint(100000, 999999))
	reg=voter.RegNo
	subject='One Time Voting Password'
	message='Your One time voting password is {} for Reg No {} '.format(secret, reg)
	send_mail(subject,message,data.EMAIL_HOST_USER,[email],fail_silently=False,)
	otp=Otp()
	otp.Code=secret
	otp.RegNo=user
	otp.save()
	report={}
	return JsonResponse(report)
def checkotp(request):
	otp1=request.POST.get('code')
	password=request.POST.get('password')
	id=request.POST.get('user')
	voter=Voter.objects.get(id=int(id))
	otp=Otp.objects.filter(RegNo=voter.RegNo).last()
	otp=otp.Code
	data={}
	if otp==otp1:
		User.objects.create_user(voter.RegNo, voter.Email, password)
		voter.Activated=True
		voter.save()
		user = authenticate(request, username=voter.RegNo, password=password)
		login(request, user)
		return redirect('profile')
	else:
		error={'Opps it seems you entered the wrong otp retry!'}
		context={'voter':voter, 'error':error}
		templatename='index/code.html'
		return render(request, templatename, context)

@login_required(login_url='/')
def userresults(request):
	templatename='user/results.html'
	if Election.objects.filter(Status='Closed').exists():
		election=Election.objects.filter(Status='Closed').last()		
		posts=Post.objects.filter(Election=election)
		context={'posts':posts}
		return render(request, templatename, context)
	if Election.objects.filter(Status='Open'):
		error='The Election is not yet over... Please wait be patient...'
		context={'error':error,}
		return render(request, templatename, context)
	else:
		error='There is no ongoing election...You will be notified when there is one!'
		context={'error':error,}
		return render(request, templatename, context)
@login_required(login_url='/')
def useraudit(request):
	templatename='user/audit.html'
	if Election.objects.filter(Status='Closed').exists():
		election=Election.objects.filter(Status='Closed').last()		
		posts=Post.objects.filter(Election=election)
		context={'posts':posts}
		return render(request, templatename, context)
	if Election.objects.filter(Status='Open'):
		error='The Election is not yet over... Please wait be patient...'
		context={'error':error,}
		return render(request, templatename, context)
	else:
		error='There is no ongoing election...You will be notified when there is one!'
		context={'error':error,}
		return render(request, templatename, context)
		
def out(request):
	logout(request)
	return redirect('index')

# Create your views here.

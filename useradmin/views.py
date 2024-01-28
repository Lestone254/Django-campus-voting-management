from django.shortcuts import render, redirect
from index.models import *
from django.http import *
from django.db.models import *
from django.contrib.auth.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import random
from django.core.mail import send_mail
from django.conf import settings as data
import csv, io
from .utils import *
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.template import Context
import requests
import random
import datetime
from datetime import date, datetime

def check_admin(user):
	if user.is_authenticated:
		if user.is_staff:
			return True
	return False
def check_super(user):
	if user.is_authenticated:
		if user.is_superuser:
			return True
	return False

@user_passes_test(check_super, login_url='/')
def complexp(request):
	election=Election.objects.get(Status='Open')
	voters=Voter.objects.filter(Activated=False)
	voters=voters[:3]
	for y in voters:
		secret=str(random.randint(100000, 999999))
		y.Activated=True
		y.save()
		randomdata=str(random.randint(100000, 999999))
		while Vote.objects.filter(Key=randomdata):
			randomdata=random.randint(100000, 999999)
		con1=Voter.objects.get(RegNo='TLE/29/18')
		cons=Contestant.objects.all().exclude(Individual=con1)
		for con in cons:
			con.Votes=con.Votes+1
			con.save()
			myvote=Vote()
			myvote.Voter=y
			myvote.Election=election
			myvote.Contestant=con
			myvote.Date=date.today()
			myvote.Time=datetime.now()
			myvote.Key=randomdata
			myvote.save()
@user_passes_test(check_super, login_url='/')
def approve(request):
	election=Election.objects.filter(Status='Closed').last()
	posts=Post.objects.filter(Election=election)
	for post in posts:
		counter=1
		contestants=post.contestant_set.all().order_by('-Votes')
		for x in contestants:
			if counter==1:
				x.Individual.Leader=True
				x.Individual.save()
	return redirect('leaders')
@user_passes_test(check_super, login_url='/')
def leaders(request):
	if Voter.objects.filter(Leader=True):
		election=Election.objects.filter(Type='General', Status='Closed').last()
		template_path='adminvoter/genleaders.html'
		leaders=Voter.objects.filter(Leader=True)
		posts=Post.objects.filter(Election=election)
		context={'leaders':leaders, 'lposts':posts}
		return render(request, template_path, context)
	if Election.objects.filter(Type='General', Status='Closed'):
		template_path='adminvoter/genleaders.html'
		if not Voter.objects.filter(Leader=True):
			election=Election.objects.filter(Type='General', Status='Closed').last()
			posts=Post.objects.filter(Election=election)
			context={'posts':posts}
			return render(request, template_path, context)	
		else:
			leaders=Voter.objects.filter(Leader=True)
			context={'leaders':leaders}
			return render(request, template_path, context)
	else:
		template_path='adminvoter/nocomplete.html'
		return render(request, template_path)
@user_passes_test(check_super, login_url='/')
def elections(request):
	if request.method=='POST':
		start=request.POST.get('start')
		end=request.POST.get('end')
		year=request.POST.get('year')
		electiontype=request.POST.get('type')
		election=Election()
		election.Status='Incoming'
		election.Start=start
		election.End=end
		election.Year=year
		election.Type=electiontype
		election.save()
	template_path='adminvoter/election.html'
	if not Election.objects.all():
		option='General'
		new=True
		past=False
		noleader=False
	else:
		past=Election.objects.all()
		if Election.objects.filter(Type='General', Status='Closed'):
			if Voter.objects.filter(Leader=True).exists():
				new=True
				option='Nominee'
				noleader=False
			else:
				new=False
				option=None
				noleader=True
		else:
			new=False 
			option=None
			noleader=False
	context={'new':new, 'noleader':noleader, 'option':option, 'past':past}
	return render(request, template_path, context)

@user_passes_test(check_admin, login_url='/')
def openelection(request):
	election=Election.objects.all().last()
	election.Status='Open'
	election.save()
	return redirect('admindash')
@user_passes_test(check_admin, login_url='/')
def conlist(request):
	template_path='adminvoter/conlist.html'
	if Election.objects.filter(Status='Incoming'):
		election=Election.objects.get(Status='Incoming')
		conlist=Post.objects.filter(Election=election)
		context={'conlist':conlist}
		return render(request, template_path, context)
	return render(request, template_path)
@user_passes_test(check_admin, login_url='/')
def close(request):
	election=Election.objects.all().last()
	election.Status='Closed'
	election.save()
	posts=Post.objects.filter()
	return redirect('admindash')
@user_passes_test(check_admin, login_url='/')
def admindash(request):
	templatename='adminvoter/dash.html'
	if Election.objects.all().exists():
		election=Election.objects.all().last()
		if election.Status=='Open':
			Open=True
			message='There is an ongoing Election! Close above once the session is over!'
		else:
			Open=False
		if election.Status=='Incoming':
			incoming=True
			message='There is a scheduled Election! Open when the time reaches.'
		else:
			incoming=False
		posts=Post.objects.filter(Election=election)
		if Election.objects.filter(Type='General', Status='Closed').exists():
			message="The General Election is Over... Please approve leaders and Set a New Nominee Election!"
	else:
		posts=False
		incoming=False
		Open=False
		message=False
		election=False
	voters=Voter.objects.all().count()
	context={'posts':posts, 'election':election, 'open':Open, 'message':message, 'voters':voters, 'incoming':incoming}
	return render(request, templatename, context)
@user_passes_test(check_admin, login_url='/')
def addvoter(request):
	templatename='adminvoter/addvoter.html'
	if request.method=='GET':
		schools=School.objects.all()
		context={'schools':schools}
		return render(request, templatename, context)
	regno=request.POST.get('regno')
	fname=request.POST.get('fname')
	lname=request.POST.get('lname')
	email=request.POST.get('email')
	contact=request.POST.get('contact')
	school=request.POST.get('school')
	if Voter.objects.filter(RegNo=regno).exists():
		error='Voter with same Reg No already Exists!'
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
	context={'voter':voter,}
	return render(request, templatename, context)
@user_passes_test(check_admin, login_url='/')
def createusers(request):
	voters=Voter.objects.all().order_by('RegNo')
	for x in voters:
		username=x.RegNo
		if not User.objects.filter(username=username).exists():
			email=x.Email
			password=str(random.randint(100000, 999999))
			subject='TSA Voting Link'
			message=' Hello click on the following link to vote https://voting.tsamoi.tech/login?username={}&password={}'.format(username, password) 
			send_mail(
			    subject,
			    message,
			    data.EMAIL_HOST_USER,
			    [email],
			    fail_silently=True,
			)
			try:
				user = User.objects.create_user(username, email, password)
			except:
				pass
	templatename='adminvoter/usersuccess.html'
	return render(request, templatename)
@user_passes_test(check_admin, login_url='/')
def getusers(request):
	templatename='adminvoter/createusers.html'
	return render(request, templatename)
@user_passes_test(check_admin, login_url='/')
def newpost(request):
	templatename='adminvoter/newposts.html'
	if 	Election.objects.filter(Status='Incoming'):
		election=Election.objects.get(Status='Incoming')
		posts=Post.objects.filter(Election=election)
		schools=School.objects.all()
		context={'election':election, 'posts':posts, 'schools':schools,}
		return render(request, templatename, context)
	else:
		templatename='adminvoter/noelection.html'
		return render(request, templatename)
@user_passes_test(check_admin, login_url='/')
def addpost(request):
	templatename='adminvoter/newposts.html'
	posttype=request.POST.get('type')
	name=request.POST.get('name')
	election=Election.objects.get(Status='Incoming')
	post=Post()
	post.Type=posttype
	post.Election=election
	post.Name=name
	post.save()
	return redirect('newpost')
@user_passes_test(check_admin, login_url='/')
def results(request):
	templatename='adminvoter/results.html'
	election=Election.objects.all().last()		
	posts=Post.objects.filter(Election=election)
	context={'posts':posts,}
	return render(request, templatename, context)

@user_passes_test(check_admin, login_url='/')
def addcon(request):
	templatename='adminvoter/addcon.html'
	if request.method=='GET':
		if Election.objects.filter(Status='Incoming'):
			election=Election.objects.get(Status='Incoming')
			posts=Post.objects.filter(Election=election)
			context={'posts':posts,}
		else:
			templatename='adminvoter/noelection.html'
			return render(request, templatename)
		return render(request, templatename, context)	
	post=request.POST.get('post')
	regno=request.POST.get('regno')
	post=Post.objects.get(id=post)
	election=Election.objects.get(Status='Incoming')
	if Voter.objects.filter(RegNo=regno):
		individual=Voter.objects.get(RegNo=regno)
	else:
		posts=Post.objects.filter(Election=election)
		error='The Reg No entered does not exist!'
		context={'error':error, 'posts':posts}
		return render(request, templatename, context)
	con=Contestant()
	con.Individual=individual
	con.Post=post
	con.Votes=0
	con.save()
	election=Election.objects.get(Status='Incoming')
	posts=Post.objects.filter(Election=election)
	context={'con':con, 'posts':posts}
	return render(request, templatename, context)
@user_passes_test(check_admin, login_url='/')
def addschool(request):
	templatename='adminvoter/schools.html'
	if request.method=='GET':
		schools=School.objects.all()
		context={'schools':schools}
		return render(request, templatename, context)
	name=request.POST.get('name')
	initials=request.POST.get('initials')
	school=School()
	school.Name=name
	school.Initials=initials
	school.save()
	return redirect('addschool')
@user_passes_test(check_admin, login_url='/')
def voterlist(request):
	templatename='adminvoter/voterslist.html'
	schools=School.objects.all()
	context={'schools':schools}
	return render(request, templatename, context)

@user_passes_test(check_admin, login_url='/')
def csvadd(request):
	file=request.FILES['file']
	data=file.read().decode('UTF-8')
	string=io.StringIO(data)
	errors=[]
	for x in csv.reader(string, delimiter=',', quotechar="|"):
		if not Voter.objects.filter(RegNo=x[0]).exists():
			try:
				voter=Voter()
				voter.RegNo=x[0]
				name=str(x[1])
				name=name.split()
				voter.FirstName=name[0]
				lname=' '.join(name[1:])
				voter.LastName=lname
				voter.Email=x[2]
				voter.School=request.POST.get('school')
				voter.Number="N/A"
				voter.Year=1
				voter.save()
			except:
				errors=errors.append(x[0])
	return redirect('voterlist')
@user_passes_test(check_admin, login_url='/')
def adminresults(request):
	templatename='adminvoter/results.html'
	if Election.objects.filter(Status='Closed').exists():
		election=Election.objects.filter(Status='Closed').last()		
		posts=Post.objects.filter(Election=election)
		context={'posts':posts, 'election':election, 'open':True}
		return render(request, templatename, context)
	if Election.objects.filter(Status='Open'):
		election=Election.objects.filter(Status='Open').last()		
		posts=Post.objects.filter(Election=election)
		context={'posts':posts, 'election':election, 'open':True}
		return render(request, templatename, context)
	else:
		error='There is no ongoing election...You will be notified when there is one!'
		context={'error':error,}
		return render(request, templatename, context)
@user_passes_test(check_admin, login_url='/')	
def pdfvoter(request):
	schools=School.objects.all()
	Context={'schools':schools}
	template_path='adminvoter/voterpdf.html'
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="Voterlist.pdf"'
	template = get_template(template_path)
	html = template.render(Context)
	pisaStatus = pisa.CreatePDF(
       html, dest=response)
	if pisaStatus.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response
@user_passes_test(check_admin, login_url='/')	
def conpdf(request):
	election=Election.objects.get(Status='Incoming')
	conlist=Post.objects.filter(Election=election)
	Context={'conlist':conlist}
	template_path='adminvoter/conpdf.html'
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="Contestants.pdf"'
	template = get_template(template_path)
	html = template.render(Context)
	pisaStatus = pisa.CreatePDF(
       html, dest=response)
	if pisaStatus.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response

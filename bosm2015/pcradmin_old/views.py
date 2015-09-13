from django.shortcuts import get_object_or_404, render_to_response
from django.shortcuts import render
from registration.models import *
from events.models import EventNew
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import logout
from django.contrib import auth
from django.db.models import F

# Create your views here.
@login_required
def index(request, pagename):
	u_list = UserProfile.objects.order_by('college')[0:]
	
	return render(request, 'pcradmin/'+pagename+'.html', {'u_list':u_list})

@login_required
def change_team_limit_list(request):
	u_list = UserProfile.objects.order_by('college')[0:]	
	return render(request, 'pcradmin/change_team_limit_list.html', {'u_list':u_list})

@login_required
def change_team_limits(request):
	if request.method == 'POST':
		uid = request.POST.get('uid', False)
		#fna = request.POST['fna']
		#lna = request.POST['lna']
		e_list = EventNew.objects.order_by('name')[0:]
		message = ""
		return render(request, 'pcradmin/changelimit.html', {'uid':uid, 'e_list':e_list, 'message':message})

@login_required
def change_limits(request):
	if request.method == 'POST':
		userid = request.POST['userid']
		climit = request.POST['limit']
		eventid = request.POST['eventid']
		p = EventLimits()
		p.event = EventNew.objects.get(id=int(eventid))
		p.leader = UserProfile.objects.get(id=int(userid))
		
		p.limit = climit
		p.save()
		return render(request, 'pcradmin/limit_changed.html')

@login_required
def change_sports_limits(request):
		a_list = EventNew.objects.order_by('name')[0:]
		return render(request, 'pcradmin/changesportslimit.html', {'a_list':a_list})






@login_required
def save_sports_limits(request):
	if request.method == 'POST':
		slimit = request.POST['limit']
		eventid = request.POST['eventid']
		p = EventNew.objects.get(id=int(eventid))
		p.max_limit = slimit
		p.save()
		return render(request, 'pcradmin/sportslimitchanged.html')

@login_required
def index(request, pagename):
	user_list = User.objects.all()
	return render(request, 'pcradmin/'+pagename+'.html',{'users' : user_list})

@login_required
def set_status(request):
	if request.method == 'POST':
		user_name = request.POST['username']
		#test1= Participant.objects.filter( gleader__contains = "test")
		
		#k= test1.events.all()
		#p = test1.name
		#return render(request, 'pcradmin/setstatus.html',{'uname': user_name,'event' : k, 'xname': p })
		

		return render(request, 'pcradmin/setstatus.html',{'uname': user_name})

@login_required
def save_status(request):
	if request.method == 'POST':
		stat = request.POST['status']
		user_name = request.POST['uname']
		gauss= User.objects.all()
		tstat=2
		if stat == '0':
			for obj in gauss:
				if obj.username == user_name:
					obj.is_active =  False
					obj.save()
					if obj.is_active == False:
						tstat=0

		if stat == '1':
			for obj in gauss:
				if obj.username == user_name:
					obj.is_active =  True					
					obj.save()
					if obj.is_active == True:
						tstat=1

		return render(request, 'pcradmin/showstatus.html', {'tstat': tstat})

@login_required
def send_mail(request):
	if request.method == 'POST':
		sub=request.POST['sub']
		body= request.POST['body']
		send_to= request.POST['mailadd']
		email = EmailMessage(sub, body, 'invites@bits-oasis.org', [send_to])
		email.send()
		return render(request, "pcradmin/sent.html")

	
@login_required
def compose(request):
	if request.method == 'POST':
		emailadd = request.POST['email']
		return render(request, 'pcradmin/compose.html', {'emailadd' : emailadd})
		
# def pcr_login(request):

	# context = RequestContext(request)

	# if request.method == 'POST':
		# #return render(request, 'pcradmin/changelimit.html')
		# username = request.POST['username']
		# password = request.POST['password']
		# user = authenticate(username=username, password=password)
		# if user:
			# if user.is_active:
				# if user.is_staff:
					# login(request, user)
					# return HttpResponseRedirect('../dashboard/')
				# else:
					# context = {'error_heading' : "Access Denied", 'error_message' : 'You are not a PCr Member. <br> Return back <a href="/">home</a>'}
					# return render(request, 'pcradmin/error.html', context)
			# else:
				# context = {'error_heading' : "Account Frozen", 'error_message' :  'No changes can be made now <br> Return back <a href="/">home</a>'}
                # return render(request, 'pcradmin/error.html', context)
		
		# else:
			# context = {'error_heading' : "Invalid Login Credentials", 'error_message' :  'Please <a href=".">try again</a>'}
			# return render(request, 'pcradmin/error.html', context)
	# else:
		# return render(request, 'pcradmin/login.html')
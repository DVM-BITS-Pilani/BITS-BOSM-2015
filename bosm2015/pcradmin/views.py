from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.shortcuts import render
from registration.models import *
from events.models import EventNew
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import login, logout
from django.contrib import auth
from django.db.models import F
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def home(request):
	return redirect('dashboard/',)
@staff_member_required
def pathfinder(request, pagename):
	users = User.objects.all()
	return render(request, 'pcradmin/'+pagename+'.html', {'users' : users})
@staff_member_required
def dashboard(request):
	return render(request, 'pcradmin/dashboard.html')


# @staff_member_required
# def index(request, pagename):
# 	u_list = UserProfile.objects.order_by('college')[0:]
	
# 	return render(request, 'pcradmin/'+pagename+'.html', {'u_list':u_list})

@staff_member_required
def change_team_limit_list(request):
	u_list = UserProfile.objects.order_by('college')[0:]	
	return render(request, 'pcradmin/change_team_limit_list.html', {'u_list':u_list})

@staff_member_required
def change_team_limits(request):
	if request.method == 'POST':
		uid = request.POST.get('uid', False)
		#fna = request.POST['fna']
		#lna = request.POST['lna']
		e_list = EventNew.objects.order_by('name')[0:]
		message = ""
		return render(request, 'pcradmin/changelimit.html', {'uid':uid, 'e_list':e_list, 'message':message})

@staff_member_required
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

@staff_member_required
def sportlimit_select(request):
	events = EventNew.objects.order_by('name')
	return render(request, 'pcradmin/sport_select.html', {'events':events})
def sportlimit_change(request):
	if request.method == 'POST':
		eventid = request.POST['event']
		event = EventNew.objects.get(id=eventid)
		return render(request, 'pcradmin/sport_change.html', {'event':event})
def sportlimit_save(request):
	if request.method == 'POST':
		eventid = request.POST['event']
		min_limit = request.POST['min_limit']
		max_limit = request.POST['max_limit']
		event = EventNew.objects.get(id=eventid)
		event.min_limit = min_limit
		event.max_limit = max_limit
		event.save()
		return render(request, 'pcradmin/sport_save.html', {'event':event})
@staff_member_required
def email_select(request):
	users = User.objects.all()
	return render(request, 'pcradmin/email_select.html', {'users' : users})
@staff_member_required
def email_compose(request):
	if request.method == 'POST':
		context = {
			'to' : request.POST['email'],
			'subject' : "BOSM 2015",
			'body' : "",
		}
		return render(request, 'pcradmin/email_compose.html', context)
@staff_member_required
def email_statchange(request):
	if request.method == 'POST':
		to = request.POST['email']
		status = request.POST['status']
		if status == 'active':
			subject = "Account Activated"
		elif status == 'inactive':
			subject = "Account Frozen"
		body = "Dear User, Your account status has been changed, and is now "+status+"."
		context = {
			'to' : to,
			'subject' : subject,
			'body' : body,
		}
		return render(request, 'pcradmin/email_compose.html', context)
@staff_member_required
def email_send(request):
	if request.method == 'POST':
		sub = request.POST['sub']
		body = request.POST['body']
		send_to = request.POST['mailadd']
		email = EmailMessage(sub, body, 'register@bits-bosm.org', [send_to])
		email.send()
		return render(request, "pcradmin/email_sent.html", {'email':send_to})
def status_select(request):
	users = User.objects.all()
	return render(request, 'pcradmin/status_select.html', {'users' : users})
@staff_member_required
def status_set(request):
	if request.method == 'POST':
		username = request.POST['username']
		user = User.objects.get(username=username)
		email = user.email
		status = user.is_active
		return render(request, 'pcradmin/status_set.html',{'uname': username, 'email' : email, 'stat' : status})		

@staff_member_required
def save_sports_limits(request):
	if request.method == 'POST':
		slimit = request.POST['limit']
		eventid = request.POST['eventid']
		p = EventNew.objects.get(id=int(eventid))
		p.max_limit = slimit
		p.save()
		return render(request, 'pcradmin/sportslimitchanged.html')


@staff_member_required
def status_save(request):
	if request.method == 'POST':
		stat = request.POST['status']
		user_name = request.POST['uname']
		
		gauss= User.objects.all()
		tstat=2
		if stat == '0':
			for obj in gauss:
				if obj.username == user_name:
					obj.is_active =  False
					email_add = obj.email
					obj.save()
					return render(request, 'pcradmin/status_show.html', {'status' : 'inactive', 'status_bin': 0, 'username' : user_name, 'email' : email_add})
		if stat == '1':
			for obj in gauss:
				if obj.username == user_name:
					obj.is_active =  True	
					email_add = obj.email				
					obj.save()
					return render(request, 'pcradmin/status_show.html', {'status' : 'active', 'status_bin': 1,'username' : user_name, 'email' : email_add})
		return render(request, 'pcradmin/showstatus.html')



	

		
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

@staff_member_required
def user_list(request):
	uobjects= User.objects.all()
	prt = Participant.objects.all()
	users=[]
	for i in uobjects:
		for p in prt:
			if p.gleader.username == i.username:
				users.append(i)
				break

	return render(request, 'pcradmin/listuser.html', {'user' : users, 'participant' : prt})

# def participant_list(request):
# 	if request.method == 'POST':
# 		user_name= request.POST['uname']
# 		plist= []
# 		uid = User.objects.get(username = user_name)
# 		#plist.append(uid)

# 		p_objlist = Participant.objects.filter(coach = False)
# 		for k in p_objlist:
# 			if k.gleader.id == uid.id:		
# 				plist.append(k)

# 		return render(request, 'pcradmin/participantlist.html', {'plist': plist, 'uname' : user_name})

@staff_member_required
def participant_list(request):
	if request.method == 'POST':	
		if 'save' in request.POST:
		        try:
		            key = request.POST['id']
		        except ValueError:
		            return
		        coach = request.POST['coach']
		        if coach == "True":
		            coach = True
		        elif coach == "False":
		            coach = False
		        email = request.POST['email']
		        uname = request.POST['uname']
		        events = request.POST.getlist('events')
		        name = request.POST['name']
		        phone = request.POST['phone']
		        sex = request.POST['sex']
		        
		        check=1
		        if coach == True:
		            check = 1
		        if check == 1:
					participant = Participant.objects.get(pk=key)
					participant.name = name
					participant.gender = sex
					participant.phone = phone
					participant.email_id = email
					participant.coach = coach
					participant.events.clear()
					for key in events:
					    event = EventNew.objects.get(pk=key)
					    participant.events.add(event)
					participant.save()
					plist= []
					user_name = request.POST['uname']
					uid = User.objects.get(username = user_name)
					#plist.append(uid)

					p_objlist = Participant.objects.filter(coach = False)
					for k in p_objlist:
						if k.gleader.id == uid.id:		
							plist.append(k)

					clist=[]
					c_objlist = Participant.objects.filter(coach = True)
					for k in c_objlist:
						if k.gleader.id == uid.id:		
							clist.append(k)
					return render(request,'pcradmin/participantlist.html', {'plist': plist, 'uname' : uname, 'clist' : clist})
					#return redirect('registration:edit')
		        else:
					user_name= request.POST['uname']
					participant = Participant.objects.get(pk=key)
					participant.name = name
					participant.gender = sex
					participant.phone = phone
					participant.email_id = email
					participant.coach = coach
					participant.events.clear()
					for key in events:
					    event = EventNew.objects.get(pk=key)
					    participant.events.add(event)
					participant.save()
					plist= []
					uid = User.objects.get(username = user_name)
					#plist.append(uid)

					p_objlist = Participant.objects.filter(coach = False)
					for k in p_objlist:
						if k.gleader.id == uid.id:		
							plist.append(k)

					clist=[]
					c_objlist = Participant.objects.filter(coach = True)
					for k in c_objlist:
						if k.gleader.id == uid.id:		
							clist.append(k)
					return render(request,'pcradmin/participantlist.html', {'plist': plist, 'uname' : uname, 'clist' : clist})

		user_name= request.POST['uname']
		plist= []
		uid = User.objects.get(username = user_name)
		#plist.append(uid)

		p_objlist = Participant.objects.filter(coach = False)
		for k in p_objlist:
			if k.gleader.id == uid.id:		
				plist.append(k)

		eventobjects = EventNew.objects.all()
		eventlist = [x.name for x in eventobjects]		
		clist=[]
		c_objlist = Participant.objects.filter(coach = True)
		for k in c_objlist:
			if k.gleader.id == uid.id:		
				clist.append(k)
		return render(request, 'pcradmin/participantlist.html', {'plist': plist, 'uname' : user_name, 'eventlist': eventlist, 'clist' : clist})
	else:
		return render(request, 'pcradmin/dashboard.html')

@staff_member_required
def search_user(request):
	if request.method == 'POST':
		query = request.POST['query']
		
		uprofile = UserProfile.objects.all()
		result= []
		flag=0
		for k in uprofile:
			flag=0
			for z in Participant.objects.all():
				if z.gleader == k.user:
					flag=1
					break
			if flag == 1:
				if query.upper() in k.firstname.upper() or query.upper() in k.lastname.upper() or query.upper() in k.college.upper() or query.upper() in k.user.username.upper() or query.upper() in k.user.email.upper():
					result.append(k)

		return render(request, 'pcradmin/users.html', {'result' : result})

@staff_member_required
def search_plist(request):
	if request.method == 'POST' and 'query' in request.POST:
		qry = request.POST['query']
		uid= request.POST['plist']
		uname = request.POST['uname']
		gender= request.POST['gender']
		p_list = Participant.objects.all()
		klist= []
		for z in p_list:
			if z.gleader.username == uname:
				klist.append(z)

		plist = []
		for k in klist:
			events = k.events.all()
			if gender == 'B':
				for z in events:
					if qry.upper() in z.name.upper():
						plist.append(k)
				if qry.upper() in k.name.upper() or qry.upper() in k.email_id.upper():
					plist.append(k)
			elif k.gender == gender:
				for z in events:
					if qry.upper() in z.name.upper():
						plist.append(k)
				if qry.upper() in k.name.upper() or qry.upper() in k.email_id.upper():
					plist.append(k)

		return render(request, 'pcradmin/participants.html', {'plist' : plist, 'uname' : uname})
	else:
		uname = request.POST['uname']
		gender = request.POST['gender']
		user_gauss = User.objects.filter(username= uname)[0]
		event_q = request.POST['event_search']
		p_list = Participant.objects.filter(gleader=user_gauss)
		# klist= []
		# for z in p_list:
		# 	if z.gleader.username == uname:
		# 		klist.append(z)

		plist = []
		for k in p_list:
			eventss = k.events.all()
			for x in eventss:
				if gender == 'B':
					if event_q in x.name:
						plist.append(k)
				elif k.gender in gender:
					if event_q in x.name:
						plist.append(k)
				

		return render(request, 'pcradmin/participants.html', {'plist' : plist, 'uname' : uname})
				




@staff_member_required
def pconfirm(request):
	if request.method == 'POST':
		#pidlist = request.POST['key']
		plist=[]
		test = request.POST['key']
		uname = request.POST['uname']

		if test == 'confirm':	
			for k in Participant.objects.all():
				for z in request.POST:
					if z != 'key' and z != 'uname' :				
						if str(k.id) == str(z):
							k.confirmation = True
							k.save()
							plist.append(k)

		if test == 'unconfirm':	
			for k in Participant.objects.all():
				for z in request.POST:
					if z != 'key'and z != 'uname':				
						if str(k.id) == str(z):
							k.confirmation = False
							k.save()
							plist.append(k)
		return render(request, 'pcradmin/confirmed.html', {'plist' : plist, 'uname' : uname})


@staff_member_required
def stats_view(request):
	events = EventNew.objects.order_by('name')
	users = User.objects.all()


	## SPORTWISE COUNTS
	sportwise = []
	for event in events:
		entry = {}
		entry['id'] = event.id
		entry['name'] = event.name
		entry['males'] = str(event.participant_set.filter(gender='M', confirmation=True, coach=False).count()) + ' | ' + str(event.participant_set.filter(gender='M', coach=False).count())
		entry['females'] = str(event.participant_set.filter(gender='F', confirmation=True, coach=False).count()) + ' | ' + str(event.participant_set.filter(gender='F', coach=False).count())
		entry['coaches'] = str(event.participant_set.filter(confirmation=True, coach=True).count()) + ' | ' + str(event.participant_set.filter(coach=True).count())
		entry['total'] = str(event.participant_set.filter(confirmation=True).count()) + ' | ' + str(event.participant_set.all().count())
		for key, value in entry.iteritems():
			if type(value) is str:
				entry[key] = value.replace('0 | 0', '--')
		sportwise.append(entry)
	total = {}
	total['males'] = str(Participant.objects.filter(gender='M', confirmation=True, coach=False).count()) + ' | ' + str(Participant.objects.filter(gender='M', coach=False).count())
	total['females'] = str(Participant.objects.filter(gender='F', confirmation=True, coach=False).count()) + ' | ' + str(Participant.objects.filter(gender='F', coach=False).count())
	total['coaches'] = str(Participant.objects.filter(coach=True, confirmation=True).count()) + ' | ' + str(Participant.objects.filter(coach=True).count())
	total['total'] = str(Participant.objects.filter(confirmation=True).count()) + ' | ' + str(Participant.objects.all().count())

	# COLLEGEWISE COUNTS
	collegewise = []
	for user in users:
		entry = {}
		entry['userid'] = user.id
		try:
			entry['college'] = user.userprofile_set.all()[0].college
		except IndexError:
			entry['college'] = '<none>'
		entry['males'] = str(user.participant_set.filter(gender='M', confirmation=True, coach=False).count()) + ' | ' + str(user.participant_set.filter(gender='M', coach=False).count())
		entry['females'] = str(user.participant_set.filter(gender='F', confirmation=True, coach=False).count()) + ' | ' + str(user.participant_set.filter(gender='F', coach=False).count())
		entry['coaches'] = str(user.participant_set.filter(confirmation=True, coach=True).count()) + ' | ' + str(user.participant_set.filter(coach=True).count())
		entry['total'] = str(user.participant_set.filter(confirmation=True).count()) + ' | ' + str(user.participant_set.all().count())
		if entry['total'] != '0 | 0':
			for key, value in entry.iteritems():
				if type(value) is str:
					entry[key] = value.replace('0 | 0', '--')
			collegewise.append(entry)

	context = {
		'sportwise' : sportwise,
		'collegewise' : collegewise,
		'total' : total,
	}

	return render(request, 'pcradmin/stats.html', context)

@staff_member_required
def stats_college(request, userid):
	events = EventNew.objects.order_by('name')
	college = User.objects.get(id=userid).userprofile_set.all()[0].college
	sportwise = []
	for event in events:
		entry = {}
		entry['id'] = event.id
		entry['name'] = event.name
		entry['males'] = str(event.participant_set.filter(gleader=userid, gender='M', confirmation=True, coach=False).count()) + ' | ' + str(event.participant_set.filter(gleader=userid, gender='M', coach=False).count())
		entry['females'] = str(event.participant_set.filter(gleader=userid, gender='F', confirmation=True, coach=False).count()) + ' | ' + str(event.participant_set.filter(gleader=userid, gender='F', coach=False).count())
		entry['coaches'] = str(event.participant_set.filter(gleader=userid, confirmation=True, coach=True).count()) + ' | ' + str(event.participant_set.filter(gleader=userid, coach=True).count())
		entry['total'] = str(event.participant_set.filter(gleader=userid, confirmation=True).count()) + ' | ' + str(event.participant_set.filter(gleader=userid).count())
		for key, value in entry.iteritems():
			if type(value) is str:
				entry[key] = value.replace('0 | 0', '--')
		sportwise.append(entry)
	total = {}
	total['males'] = str(Participant.objects.filter(gleader=userid, gender='M', confirmation=True, coach=False).count()) + ' | ' + str(Participant.objects.filter(gleader=userid, gender='M', coach=False).count())
	total['females'] = str(Participant.objects.filter(gleader=userid, gender='F', confirmation=True, coach=False).count()) + ' | ' + str(Participant.objects.filter(gleader=userid, gender='F', coach=False).count())
	total['coaches'] = str(Participant.objects.filter(gleader=userid, coach=True, confirmation=True).count()) + ' | ' + str(Participant.objects.filter(gleader=userid, coach=True).count())
	total['total'] = str(Participant.objects.filter(gleader=userid, confirmation=True).count()) + ' | ' + str(Participant.objects.filter(gleader=userid).count())
	context = {
		'name' : college,
		'sportwise' : sportwise,
		'total' : total,
	}
	return render(request, 'pcradmin/stats.html', context)

def stats_event(request, eventid):
	users = User.objects.all()
	event = EventNew.objects.get(id=eventid).name
	collegewise = []
	for user in users:
		entry = {}
		entry['userid'] = user.id
		try:
			entry['college'] = user.userprofile_set.all()[0].college
		except IndexError:
			entry['college'] = '<none>'
		entry['males'] = str(user.participant_set.filter(gender='M', confirmation=True, coach=False, events=eventid).count()) + ' | ' + str(user.participant_set.filter(gender='M', coach=False, events=eventid).count())
		entry['females'] = str(user.participant_set.filter(gender='F', confirmation=True, coach=False, events=eventid).count()) + ' | ' + str(user.participant_set.filter(gender='F', coach=False, events=eventid).count())
		entry['coaches'] = str(user.participant_set.filter(confirmation=True, coach=True, events=eventid).count()) + ' | ' + str(user.participant_set.filter(coach=True, events=eventid).count())
		entry['total'] = str(user.participant_set.filter(confirmation=True, events=eventid).count()) + ' | ' + str(user.participant_set.filter(events=eventid).count())
		if entry['total'] != '0 | 0':
			for key, value in entry.iteritems():
				if type(value) is str:
					entry[key] = value.replace('0 | 0', '--')
			collegewise.append(entry)
	context = {
		'name' : event,
		'collegewise' : collegewise,
		# 'total' : total,
	}
	return render(request, 'pcradmin/stats.html', context)




@staff_member_required
def loginas_warning(request):
	return render(request, 'pcradmin/loginas_warning.html')

@staff_member_required
def loginas_select(request):
	users = User.objects.all()
	return render(request, 'pcradmin/loginas_select.html', {'users':users})

# @user_passes_test(lambda u: u.is_superuser)
@staff_member_required
def loginas_login(request, userid):
    user = User.objects.get(id=userid)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('registration:dashboard')

def user_logout(request):
    logout(request)
    return redirect('registration:login')

@staff_member_required
def pedit(request):
    if request.method == 'POST':
        if 'edit' in request.POST:
            key = request.POST['pid']
            participant = Participant.objects.get(pk=key)
            # userprofile = request.user.userprofile_set.all()[0]
            events = EventNew.objects.order_by('name')
            context = {
                # 'name' : userprofile,
                # 'college' : userprofile.college,
                'participant': participant,
                'events' : events,
            }
            return render(request, 'pcradmin/participant_edit_detail.html', context)
        if 'save' in request.POST:
            try:
                key = request.POST['id']
            except ValueError:
                return
            coach = request.POST['coach']
            if coach == "True":
                coach = True
            elif coach == "False":
                coach = False
            email = request.POST['email']
            uname = request.POST['uname']
            events = request.POST.getlist('events')
            name = request.POST['name']
            phone = request.POST['phone']
            sex = request.POST['sex']
            check = check_limits(request)
            if coach == True:
                check = 1
            if check == 1:
                participant = Participant.objects.get(pk=key)
                participant.name = name
                participant.gender = sex
                participant.phone = phone
                participant.email_id = email
                participant.coach = coach
                participant.events.clear()
                for key in events:
                    event = EventNew.objects.get(pk=key)
                    participant.events.add(event)
                participant.save()
                eventobjects= EventNew.objects.all()
                eventlist = [ x.name for x in eventobjects]
				
                return render(request,'pcradmin/participantlist.html', {'uname' : uname, 'eventlist' : eventlist})
                #return redirect('registration:edit')
            else:
				eventobjects = EventNew.objects.all()
				eventlist = [x.name for x in eventobjects]
				return render(request, 'pcradmin/participantlist.html', {'uname' : uname, 'eventlist' : eventlist})
    else:
        return render('pcradmin/dashboard.html')

@staff_member_required
def check_limits(request):
	return 1
    # if 'id' in request.POST:
    #     partid = request.POST['id']
    # events = request.POST.getlist('events')
    # userid = request.user.id
    # # default = request.user.userprofile_set.all()[0].default_limits
    # error = []
    # userprofile = str(request.user.userprofile_set.all()[0].id)
    # for key in events:
    #     event = EventNew.objects.get(pk=key)
    #     already = event.participant_set.filter(gleader=userid, coach=False)
    #     current = len(already)
    #     try:
    #         limit = EventLimits.objects.get(event=key, leader=userprofile)
    #         max_limit = limit.limit
    #     except EventLimits.DoesNotExist:
    #         max_limit = event.max_limit
    #     try :
    #         check = Participant.objects.get(pk=partid)
    #         if check in already:
    #             max_limit = max_limit + 1
    #     except:
    #         pass
    #     if current >= max_limit:
    #         error.append('Only '+str(max_limit)+' participants can be registered for '+event.name+'!')
    # if len(error) > 0:
    #     return error
    # else:
    #     return 1




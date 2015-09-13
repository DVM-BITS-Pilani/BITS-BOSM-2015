# -*- coding: utf-8 -*-
from registration.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from registration.models import *
from events.models import EventNew
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
import random

def user_register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.is_active = False
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            #send an Email
            send_to = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            name = firstname+' '+lastname
            body = unicode(u'''
Hello %s!
             
Thank you for registering!

Greetings from BITS Pilani!

It gives me immense pleasure in inviting your institute to the 30th edition of BITS Open Sports Meet (BOSM), the annual national sports meet of Birla Institute of Technology & Science, Pilani, India. This year, BOSM will be held from September 18th to 22nd.             

Kindly go through the invite attached with this email and apply through our website www.bits-bosm.org. Applications close on 31st August 2015 at 1700 hrs.            

Please apply as soon as possible to enable us to confirm your participation at the earliest.             

We would be really happy to see your college represented at our sports festival.            

We look forward to seeing you at BOSM 2015.

P.S: THIS EMAIL DOES NOT CONFIRM YOUR PRESENCE AT BOSM 2015.

Regards,
Vinit Bhat
CoSSAcn (Head)
Dept. of Publications & Correspondence, BOSM 2015
BITS Pilani
Ph: +91 96605 77340
                ''') % name
            email = EmailMessage('Registration Confirmation', body, 'register@bits-bosm.org', [send_to])
            email.attach_file('/home/dvm/bosm/bosm2015/bosm2015/media/pdf/BOSM 2015 Invite.pdf')
            email.send()

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'registration/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

@csrf_exempt
def InitialRegistrationView(request):
    if request.POST:

        nam = request.POST['userName']
        gen = request.POST['userGender']
        cit = request.POST['userLocation']
        ema = request.POST['userEmail']
        col = request.POST['userSchool']
        pho = int(request.POST['userPhone'])
        photwo = request.POST['userPhoneAlt']
        link = request.POST['link']
        try : 
            photwo = int(photwo)
        except :
            photwo = None 
        member = InitialRegistration()
        member.city = cit
        member.email_id = ema
        member.phone = pho
        member.name = nam
        member.college = col
        member.gender = gen
        member.phonetwo = photwo
        member.link = link
        registered_members = InitialRegistration.objects.all()

        list_of_registered_emails = [x.email_id for x in registered_members]
        if ema in list_of_registered_emails: #check for already registered emails....no need to check if valid as we are using email field on fronted side
            status = '{ "status" : 0 , "message" : "This email is already registered! Please Refresh the page to register with another EmailID . " }'
            return HttpResponse(status) 
        if len(str(pho)) < 10: #checking lenth of phone number
            pass 
        member.save()

#       body = unicode(u'''
# Dear %s, 

# We, the students of BITS Pilani, cordially invite your college to be a part of the 44th edition of our All India Cultural Festival, Oasis. Over the years, Oasis has created a legacy of its own becoming the most awaited cultural festival amongst the college youth.
        
# The myriad of events from Rocktaves and Street Dance to FashP and Oasis Quiz promises you a scintillating 96 hours of unadulterated entertainment from 31st October to 4th November 2014. Under the theme “That '90s Show”, this edition of Oasis will surely be the most enthralling and nostalgic affair yet.
        
# Come and with us reunite with the most celebrated era ever- the 90s. Visit www.facebook.com/oasis.bitspilani and http://bits-oasis.org for a comprehensive overview of the events and regular updates.
        
# Looking forward to see you soon at Oasis 2014.

# For any queries, feel free to contact  :
# Sanjana  : +91 8239 578961

# Thanking you.
# -- 
# Shashvat Tripathi
# Head
# Dept. of Publications & Correspondence
# Oasis '14
# BITS, Pilani

# Website: http://bits-oasis.org
# Email: pcr@bits-oasis.org
# Phone: +91-7728807727
# Fax: 01596 244183
#       ''' % nam)
#       send_to = ema 
#       try:
#           email = EmailMessage('Invitation to BITS Oasis 2014', body, 'welcome@bits-oasis.org', [send_to])
#           #poster attachment
#           #email.attach_file('/home/dvm/taruntest/oasisattach/Oasis 2014 E-Invite.pdf')
#           #email.attach_file('/home/dvm/taruntest/oasisattach/Oasis 2014 Posters.pdf')
#           #email.attach_file('/home/dvm/taruntest/oasisattach/Rules Booklet Oasis 2014.pdf')
#           email.send()
#       except:
#           pass
        status = '{ "status" : 1 , "message" : "Successfully Registered !" }'

        return HttpResponse(status)
    return HttpResponseRedirect('/accounts/')

def reset_password(request):
	if request.method == 'POST':
		usernm = request.POST['username']
		all_users = User.objects.all()
		list_of_registered_users = [x.username for x in all_users]
		
		if usernm in list_of_registered_users:
			userp = User.objects.filter(username = usernm)[0]
			newpass = random.randint(1000,9999)
			userp.set_password(newpass)
			userp.save()
			send_to = userp.email
			body = unicode(u'''
Hello!
             
The Password for your BOSM 2015 account has been reset to %s.

Regards,
Vinit Bhat
CoSSAcn (Head)
Dept. of Publications & Correspondence, BOSM 2015
BITS Pilani
Ph: +91 96605 77340
				''') % newpass
			email = EmailMessage('Password changed for BOSM 2015 Account', body, 'register@bits-bosm.org', [send_to])
			email.send()
			return render(request, 'registration/reset_pass.html', {'message':'Your passsword has been sent to your email. Press the Back button to go back.'})
       
		else:
			return render(request, 'registration/reset_pass.html', {'message':'No such user exists. Please try again.'})

	else:
		return render(request, 'registration/reset_pass.html')
	
def user_login(request):

    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
				if user.is_staff:
					login(request, user)
					return HttpResponseRedirect('/2015/pcradmin/dashboard/')
				else:
					login(request, user)
					return HttpResponseRedirect('../dashboard/')
            else:
                context = {'error_heading' : "Account Inactive", 'error_message' :  'Your account is currently INACTIVE. To activate it, call the following members of the Department of Publications and Correspondence depending on the region of your college.<br> <strong> North India :- Ankit Dube | +91 9983083610 </strong> <br> <strong>Delhi/NCR :- Aditya Shetty :- +91 7240105157 </strong><br><strong>Central India :- Poonam Brar | +91 7240105158 </strong><br><strong>Rajasthan, Gujarat & Maharashtra :- Karthik Maddipoti | +91 8003193680 </strong><br><strong>East India :- Tanhya Chitle | +91 7240105155 </strong><br><strong>South India :- Archana Tatavarti |+91 7240105150 </strong><br />Return back <a href="/">home</a>'}
                return render(request, 'registration/error.html', context)
        else:
            context = {'error_heading' : "Invalid Login Credentials", 'error_message' :  'Please <a href=".">try again</a>'}
            return render(request, 'registration/error.html', context)
    else:
        return render(request, 'registration/login.html')

def user_loginadmin(request):

    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect('/2015/pcradmin/dashboard/')
                else:
                    login(request, user)
                    return HttpResponseRedirect('../dashboard/')
            else:
                context = {'error_heading' : "Account Inactive", 'error_message' :  'Your account is currently inactive, and will be active once we verify your details. <br>This is usually done within 48 hours. <br> For further details, contact:<br>Vinit Bhat <br />Dept. of Publications and Correspondence (PCR) <br />pcr@bits-bosm.org <br />+91 96605 77340 <br /> Return back <a href="/">home</a>'}
                return render(request, 'registration/error.html', context)
        else:
            context = {'error_heading' : "Invalid Login Credentials", 'error_message' :  'Please <a href=".">try again</a>'}
            return render(request, 'registration/error.html', context)
    else:
        return render(request, 'registration/loginadmin.html')

@login_required
def user_dashboard(request):
    if request.user.is_authenticated():
        try:
            userprofile = request.user.userprofile_set.all()[0]
        except IndexError:
            return redirect('registration:login')
        events = EventNew.objects.order_by('name')
        errors = []
        for event in events:
            count = event.participant_set.filter(gleader=request.user.id, coach=False).count()
            if 0 < count < event.min_limit:
                rem = event.min_limit - count
                errors.append("Please add "+str(rem)+" more participants in "+event.name+"!")
        participants = request.user.participant_set.filter(coach=False)
        coaches = request.user.participant_set.filter(coach=True)
        context = {
            'name' : userprofile,
            'college' : userprofile.college,
            'participants' : participants,
            'coaches' : coaches,
            'errors' : errors,
        }
        return render(request, 'registration/dashboard.html', context)
    else:
        pass

@login_required
def user_delete(request):
    if request.method == "POST":
        if 'delete' in request.POST:
            key = request.POST['id']
            participant = Participant.objects.get(pk=key)
            participant.delete()
    userprofile = request.user.userprofile_set.all()[0]
    participants = request.user.participant_set.filter(coach=False)
    coaches = request.user.participant_set.filter(coach=True)
    events = EventNew.objects.order_by('name')
    errors = []
    for event in events:
        count = event.participant_set.filter(gleader=request.user.id, coach=False).count()
        if 0 < count < event.min_limit:
            rem = event.min_limit - count
            errors.append("Please add "+str(rem)+" more participants in "+event.name+"!")
    context = {
        'name' : userprofile,
        'college' : userprofile.college,
        'participants' : participants,
        'coaches' : coaches,
        'events' : events,
        'errors' : errors,
    }
    return render(request, 'registration/member_delete.html', context)

@login_required
def user_edit(request, error=None):
    userprofile = request.user.userprofile_set.all()[0]
    participants = request.user.participant_set.filter(coach=False)
    coaches = request.user.participant_set.filter(coach=True)
    events = EventNew.objects.order_by('name')
    errors = [] + error if error != None else []
    for event in events:
        count = event.participant_set.filter(gleader=request.user.id, coach=False).count()
        if 0 < count < event.min_limit:
            rem = event.min_limit - count
            errors.append("Please add "+str(rem)+" more participants in "+event.name+"!")
    context = {
        'name' : userprofile,
        'college' : userprofile.college,
        'participants' : participants,
        'coaches': coaches,
        'events' : events,
        'errors' : errors,
    }
    return render(request, 'registration/member_edit.html', context)

@login_required
def user_edit_detail(request):
    if request.method == 'POST':
        if 'edit' in request.POST:
            key = request.POST['id']
            participant = Participant.objects.get(pk=key)
            userprofile = request.user.userprofile_set.all()[0]
            events = EventNew.objects.order_by('name')
            context = {
                'name' : userprofile,
                'college' : userprofile.college,
                'participant': participant,
                'events' : events,
            }
            return render(request, 'registration/member_edit_detail.html', context)
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
                return redirect('registration:edit')
            else:
                return user_edit(request, check)
    else:
        return user_dashboard(request)

@login_required
def user_add(request):
    if request.method == 'POST':
        if 'add' in request.POST:
            coach = request.POST['coach']
            if coach == "True":
                coach = True
            elif coach == "False":
                coach = False
            email = request.POST['email']
            events = request.POST.getlist('events')
            name = request.POST['name']
            phone = request.POST['phone']
            sex = request.POST['sex']
            leader = request.user
            check = check_limits(request)

            user_pr = UserProfile.objects.filter(user = leader)[0]

            if coach == True:
                check = 1
            if check == 1:
                participant = Participant.objects.create(name=name, gender=sex, phone=phone, email_id=email, gleader=leader, coach=coach)
                #### FireWallz bypass for bitsians
                if str(user_pr.college) == 'BITS Pilani':
                    participant.firewallz= True
                    participant.confirmation= True
                for key in events:
                    event = EventNew.objects.get(pk=key)
                    participant.events.add(event)
                participant.save()
                return user_dashboard(request)
            else:
                userprofile = request.user.userprofile_set.all()[0]
                events = EventNew.objects.order_by('name')
                context = {
                    'name' : userprofile,
                    'college' : userprofile.college,
                    'error' : check,
                    'events' : events,
                }
                return render(request, 'registration/member_add.html', context)
    userprofile = request.user.userprofile_set.all()[0]
    events = EventNew.objects.order_by('name')
    context = {
        'name' : userprofile,
        'college' : userprofile.college,
        'participant': None,
        'events' : events,
    }
    return render(request, 'registration/member_add.html', context)

def check_limits(request):
    if 'id' in request.POST:
        partid = request.POST['id']
    events = request.POST.getlist('events')
    userid = request.user.id
    # default = request.user.userprofile_set.all()[0].default_limits
    error = []
    userprofile = str(request.user.userprofile_set.all()[0].id)
    ###### for bitsian registrations limit bypass
    user_ob = User.objects.filter(id=userid)[0]
    user_pro= UserProfile.objects.filter( user = user_ob)[0]
    if user_pro.college == 'BITS Pilani':
        return 1

    for key in events:
        event = EventNew.objects.get(pk=key)
        already = event.participant_set.filter(gleader=userid, coach=False)
        current = len(already)
        max_limit = event.max_limit
        try :
            check = Participant.objects.get(pk=partid)
            if check in already:
                max_limit = max_limit + 1
        except:
            pass
        if current >= max_limit:
            error.append('Only '+str(max_limit)+' participants can be registered for '+event.name+'!')
    if len(error) > 0:
        return error
    else:
        return 1

@login_required
def user_rules(request):
    events = EventNew.objects.order_by('name')
    userprofile = request.user.userprofile_set.all()[0]
    eventdata = []
    for key in events:
        event = {}
        event['name'] = key.name
        event['min_limit'] = key.min_limit
        event['max_limit'] = key.max_limit
        eventdata.append(event)
    context = {
        'eventdata' : eventdata,
        'name' : userprofile,
        'college' : userprofile.college,
    }
    return render(request, 'registration/rules.html', context)

@login_required
def user_sport_view(request):
    userprofile = request.user.userprofile_set.all()[0]
    eventnew = EventNew.objects.order_by('name')
    events = []
    for key in eventnew:
        event = {}
        event['name'] = key.name
        event['count'] = key.participant_set.filter(gleader=request.user.id, coach=False).count()
        event['members'] = key.participant_set.filter(gleader=request.user.id, coach=False).order_by('gender')
        if event['count'] > 0:
            events.append(event)
    context = {
        'events' : events,
        'name' : userprofile,
        'college' : userprofile.college,
    }
    return render(request, 'registration/sport_view.html', context)

def user_logout(request):
    logout(request)
    return redirect('registration:login')

from registration.models import *
from events.models import *
from models import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import string
from random import randint
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def encode_glid(gl_id):
	gl_ida = '0'*(4-len(str(gl_id)))+str(gl_id)
	mixed = string.ascii_uppercase + string.ascii_lowercase
	count = 51
	encoded = ''
	for x in gl_ida:
		encoded = encoded + x
		encoded = encoded + mixed[randint(0,51)]
	return encoded
def get_barcode(request):
	''' list_of_people_selected = InitialRegistration.objects.all()
	# list_of_people_selected = [x for x in list_of_people_selected if x.user]'''
	list_of_people_selected = UserProfile.objects.all()
	list_of_people_selected = [x for x in list_of_people_selected]
	final_display = []
	for x in list_of_people_selected:
		gl_id = x.id
		name = x.firstname + ' ' + x.lastname
		college = x.college
		encoded = encode_glid(gl_id)
		final_display.append((name,college,encoded))
	context = RequestContext(request)
	context_dict = {'final_display':final_display}
	return render_to_response('get_barcode.html', context_dict, context)

def showteam(request,gl_id): #shows team members who have checked in from firewallz booth for teams
	gl = UserProfile.objects.get(id=gl_id)
	participant_list = gl.user.participant_set.all()
	final = [x for x in participant_list if x.firewallz==True]
	context = RequestContext(request)
	context_dict = {'final':final}
	return render_to_response('teamdetails.html', context_dict, context)
####################################Firewallz outer booth code#######################################
#####################################################################################################
@csrf_exempt
def firewallzo_gl(request): #team details editable on first view
	#add gl_name to context dict
	if request.POST:
		if str(request.POST['formtype']) == 'finalform':
			list_of_people_selected = request.POST.getlist('left')
			selectedpeople_list = [int(x) for x in list_of_people_selected]
			display_table = []
			for x in selectedpeople_list:
				participant = Participant.objects.get(id=x)
				participant.firewallz = True
				participant.save()
				participant_name = str(participant.name)
				participant_gender = str(participant.gender)[0].upper()
				if len(participant.events.all()): #checks if the participant has the event otherwise the lenth of the list will be zero
						participant_event_list = [x.name for x in participant.events.all()]
						participant_event = ','.join(participant_event_list)
				else:
					participant_event = ''
				display_table.append((participant_name,participant_gender,participant_event))
			context = RequestContext(request)
			context_dict = {'display_table':display_table}
			return render_to_response('firewallzo_checkout.html', context_dict, context)

		try:
			encoded=request.POST['code']
			decoded = encoded[0]+encoded[2]+encoded[4]+encoded[6] #taking alternative character because alphabets were random and had no meaning
			gl_id = int(decoded) #to remove preceding zeroes and get user profile
			gl = UserProfile.objects.get(id=gl_id)
		except:
			error="Invalid code entered " +encoded
			context = RequestContext(request)
			context_dict = {'error':error}
			return render_to_response('firewallzo_home.html', context_dict, context)

		participant_list = gl.user.participant_set.all() 
		college = str(gl.college)
		gl_name = str(gl.firstname) + ' ' + str(gl.lastname)
		display_participants = []
		done_participants = []
		for p in participant_list:
			participant_name = str(p.name) 
			participant_gender = str(p.gender)[0].upper()#for using just M or F instead of fulll to save space.
			participant_id = int(p.id)
			if len(p.events.all()): #checks if the participant has the event otherwise the lenth of the list will be zero
				participant_event_list = [x.name for x in p.events.all()]
				participant_event = ','.join(participant_event_list)
			else:
				participant_event = '' #done because faculty is not assigned any event
			if p.firewallz != True: #list only particiants whose case is not finalized
				display_participants.append((participant_name,participant_gender,participant_id,participant_event))
			else:
				done_participants.append((participant_name,participant_gender,participant_id,participant_event))

		context = RequestContext(request)
		context_dict = {'display_participants': display_participants, 'college':college, 'gl_name':gl_name,'done_participants':done_participants,'gl':gl}
		return render_to_response('firewallzo_gl.html', context_dict, context)
	else:
		context = RequestContext(request)
		error = ''
		context_dict = {'error':error}
		return render_to_response('firewallzo_home.html', context_dict, context)

@csrf_exempt
@staff_member_required
def firewallzo_remove_people(request,gl_id):
	if request.POST:
		list_of_people_selected = request.POST.getlist('remove')
		selectedpeople_list = [int(x) for x in list_of_people_selected]
		removed_people = []
		for x in selectedpeople_list:
			participant = Participant.objects.get(id=x)
			participant.firewallz = False
			participant.save()
			participant_name = str(participant.name) 
			participant_gender = str(participant.gender[0].upper())
			if len(participant.events.all()): #checks if the participant has the event otherwise the lenth of the list will be zero
				participant_event_list = [x.name for x in participant.events.all()]
				participant_event = ','.join(participant_event_list)
			else:
				participant_event = ''
			removed_people.append((participant_name,participant_gender,participant_event))
		gl = UserProfile.objects.get(id=gl_id)
		#participant_list = gl.user.participant_set.all()
		participant_list = gl.user.participant_set.all()
		approved_participant_list = [x for x in participant_list if x.firewallz == True]
		encoded = encode_glid(gl_id)
		context = RequestContext(request)
		context_dict = {'removed_people':removed_people,'approved_participant_list':approved_participant_list, 'gl_id':gl_id, 'encoded':encoded}
		return render_to_response('firewallzo_remove.html', context_dict, context)
	else:
		gl = UserProfile.objects.get(id=gl_id)
		participant_list = gl.user.participant_set.all()
		approved_participant_list = [x for x in participant_list if x.firewallz == True]
		encoded = encode_glid(gl_id)		
		context = RequestContext(request)
		context_dict = {'approved_participant_list':approved_participant_list, 'gl_id':gl_id,'encoded':encoded}
		return render_to_response('firewallzo_remove.html', context_dict, context)

@csrf_exempt
@staff_member_required
def firewallzo_add_participant(request,gl_id):
	event_list = EventNew.objects.all()
	c = Category.objects.get(name='other')
	category_list = [x for x in Category.objects.all() if x != c]
	category_event_list = []
	event_list = [x for x in event_list if x.category != category_list]
	category_name_list = [x.name for x in category_list]

	try:
		gl=UserProfile.objects.get(id=int(gl_id))
		message = ''
	except:
		return HttpResponse('try again')
	if request.POST:
		# try:
		# 	gl=InitialRegistration.objects.get(id=int(gl_id))
		# except:
		# 	return HttpResponse('Invalid Group Leader')
		participant_name=request.POST['name']
		participant_gender = request.POST['gender']
		participant_contact = request.POST['contact']
		participant_email = request.POST['email']
		par = request.POST.getlist('eventList')
		participant_event_list_final = [int(x) for x in par]
		participant_gl = gl.user
		participant_college = gl.college
		p = Participant(name=participant_name,phone=participant_contact,email_id=participant_email,gleader=gl.user,gender=participant_gender)
		p.save()
		#Now add events

		for event_id in participant_event_list_final:
			participant_event = EventNew.objects.get(id=event_id)
			p.events.add(participant_event)
		p.save()

		#save participant
		message="New Participant added successfully"

	encoded = encode_glid(gl_id)	
	context = RequestContext(request)
	context_dict = {'message':message, 'encoded':encoded,'gl_id':gl_id, 'event_list':event_list, 'category_name_list':category_name_list}
	return render_to_response('firewallzo_add.html', context_dict, context)
@csrf_exempt #currently allows only change of name and gender on firewalzz booth
@staff_member_required
def firewallzo_edit_participant(request,participant_id):
	try:
		participant=Participant.objects.get(id=int(participant_id))
		message = ''
	except:
		return HttpResponse('try again')
	if request.POST:
		participant.name=request.POST['name']
		participant.gender = request.POST['gender']
		participant.save()
		message="Participant Details changed successfully"
	u_id = int(participant.gleader.id)
	user_ob = User.objects.filter(id= u_id)[0]
	user_pr = UserProfile.objects.filter(user = user_ob)[0]
	gl_id = int(user_pr.id)	
	encoded = encode_glid(gl_id)
	context = RequestContext(request)
	context_dict = {'participant':participant,'message':message, 'encoded':encoded,'gl_id':gl_id}

	return render_to_response('firewallzo_edit.html', context_dict, context)

@csrf_exempt
@staff_member_required
def firewallzo_checkout(request):
	selectedpeople = request.session.get('selectedpeople')
	selectedpeople_list = selectedpeople.split()
	selectedpeople_list = [int(x) for x in selectedpeople_list]
	display_table = []
	for x in selectedpeople_list:
		participant = Participant.objects.get(id=x)
		participant.firewallz = True
		participant.save()
		participant_name = str(participant.name) 
		participant_gender = str(participant.gender)[0].upper()
		if len(participant.events.all()): #checks if the participant has the event otherwise the lenth of the list will be zero
				participant_event = str(participant.events.all()[0].name)
		display_table.append((participant_name,participant_gender,participant_event))
	context = RequestContext(request)
	context_dict = {'display_table':display_table}
	return render_to_response('firewallzo_checkout.html', context_dict, context)

@csrf_exempt
@staff_member_required
def firewallzo_gl_reassign(request,gl_id):
	if request.POST:
		if str(request.POST['formtype']) == 'Finalform':
			newid= request.POST['newgl']
			newgl = Participant.objects.filter(id=newid)[0]
			puser = newgl.gleader
			glid = puser.id
			newuser= UserProfile.objects.filter(user=puser)[0]
			newuser.firstname = newgl.name
			newuser.lastname=''
			newuser.phone = int(request.POST['phone'])
			newuser.email_id= newgl.email_id
			newuser.save()
			
			context = RequestContext(request)
			context_dict = {'newgl' : newuser}
			return render_to_response('newglshow.html',context_dict, context)


		# 	newglidlist = str(request.session.get('newglidlist')).split(' ')
		# 	newglidlist = [int(x) for x in newglidlist]
		# 	selected_participant_id=int(request.POST['newgl'])
		# 	participant = Participant.objects.get(id= selected_participant_id)
		# 	#creating user for participant
		# 	final_member_list = [Participant.objects.get(id=x) for x in newglidlist]
		# 	participant_username = str(participant.name).replace(' ','') + str(randint(100,9999))
		# 	if participant.email_id:
		# 		participant_email = participant.email_id
		# 	else:
		# 		participant_email = 'abc@abc.com'
		# 	u = User(username=participant_username, email = participant_email)
		# 	u.save()
		# 	password = randint(1000,9999)
		# 	u.set_password(password)
		# 	#Creating InitialRegistration for participant
		# 	participant_name = participant.name
		# 	participant_college = participant.gleader.initialregistration_set.all()[0].college
		# 	participant_gender = participant.gender
		# 	participant_contact_no = participant.phone
		# 	participant_city = participant.gleader.initialregistration_set.all()[0].city
		# 	newgl = InitialRegistration(name=participant.name,user=u,college=participant_college,gender=participant.gender,phone=participant.phone,city =participant_city)
		# 	newgl.save()
		# 	#assigining the new gl to all selected people
		# 	for x in newglidlist:
		# 		part = Participant.objects.get(id=x)
		# 		part.gleader = newgl.user
		# 		part.save()
		# 	#Generating uniquecode for new_gl
		# 	new_gl_id = newgl.id
		# 	gl_ida = '0'*(4-len(str(new_gl_id)))+str(new_gl_id)
		# 	mixed = string.ascii_uppercase + string.ascii_lowercase
		# 	count = 51
		# 	new_encoded = ''
		# 	for x in gl_ida:
		# 		new_encoded = new_encoded + x
		# 		new_encoded = new_encoded + mixed[randint(0,51)]
		# 	#new_encoded is the unique id of the new_gl
		# 	context = RequestContext(request)
		# 	context_dict = {'newgl':newgl,'new_encoded':new_encoded,'password':password, 'participant_username':participant_username,'final_member_list':final_member_list}
		# 	return render_to_response('newgl_checkout.html', context_dict, context)
		# else:#radio button form
		# 	try:
		# 		new_members_id = request.POST.getlist('newglmember')
		# 		new_members_id = [str(x) for x in new_members_id]
		# 		new_members_id_string = ' '.join(new_members_id)
		# 		new_members_id = [int(x) for x in new_members_id]
		# 	except:
		# 		orignal_gl = UserProfile.objects.get(id=gl_id).user
		# 		participant_list = orignal_gl.participant_set.all()
		# 		not_approved_paticipants = [x for x in participant_list if x.firewallz != True]
		# 		error = 'No selection made'
		# 		context = RequestContext(request)
		# 		context_dict = {'not_approved_participants':not_approved_participants,'error':error,'gl_id':gl_id}
		# 		return render_to_response('newglcheckbox.html', context_dict, context)
			
			# request.session['newglidlist'] = new_members_id_string
			# new_members_list = [Participant.objects.get(id=y) for y in new_members_id]
			# context = RequestContext(request)
			# context_dict = {'new_members_list':new_members_list,'gl_id':gl_id}
			# return render_to_response(, context_dict, context)

	else:
		orignal_gl = UserProfile.objects.get(id=gl_id).user
		participant_list = orignal_gl.participant_set.all()
		not_approved_participants = [x for x in participant_list if x.firewallz != True]
		error = ''
		context = RequestContext(request)
		context_dict = {'not_approved_participants':not_approved_participants,'error':error,'gl_id':gl_id}
		return render_to_response('newglcheckbox.html', context_dict, context)



@csrf_exempt
@staff_member_required
def firewallz_fid(request):
	if request.POST:
		try:
			encoded=request.POST['code']
			decoded = encoded[0]+encoded[2]+encoded[4]+encoded[6] #taking alternative character because alphabets were random and had no meaning
			gl_id = int(decoded) #to remove preceding zeroes and get user profile
			gl = UserProfile.objects.get(id=gl_id)
			request.session['glidfire'] = str(gl_id)
		except:
			encoded=request.POST['code']
			decoded = encoded[0]+encoded[2]+encoded[4]+encoded[6] #taking alternative character because alphabets were random and had no meaning
			gl_id = int(decoded) #to remove preceding zeroes and get user profile
			gl = UserProfile.objects.get(id=gl_id)
			request.session['glidfire'] = str(gl_id)
			error="Invalid code entered " +encoded
			context = RequestContext(request)
			context_dict = {'encoded':encoded}
			return render_to_response('firewallzi_home.html', context_dict, context)
		
		if request.POST:
			if str(request.POST['formtype']) == 'finalform':
				gl_id = int(request.session.get('glidfire'))
				gl = UserProfile.objects.get(id=gl_id)
				participant_list = gl.user.participant_set.all()
			
				firewallz_controlz_approved = [x for x in participant_list if x.firewallz == True and x.fid != True and x.controlzpay == True]
				for x in firewallz_controlz_approved:
					if x.id in request.POST:
						x.fid = True
						x.save()
				done_list = [x for x in participant_list if x.firewallz == True and x.fid == True and x.controlzpay == True]
				participant_list = gl.user.participant_set.all()
				firewallz_controlz_approved = [x for x in participant_list if x.firewallz == True and x.fid != True and x.controlzpay == True]
				context = RequestContext(request)
				context_dict = {'firewallz_controlz_approved':firewallz_controlz_approved,'done_list':done_list}
				return render_to_response('firewallzi_checkout.html', context_dict, context)
		
			else:
				gl_id = int(request.session.get('glidfire'))
				gl = UserProfile.objects.get(id=gl_id)
				participant_list = gl.user.participant_set.all()
				firewallz_controlz_approved = [x for x in participant_list if x.firewallz == True and (x.fid)== False and x.controlzpay == True]
				done_list = [x for x in participant_list if x.firewallz == True and (x.fid)== True]
				context = RequestContext(request)
				context_dict = {'firewallz_controlz_approved':firewallz_controlz_approved,'done_list':done_list}
				return render_to_response('firewallzi_checkout.html', context_dict, context)
	else:
		context = RequestContext(request)
		error = ''
		context_dict = {'error':error}
		return render_to_response('firewallzi_home.html', context_dict, context)

@staff_member_required
def recnacc_dashboard(request, gl_id):
		gl = UserProfile.objects.get(id=gl_id)
		participant_list = gl.user.participant_set.all() 
		college = str(gl.college)
		gl_name = str(gl.firstname +' '+ gl.lastname)
		display_participants = []
		done_participants = []
		no_males=0
		no_females=0
		for p in participant_list:
			if p.gender[0].upper()=="M" and p.firewallz ==True and p.acco!=True:
				no_males+=1
			elif p.gender[0].upper()=="F" and p.firewallz ==True and p.acco!=True:
				no_females+=1		
			participant_name = str(p.name) 
			participant_gender = str(p.gender)[0].upper()#for using just M or F instead of fulll to save space.
			participant_id = int(p.id)
			if p.acco == True and p.room:
				participant_room = str(p.room.room)+' '+p.room.bhavan.name
			else:
				participant_room = ''
			# if len(p.events.all()): #checks if the participant has the event otherwise the lenth of the list will be zero
			# 	participant_event = str(p.events.all()[0].name)
			# else:
			# 	participant_event = '' #done because faculty is not assigned any event
			if p.firewallz == True: #list only particiants who have been approved by firewallz
				display_participants.append((participant_name,participant_gender,participant_id,participant_room))
		done_participants = [x for x in participant_list if x.firewallz==True and x.acco==True]
		context = RequestContext(request)
		context_dict = {'done_participants':done_participants,'display_participants': display_participants, 'college':college, 'no_males':no_males, 'no_females':no_females,
		'gl_name':gl_name,'done_participants':done_participants, "gl_id":gl_id}
		return render_to_response('reconec_gl.html', context_dict, context)

@csrf_exempt
def reconec_home(request):
	#simple template to enter id
	if request.POST:
		try:
			encoded=request.POST['code']
			decoded = encoded[0]+encoded[2]+encoded[4]+encoded[6] #taking alternative character because alphabets were random and had no meaning
			gl_id = int(decoded) #to remove preceding zeroes and get user profile
			return redirect('regsoft:recnacc_dashboard', gl_id)
		except:
			error="Invalid code entered " +encoded
			context = RequestContext(request)
			context_dict = {'error':error}
			return render_to_response('reconec_home2.html', context_dict, context)

		# participant_list = gl.user.participant_set.all() 
		# college = str(gl.college)
		# gl_name = str(gl.firstname +' '+ gl.lastname)
		# display_participants = []
		# done_participants = []
		# no_males=0
		# no_females=0
		# for p in participant_list:
		# 	if p.gender[0].upper()=="M" and p.firewallz ==True and p.acco!=True:
		# 		no_males+=1
		# 	elif p.gender[0].upper()=="F" and p.firewallz ==True and p.acco!=True:
		# 		no_females+=1		
		# 	participant_name = str(p.name) 
		# 	participant_gender = str(p.gender)[0].upper()#for using just M or F instead of fulll to save space.
		# 	participant_id = int(p.id)
		# 	if p.acco == True and p.room:
		# 		participant_room = str(p.room.room)+' '+p.room.bhavan.name
		# 	else:
		# 		participant_room = ''
		# 	# if len(p.events.all()): #checks if the participant has the event otherwise the lenth of the list will be zero
		# 	# 	participant_event = str(p.events.all()[0].name)
		# 	# else:
		# 	# 	participant_event = '' #done because faculty is not assigned any event
		# 	if p.firewallz == True: #list only particiants who have been approved by firewallz
		# 		display_participants.append((participant_name,participant_gender,participant_id,participant_room))
		# done_participants = [x for x in participant_list if x.firewallz==True and x.acco==True]
		# context = RequestContext(request)
		# context_dict = {'done_participants':done_participants,'display_participants': display_participants, 'college':college, 'no_males':no_males, 'no_females':no_females,
		# 'gl_name':gl_name,'done_participants':done_participants, "gl_id":gl_id}
		# return render_to_response('reconec_gl.html', context_dict, context)
	else:
		context = RequestContext(request)
		error = ''
		context_dict = {'error':error}
		return render_to_response('reconec_home2.html', context_dict, context)

@csrf_exempt
@staff_member_required
def acco_list(request,gl_id):

	#list acco with availibilty
	#ability to select
	bhavan_list= Bhavan.objects.all()
	initial_vacancy_display= []
	vacancy_display = []
	for bhavan in bhavan_list:
		if bhavan.id != 1:
			bhavan_name = bhavan.name
			rooms = bhavan.room_set.all()
			initial_vacancy_display.append((bhavan_name,rooms))
	all_rooms = []
	for bhavan in bhavan_list:
		if bhavan.id != 1:
			bhavan_name = bhavan.name
			rooms = [x for x in bhavan.room_set.all()]
			all_rooms += rooms
			if len(rooms):
				vacancy_display.append((bhavan_name,rooms))
	gl = UserProfile.objects.get(id=gl_id)
	participant_list = gl.user.participant_set.all() 
	no_males=0
	no_females=0
	for p in participant_list:
		if p.gender[0].upper()=="M" and p.firewallz ==True and p.acco!=True:
			no_males+=1
		elif p.gender[0].upper()=="F" and p.firewallz ==True and p.acco!=True:
			no_females+=1
	if request.POST:
		try:
			request.POST.getlist('roomid')
		except:
			error="Invalid Room Selected"
			context = RequestContext(request)
			context_dict = {'error':error}
			return render_to_response('reconec_acco.html', context_dict, context)
		for roomid in request.POST.getlist('roomid'):
			# roomid=request.POST.getlist('roomid')
			x = roomid + 'alloted'
			noalloted=int(request.POST[x])
			roomid = int(roomid)
			no_males=0
			no_females=0
			for p in participant_list:
				if p.gender[0].upper()=="M" and p.firewallz ==True and p.acco!=True:
					no_males+=1
				elif p.gender[0].upper()=="F" and p.firewallz ==True and p.acco!=True:
					no_females+=1
			selectedroom = Room.objects.get(id=roomid)
			selectedroom_availibilty = selectedroom.vacancy
			unalloted_males = [x for x in participant_list if x.firewallz == True and x.gender[0].upper() == 'M' and x.acco != True]
			unalloted_females = [x for x in participant_list if x.firewallz == True and x.gender[0].upper() == 'F' and x.acco != True]
			if selectedroom.bhavan.name == 'MB' or selectedroom.bhavan.name == 'MB 1' or selectedroom.bhavan.name == 'MB 3' or selectedroom.bhavan.name == 'MB 4' or selectedroom.bhavan.name == 'MB 5' or selectedroom.bhavan.name == 'MB 6-1' or selectedroom.bhavan.name == 'MB 6-2'or selectedroom.bhavan.name == 'MB 9' or selectedroom.bhavan.name == 'SQ' or selectedroom.bhavan.name == 'CVR': #use or for extra bhavanas
				if no_females<noalloted:
					return HttpResponse('error: Alloted rooms are greater than the number of participants. <br /> <a href="http://www.bits-bosm.org/2015/regsoft/recnacc/allot/%s/">Back</a>' % gl_id)
				for y in range(noalloted):
					unalloted_females[y].acco=True
					unalloted_females[y].room = selectedroom
					selectedroom.vacancy -= 1
					selectedroom.save()
					unalloted_females[y].save()
			
			else:
				if no_males<noalloted:
					return HttpResponse('error: Alloted rooms are greater than the number of participants. <br /> <a href="http://www.bits-bosm.org/2015/regsoft/recnacc/allot/%s/">Back</a>' % gl_id)
				for y in range(noalloted):
					unalloted_males[y].acco=True
					unalloted_males[y].room = selectedroom
					selectedroom.vacancy -= 1
					selectedroom.save()
					unalloted_males[y].save()
		#return HttpResponse(selectedroom.vacancy)
		no_males=0
		no_females=0
		participant_list = gl.user.participant_set.all()
		for p in participant_list:
			if p.gender[0].upper()=="M" and p.firewallz ==True and p.acco!=True:
				no_males+=1
			elif p.gender[0].upper()=="F" and p.firewallz ==True and p.acco!=True:
				no_females+=1
		bhavan_list= Bhavan.objects.all()
		all_rooms =[]
		for bhavan in bhavan_list:
			if bhavan.id != 1:
				bhavan_name = bhavan.name
				rooms = [x for x in bhavan.room_set.all() if x.vacancy != 0]
				all_rooms += rooms
				if len(rooms):
					vacancy_display.append((bhavan_name,rooms))
		done_participants = [x for x in participant_list if x.firewallz==True and x.acco==True]
		context = RequestContext(request)
		context_dict = {'done_participants':done_participants,'all_rooms':all_rooms,'no_males':no_males, 'no_females':no_females,"gl_id":gl_id, 'vacancy_display':vacancy_display}
		return render_to_response('reconec_acco.html', context_dict, context)

	else:
		done_participants = [x for x in participant_list if x.firewallz==True and x.acco==True]
		context = RequestContext(request)
		context_dict = {'done_participants':done_participants,'all_rooms':all_rooms,'vacancy_display':vacancy_display, 'no_males':no_males, 'no_females':no_females, "gl_id":gl_id}
		return render_to_response('reconec_acco.html', context_dict, context)
@staff_member_required
def all_bhawans(request):
	bhavan_list= Bhavan.objects.all()
	all_rooms = []
	for bhavan in bhavan_list:
		bhavan_name = bhavan.name
		rooms = [x for x in bhavan.room_set.all()]
		all_rooms += rooms
	context = RequestContext(request)
	context_dict = {'all_rooms':all_rooms}
	return render_to_response('all_bhavans.html', context_dict, context)

@csrf_exempt
@staff_member_required
def room_details(request):
	room_list= [x for x in Room.objects.all() if x.id != 1]
	room_list_mod = [(str(x.bhavan.name)+' '+str(x.room)+'#'+str(x.id),x) for x in room_list]
	if request.POST:
		roomid=str(request.POST['roomid'])
		roomid = int(roomid[roomid.find('#')+1:])
		selectedroom = Room.objects.get(id=roomid)
		room_participants = selectedroom.participant_set.all()
		gl_list = []
		gl_count = {}
		for p in room_participants:
			if p.gleader.initialregistration_set.all()[0] not in gl_list:
				gl_list.append(p.gleader.initialregistration_set.all()[0])
				gl_count[p.gleader.initialregistration_set.all()[0]] = 1
			else:
				gl_count[p.gleader.initialregistration_set.all()[0]] += 1

		context = RequestContext(request)
		context_dict = {'gl_list':gl_list, 'room_list_mod':room_list_mod, 'gl_count':gl_count}
		return render_to_response('room_details.html', context_dict, context)

	context = RequestContext(request)
	context_dict = {'room_list_mod':room_list_mod}
	return render_to_response('room_details.html', context_dict, context)	

@csrf_exempt
@staff_member_required
def reconec_deallocate(request,gl_id):
	gl = UserProfile.objects.get(id=gl_id)
	alloted_people = [x for x in gl.user.participant_set.all() if x.firewallz == True and x.acco == True]
	if request.POST:
		try:
			list_of_people_selected = request.POST.getlist('deallocate')
		except:
			return HttpResponse('No one was selected')
		selected_people_list = [int(x) for x in list_of_people_selected]
		done_people = []
		for x in selected_people_list:
			p= Participant.objects.get(id=x)
			p.acco = False
			selected_room = p.room
			selected_room.vacancy += 1
			selected_room.save()
			p.room = None
			p.save()
			done_people.append(p)
		alloted_people = [x for x in gl.user.participant_set.all() if x.firewallz == True and x.acco == True]
		context = RequestContext(request)
		context_dict = {'done_people':done_people, 'alloted_people':alloted_people,"gl_id":gl_id}
		return render_to_response('reconec_deallocate.html', context_dict, context)
	else:
		done_people = []
		context = RequestContext(request)
		context_dict = {'done_people':done_people, 'alloted_people':alloted_people,"gl_id":gl_id}
		return render_to_response('reconec_deallocate.html', context_dict, context)
		
@csrf_exempt
@staff_member_required
def phonedetails(request,gl_id):
	gl = UserProfile.objects.get(id=gl_id)
	participant_list = gl.user.participant_set.all()
	context = RequestContext(request)
	context_dict = {'participant_list':participant_list}
	return render_to_response('reconec_phone.html', context_dict, context)


@csrf_exempt
@staff_member_required
def reconec_checkout(request,gl_id):
	#simple template to enter id
	postcheck = False
	if request.POST:
		postcheck = True
		try:
			list_of_people_selected = request.POST.getlist('checkout')
		except:
			return HttpResponse('error')

		selectedpeople_list = [int(x) for x in list_of_people_selected]
		display_table = []
		for x in selectedpeople_list:
			participant = Participant.objects.get(id=x)
			participant_room = participant.room
			participant_room.vacancy += 1
			participant_room.save()
			participant.room = Room.objects.get(id=1)
			croom = Room.objects.get(id=1)
			croom.vacancy -= 1
			croom.save()
			participant.save()
			participant_name = str(participant.name) 
			participant_gender = str(participant.gender)[0].upper()
			if len(participant.events.all()): #checks if the participant has the event otherwise the lenth of the list will be zero
					participant_event = str(participant.events.all()[0].name)
			else:
				participant_event = ''
			display_table.append((participant_name,participant_gender,participant_event))
		gl = UserProfile.objects.get(id=gl_id)
		participant_list = gl.user.participant_set.all() 
		college = str(gl.college)
		gl_name = str(gl.firstname + ' ' + gl.lastname)
		final_participants = [x for x in participant_list if x.firewallz==True and x.acco==True and x.room.bhavan.id != 1]
		context = RequestContext(request)
		context_dict = {'college':college,"gl_id":gl_id,'display_table':display_table, 'postcheck':postcheck}
		return render_to_response('reconec_checkout.html', context_dict, context)


	else:
		gl = UserProfile.objects.get(id=gl_id)
		participant_list = gl.user.participant_set.all() 
		college = str(gl.college)
		gl_name = str(gl.firstname + ' ' + gl.lastname)
		final_participants = [x for x in participant_list if x.firewallz==True and x.acco==True and x.room.bhavan.id != 1]
		context = RequestContext(request)
		context_dict = {'final_participants':final_participants, 'college':college,"gl_id":gl_id}
		return render_to_response('reconec_checkout.html', context_dict, context)
@staff_member_required
def college_in_bhavan(request):
	colleges = {}
	bhavan_list = Bhavan.objects.all()

	for bhavan in bhavan_list:
		colleges[bhavan.name] = []
		for room in bhavan.room_set.all():
			for participant in room.participant_set.all():
				participant_college = participant.gleader.userprofile_set.all()[0].college
				if participant_college not in colleges[bhavan.name]:
					colleges[bhavan.name].append(participant_college)
	display = []
	for x in colleges:
		for y in colleges[x]:
			display.append((x,y))

	context = RequestContext(request)
	context_dict = {'display':display}
	return render_to_response('reconec_bhavanwise.html', context_dict, context)

@csrf_exempt
def receipt(request):
	if request.POST:
		try:
			encoded=request.POST['code']
			decoded = encoded[0]+encoded[2]+encoded[4]+encoded[6] #taking alternative character because alphabets were random and had no meaning
			gl_id = int(decoded) #to remove preceding zeroes and get user profile
			gl = UserProfile.objects.get(id=gl_id)
			if encoded == "":
				college = request.POST['college']
				gl = UserProfile.objects.get(college=college)			
		except:
			error="Invalid code entered " +encoded
			context = RequestContext(request)
			context_dict = {'error':error}
			return render_to_response('controlzhome.html', context_dict, context)
		college = gl.college
		uid = encoded
		people = [x for x in gl.user.participant_set.all() if x.firewallz == True and x.controlzpay != True]
		done_participants = [x for x in gl.user.participant_set.all() if x.firewallz == True and x.controlzpay == True]
		request.session['uid'] = encoded
		# count=0
		# for ppl in people:
		# 	if ppl.controlzpay == True:
		# 		count+=1
		#error = ''
		#if len(people)==0:
			#error="No receipt can be generated now."
			#context = RequestContext(request)
			#context_dict = {'error':error}
			#return render_to_response('controlzhome.html', context_dict, context)

		context = RequestContext(request)
		context_dict = {'people':people, 'done_participants':done_participants,'gl_id':gl.id,'encoded':encoded}
		return render_to_response('controlgl.html', context_dict, context)		


	else:
		context = RequestContext(request)
		colleges = UserProfile.objects.order_by('college')
		context_dict = {'users':colleges}
		return render_to_response('controlzhome.html', context_dict, context)

def controlz_lists(request):
	participants = None
	if request.POST:
		event = request.POST['sport']
		user = request.POST['college']
		all_participants = Participant.objects.all()
		if event == "":
			events = EventNew.objects.all()
			eventwise = all_participants
			if user == "":
				participants = eventwise
			elif user != "":
				userid = int(user.rsplit('| ', 1)[1])
				participants = [x for x in eventwise if x.gleader.id == userid]

		elif event != "":
			eventid = int(event.rsplit('| ', 1)[1])
			event = EventNew.objects.get(id=eventid)
			eventwise = [x for x in all_participants if event in x.events.all()]
			if user == "":
				participants = eventwise
			elif user != "":
				userid = int(user.rsplit('| ', 1)[1])
				participants = [x for x in eventwise if x.gleader.id == userid]
		# eventwise = [x for x in all_participants if events in x.events.all()]
		# all_participants = Participant.objects.filter(controlzpay=True)
		# participants = [x for x in all_participants if x.gleader == college and event in x.event_set.all()]
	users = [x for x in UserProfile.objects.all()]
	sports = [x for x in EventNew.objects.all()]
	context = {
		'users':users,
		'sports':sports,
		'participants':participants,
	}
	return render(request, 'controlz_list.html', context)

@csrf_exempt
def enter_denominations(request,gl_id):
	if request.POST:
		gl = UserProfile.objects.get(id=gl_id)
		list_of_people_selected = request.POST.getlist('left')
		selectedpeople_list = [int(x) for x in list_of_people_selected]
		display_table = []
		for x in selectedpeople_list:
			participant = Participant.objects.get(id=x)
			display_table.append(participant)
	
	#people = [x for x in gl.user.participant_set.all() if x.firewallz == True and x.controlzpay != True and x.coach != True]
	#bill_no_raw = len(Bill_new.objects.all()) + 1
	#rec = '0'*(4-len(str(bill_no_raw)))+str(bill_no_raw)
	number_of_participants = len(selectedpeople_list)
	register=750
	amount=750*number_of_participants
	return render_to_response('bill_template.html',{'college':gl.college,'number_of_participants':number_of_participants,'register':register,'amount':amount,'gl_id':gl.id,'display_table':display_table})

# @csrf_exempt
# def generate_receipt(request,gl_id):	
	# gl=UserProfile.objects.get(id=gl_id)
	# if request.POST:
		# if str(request.POST['formtype']) == 'finalform':
			# bill_part = request.POST['left']
			# college = gl.college
			# participant = Participant.objects.filter(bill_id=bill_part)
			
				
	# encoded = encode_glid(gl_id)
	# #billno = request.POST['billid']
	# gl=UserProfile.objects.get(id=gl_id)
	# participant_list = gl.user.participant_set.all()
	# b_list=[]
	# for p in participant_list:	
		# if p.firewallz == True and p.controlzpay==True:
			# if str(p.bill_id) not in b_list:
				# bid = str(p.bill_id)
				# b_list.append(bid)
	
	# context = RequestContext(request)
	# context_dict = {'b_list':b_list}
	# # # p = Participant.objects.filter(gleader=gl)
		# # # for x in p:
			# # # x.controlzpay = False
			# # # x.bill_id = None
			# # # x.fid = False
		
		# # # a = Bill_new.objects.filter(number=billno)[0]
		# # # a.remove()
		# # #return render_to_response('revertbill.html',{'message':'This Bill_new has been cancelled'} )
	# return render_to_response('revertbill.html', context_dict, context)
	
@csrf_exempt
def generate_receipt(request,gl_id):
	if request.POST:
		# n1000 = request.POST['n_1000']
		# n500 = request.POST['n_500']
		# n100 = request.POST['n_100']
		# n50 = request.POST['n_50']
		# n20 = request.POST['n_20']
		# n10 = request.POST['n_10']
		gl = UserProfile.objects.get(id=gl_id)
		list_of_people_selected = request.POST.getlist('left')
		selectedpeople_list = [int(x) for x in list_of_people_selected]
		register=750
		number_of_participants = len(selectedpeople_list)
		
		amount=750*number_of_participants
		ddno = request.POST['dd']
		
	#calculationg amount
		
	#now make Bill_new
		
		a = Bill_new()
		# a.notes_1000= n1000
		# a.notes_500= n500
		# a.notes_100= n100
		# a.notes_50= n50
		# a.notes_20= n2
		# a.notes_10= n10
		a.draft_number = ddno
		a.gleader = gl.firstname + ' ' + gl.lastname
		a.college = gl.college
		#a.number = bill_no_raw 
		a.amount = amount
		a.save()
		rec = '0'*(4-len(str(a.id)))+str(a.id)
		
		display_table = []
		#bill_no_raw = len(Bill_new.objects.all()) + 1
		for x in selectedpeople_list:
			participant = Participant.objects.get(id=x)
			participant.controlzpay= True
			participant.bill_id = a.id
			participant.save()
		
		uid = request.session['uid']
		
		return render_to_response('controlz_gen_bill.html',{'college':gl.college,'uid':uid,'register':register,'amount':amount,'receiptno':rec,'gl_id':gl.id})


@csrf_exempt
def print_receipt(request,gl_id):
	if request.POST:
		college=request.POST['college']
		uid=request.POST['uid']
		register=request.POST['register']
		amount=request.POST['amount']
		rec=request.POST['receiptno']
		return render_to_response('receipt.html',{'college':college,'uid':uid,'register':register,'amount':amount,'receiptno':rec})
		
@csrf_exempt
def controlz_edit_participant(request,participant_id):
	try:
		participant=Participant.objects.get(id=int(participant_id))
		message = ''
	except:
		return HttpResponse('try again')
	#participant_selected_events = [event for event in participant.events.all()]
	p = participant
	event_list = EventNew.objects.all()
	#c = Category.objects.get(name='other')
	#category_list = [x for x in Category.objects.all() if x != c]
	#category_event_list = []
	##event_list = [x for x in event_list if x.category != c]
	##category_name_list = [x.name for x in category_list]
	participant_event_list = participant.events.all()
	event_add_list = [x for x in event_list if x not in participant_event_list]

	if request.POST:
		try:
			addorremove = request.POST['addorremove']
		except:
			return HttpResponse('error')
		if addorremove == 'add':
			selected_event_name = request.POST['eventselected']
			selected_event = EventNew.objects.get(name=selected_event_name)
			p.events.add(selected_event)
			p.save()
			message="Participant Details changed successfully"
		elif addorremove == 'remove':
			selected_event_name = request.POST['eventselected']
			selected_event = EventNew.objects.get(name=selected_event_name)
			p.events.remove(selected_event)
			p.save()
			message="Participant Details changed successfully"
	participant_event_list = participant.events.all()
	event_add_list = [x for x in event_list if x not in participant_event_list]
	gl_id = participant.gleader.id
	encoded = encode_glid(gl_id)
	context = RequestContext(request)
	context_dict = {'event_add_list':event_add_list,'participant':participant,'message':message, 'encoded':encoded,'gl_id':gl_id,'participant_event_list':participant_event_list}

	return render_to_response('controlz_edit.html', context_dict, context)

@csrf_exempt
def controlz_sport_leader(request,participant_id):
	try:
		participant=Participant.objects.get(id=int(participant_id))
		message = ''
	except:
		return HttpResponse('try again')
	#participant_selected_events = [event for event in participant.events.all()]
	p = participant
	event_list = EventNew.objects.all()
	#c = Category.objects.get(name='other')
	#category_list = [x for x in Category.objects.all() if x != c]
	#category_event_list = []
	#event_list = [x for x in event_list if x.category != c]
	#category_name_list = [x.name for x in category_list]
	participant_event_list = participant.events.all()
	participant_sport_leader = participant.sport_leader
	#event_add_list = [x for x in event_list if x not in participant_event_list]

	if request.POST:
		selected_event_name = request.POST['eventselected']
		phoneno = request.POST['phonen']
		selected_event = EventNew.objects.get(name=selected_event_name)
		p.sport_leader = selected_event_name
		p.phone = phoneno
		p.save()
		message="Successfully made sport leader."
		usr_ob = participant.gleader
		user_ob= UserProfile.objects.filter(user = usr_ob)[0]
		gl_id = user_ob.id
		encoded = encode_glid(gl_id)
		#participant_event_list = participant.events.all()
		#participant_sport_leader = participant.sport_leader
		context = RequestContext(request)
		context_dict = {'participant':participant,'message':message, 'encoded':encoded,'gl_id':gl_id,'participant_event_list':participant_event_list,'participant_sport_leader':participant_sport_leader}
		return render_to_response('make_sl.html', context_dict, context)
		
	#participant_event_list = participant.events.all()
	#event_add_list = [x for x in event_list if x not in participant_event_list]
	
	usr_ob = participant.gleader
	user_ob= UserProfile.objects.filter(user = usr_ob)[0]
	gl_id = user_ob.id
	encoded = encode_glid(gl_id)
	context = RequestContext(request)
	context_dict = {'participant':participant,'message':message, 'encoded':encoded,'gl_id':gl_id,'participant_event_list':participant_event_list,'participant_sport_leader':participant_sport_leader}

	return render_to_response('make_sl.html', context_dict, context)
	
@csrf_exempt
@staff_member_required
def controlz_event_details(request):
	#c = Category.objects.get(name='other')
	event_list= EventNew.objects.all()
	event_list_mod = [(str(x.name)+'#'+str(x.id),x) for x in event_list]
	if request.POST:
		eventid=str(request.POST['eventid'])
		eventid = int(eventid[eventid.find('#')+1:])
		selected_event = EventNew.objects.get(id=eventid)
		event_participants_temp = [x for x in selected_event.participant_set.all() if x.controlzpay == True]
		event_participants = [(x,x.gleader.college) for x in selected_event.participant_set.all() if x.controlzpay == True]
		no_males = len([x for x in event_participants_temp if x.gender[0].upper() == 'M'])
		no_females = len(event_participants)-no_males
		context = RequestContext(request)
		context_dict = {'event_participants':event_participants, 'event_list_mod':event_list_mod,'no_males':no_males,'no_females':no_females}
		return render_to_response('controlz_event_details.html', context_dict, context)

	context = RequestContext(request)
	context_dict = {'event_list_mod':event_list_mod}
	return render_to_response('controlz_event_details.html', context_dict, context)	

@csrf_exempt
def show_prev_bills(request):
	all_participants = Participant.objects.filter(controlzpay = True)
	bill_num = Bill_new.objects.all()
	all_bills = []
	#if not bill_num:
	for x in bill_num:
		bill_number = x.id
		part = Participant.objects.filter(bill_id = x.id)[0]
		# # for y in part:
			# # if y.bill_id == bill_number:
				# # group_lead = y.gleader
				# # break
		group_lead = part.gleader
		gl = UserProfile.objects.get(user = group_lead)
		college_nm = gl.college
		group_lead_name = gl.firstname + " " + gl.lastname
		all_bills.append((bill_number,college_nm,group_lead_name))
	context = RequestContext(request)
	context_dict = {'all_bills':all_bills}
	return render_to_response('show_bills.html',context_dict, context)
	#else:
	#	return render_to_response('show_bills.html',{'message':'No bills are created yet'})
@csrf_exempt	
def bill_details(request, bid):
	all_participants = Participant.objects.all()
	all_parts = []
	for x in all_participants:
		if str(x.bill_id) == str(bid):
			part_name = x.name
			part_gender = x.gender
			part_phone = x.phone
			all_parts.append((part_name, part_gender, part_phone))
	return render_to_response('bill_details.html',{'all_parts':all_parts})	


@csrf_exempt
def controlz_cancel_bill(request, gl_id):
	participant_list_bill_ref=[]
	if request.POST:
		if str(request.POST['formtype']) == 'finalform':
			bill_part = request.POST['left']
			participant = Participant.objects.filter(bill_id=bill_part)
			for x in participant:
				if x.firewallz== True and x.controlzpay == True:
					x.controlzpay = False
					x.bill_id = None
					x.save()
			a = Bill_new.objects.filter(id=bill_part).delete()
		
		# if str(request.POST['formtype']) == 'partform':
			# bill_number = request.POST['bill_number']
			# participant_list_bill_ref = Participant.objects.filter(bill_id=bill_number)
					
	encoded = encode_glid(gl_id)
	#billno = request.POST['billid']
	gl=UserProfile.objects.get(id=gl_id)
	participant_list = gl.user.participant_set.all()
	b_list=[]
	for p in participant_list:	
		if p.firewallz == True and p.controlzpay==True:
			if str(p.bill_id) not in b_list:
			#if p not in b_list:
				bid = str(p.bill_id)
				p_ref_name = str(p.name)
				b_list.append((bid,p_ref_name))
	
	context = RequestContext(request)
	context_dict = {'b_list':b_list}
	# # p = Participant.objects.filter(gleader=gl)
		# # for x in p:
			# # x.controlzpay = False
			# # x.bill_id = None
			# # x.fid = False
		
		# # a = Bill_new.objects.filter(number=billno)[0]
		# # a.remove()
		# #return render_to_response('revertbill.html',{'message':'This Bill_new has been cancelled'} )
	return render_to_response('revertbill.html', context_dict, context)
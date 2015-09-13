# -*- coding: utf-8 -*-
from registration.models import *
from django.http import HttpResponse
from django.template.loader import get_template
from barg import code128_image
from django.template import Context
import ho.pisa as pisa
import cgi
import cStringIO as StringIO
#import GifImagePlugin
import sys
import os
from django.views.static import serve
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, EmailMessage
import pyPdf
import os
import string
from random import randint
import shutil
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect,render
sys.path.append('/home/dvm/taruntest/')
sys.path.append('/home/dvm/taruntest/oasis/')
@staff_member_required
def freeze_all(request):
	selected_users = [x.user for x in InitialRegistration.objects.all() if x.user]
	for x in selected_users:
		x.is_active = False
		x.save()
	return HttpResponse('All users have now been frozen')
@staff_member_required
def unfreeze_all(request):
	selected_users = [x.user for x in InitialRegistration.objects.all() if x.user]
	for x in selected_users:
		x.is_active = True
		x.save()
	return HttpResponse('All users have now been unfrozen')
def encode_glid(gl_id):
	gl_ida = '0'*(4-len(str(gl_id)))+str(gl_id) #convert gl_id to a string of lenth 4 by prefixing no of zeroes as required.
	mixed = string.ascii_uppercase + string.ascii_lowercase
	count = 51
	encoded = ''
	#now adding alternatve random characters
	for x in gl_ida:
		encoded = encoded + x
		encoded = encoded + mixed[randint(0,51)]
	return encoded
def gen_barcode(gl_id):
	encoded = encode_glid(gl_id)
	image='/home/dvm/oasis/public_html/taruntest/oasiscode/%s.png' % str(gl_id)
	code128_image(encoded).save(image, 'PNG')
	return encoded
def write_pdf(gl_id,encoded):
	gl = InitialRegistration.objects.get(id=gl_id)
	participants = gl.user.participant_set.all()
	no_of_participants = len(participants)
	no_of_pages = no_of_participants / 20 + int(bool(no_of_participants % 20))
	if no_of_pages ==0:
		return 'lite'
	if no_of_pages == 1:
		page_participants = participants
		display_page_participants = []
		for p in page_participants:
			name = p.name
			gender = p.gender[0].upper()
			events_list = [x.name for x in p.events.all()]
			if len(events_list) < 6:
				events = ','.join(events_list)
			else:
				events = ','.join(events_list[0:5]) + '...'
			display_page_participants.append((name,gender,events))
		no_of_males = len([x for x in participants if str(x.gender)[0].upper() == 'M'])
		no_of_females = len(participants)-no_of_males
		barcode_name = '%s' % gl_id
		template = get_template('firstwithbarcode.html')
		context = Context({'display_page_participants':display_page_participants,'gl':gl,'no_of_males':no_of_males,'no_of_females':no_of_females,'encoded':encoded,'barcode_name':barcode_name})
		html = template.render(context)
		result = open('/home/dvm/taruntest/oasis/%s.pdf' %(str(gl_id)), 'wb')
		pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, encoding='UTF-8')
		result.close()
	else:
		#first page
		page_participants = participants[0:20]
		no_of_males = len([x for x in participants if str(x.gender)[0].upper() == 'M'])
		no_of_females = len(participants)-no_of_males
		display_page_participants = []
		for p in page_participants:
			name = p.name
			gender = p.gender[0].upper()
			events_list = [x.name for x in p.events.all()]
			if len(events_list) < 6:
				events = ','.join(events_list)
			else:
				events = ','.join(events_list[0:5]) + '...'
			display_page_participants.append((name,gender,events))
		barcode_name = '%s' % gl_id
		template = get_template('firstwithoutbarcode.html')
		context = Context({'display_page_participants':display_page_participants,'gl':gl,'encoded':encoded,'barcode_name':barcode_name,'no_of_males':no_of_males,'no_of_females':no_of_females})
		html = template.render(context)
		result = open('/home/dvm/taruntest/oasis/%s.pdf' %((str(gl_id))+'_1'), 'wb')
		pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
		result.close()

		#normal pages now
		for x in range(2,no_of_pages):
			page_participants =  participants[(x-1)*20:x*20]
			page_no = str(x)
			display_page_participants = []
			for p in page_participants:
				name = p.name
				gender = p.gender[0].upper()
				events_list = [x.name for x in p.events.all()]
				if len(events_list) < 6:
					events = ','.join(events_list)
				else:
					events = ','.join(events_list[0:5]) + '...'
				display_page_participants.append((name,gender,events))
			template = get_template('nobarcode.html')
			context = Context({'display_page_participants':display_page_participants})
			html = template.render(context)
			result = open('/home/dvm/taruntest/oasis/%s.pdf' %((str(gl_id))+'_'+page_no), 'wb')
			pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
			result.close()
		#now the last page
		page_participants =  participants[(no_of_pages-1)*20:]
		display_page_participants = []
		for p in page_participants:
			name = p.name
			gender = p.gender[0].upper()
			events_list = [x.name for x in p.events.all()]
			if len(events_list) < 6:
				events = ','.join(events_list)
			else:
				events = ','.join(events_list[0:5]) + '...'
			display_page_participants.append((name,gender,events))
		barcode_name = '%s' % gl_id
		template = get_template('withbarcode.html')
		context = Context({'display_page_participants':display_page_participants,'encoded':encoded,'barcode_name':barcode_name})
		html = template.render(context)
		result = open('/home/dvm/taruntest/oasis/%s.pdf' %((str(gl_id))+'_'+str(no_of_pages)), 'wb')
		pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
		result.close()
		#now combining the pages
		output = pyPdf.PdfFileWriter()

		for x in range(1,no_of_pages+1):
			pdfDocument = '/home/dvm/taruntest/oasis/%s.pdf' %(str(gl_id)+'_'+str(x))
			input1 = pyPdf.PdfFileReader(file(pdfDocument, "rb"))
			for page in range(input1.getNumPages()):
				output.addPage(input1.getPage(page))

		outputStream = file('/home/dvm/taruntest/oasis/%s.pdf' %(str(gl_id)), 'wb')
		output.write(outputStream)
		outputStream.close()
	own_xls(gl_id)

@staff_member_required
def email_participant(request,gl_id):
	our_user = InitialRegistration.objects.get(id=gl_id)
	if our_user.user.is_active != False:
		return HttpResponse('This account has not been frozen yet.')
	send_to = str(our_user.email_id)
	college = str(our_user.college)
	participants = our_user.user.participant_set.all()
	no_of_males = len([x for x in participants if str(x.gender)[0].upper() == 'M'])
	no_of_females = len(participants)-no_of_males
	incharge = our_user.incharge
	body = unicode('''
Hello!

It is my pleasure to inform you that your college has been shortlisted to participate at Oasis'14 - That '90s Show. 

Please find attached to this mail the list of students from your college that have been confirmed. You must mail the bonafide certificates for all these students to pcr@bits-oasis.org before 11:59 pm on 29th October, 2014.

Remember - only these students and no-one else from your college shall be allowed to participate in Oasis'14-That '90s Show. 

Make sure that the subject of the above mail is of the format "<college name>- Bonafides" and the images/documents attached are titled "<college>-Bonafide" and so on.

For any queries regarding confirmation of participants, please contact your college in-charge : %s at +91 %s

While entering the campus, please ensure that you carry the following: 

	*  A hard-copy of the attached list of participants along with barcode at the end of it.
	*  Registration fee in the form of CASH / DD (in favor of "BITS Pilani" payable at UCO Bank, Pilani or ICICI Bank, Pilani or State Bank of Bikaner and Jaipur, Pilani).
	*  Original copy of the bona fide document which you will email to us (for more details, check the Security Details document).
	*  Valid college Identity Cards of every member in your group.
	*  Two passport size photographs of the Group Leader, and one of each of the participants.

Also, kindly let us know your Expected Time of Arrival (ETA) and Expected Time of Departure (ETD) for smoother registration on campus.

 

Also go through the attached set of documents - they include some strict guidelines to be followed at all times once on campus, along with some important information for a few events.
          
Please find attached the following files:-

1) List of Confirmed Participants
2) Security details
3) Sunburn details

We are glad to announce that BITS - Pilani will be having its very own Sunburn this Oasis. Kindly login to your GL account to pre-register for this extravaganza of electronic music and entertainment

Please acknowledge the receipt of this email at the earliest. 
We look forward to your participation in OASIS'14!
''' % (incharge.name.decode("utf8"),str(incharge.phone).decode("utf8")))
	attachment = '/home/dvm/taruntest/oasis/%s.pdf' % gl_id
	a_name = 'Oasis'+str(randint(9901,99000))
	shutil.copy2(attachment, '/home/dvm/taruntest/oasis/%s.pdf' % a_name)
	email = EmailMessage('CONFIRMATION for Oasis 2014', body, 'invitation@bits-oasis.org', [send_to])
	email.attach_file('/home/dvm/taruntest/oasis/%s.pdf' % a_name)
	email.attach_file('/home/dvm/taruntest/oasisattach/Department of Firewallz Instructions.pdf')
	email.attach_file('/home/dvm/taruntest/oasisattach/Oasis Bus Booking.pdf')
	email.attach_file('/home/dvm/taruntest/oasisattach/SB 1.jpg')
	email.send()
	#send_mail('BOSM 2014 Registration', 'Here is the message.', 'reachtarunhere@gmail.com',[send_to], fail_silently=False)
	return HttpResponse('mail sent')
@staff_member_required
def generate_pdf(request, gl_id):
	encoded = gen_barcode(gl_id)
	write_pdf(gl_id,encoded)
	return HttpResponse('generation sucessful')
@staff_member_required
def view_pdf(request, gl_id):
	#first generating
	encoded = gen_barcode(gl_id)
	write_pdf(gl_id,encoded)
	return serve(request, os.path.basename('/home/dvm/taruntest/oasis/%s.pdf' % gl_id), os.path.dirname('/home/dvm/taruntest/oasis/%s.pdf' % gl_id))
@staff_member_required
def pcr_act(request):
	big_list = InitialRegistration.objects.all()
	gleader_list = []
	for gl in big_list:
		if gl.user and len(gl.user.participant_set.all()):
			gleader_list.append(gl)
	context = RequestContext(request)
	context_dict = {'gleader_list':gleader_list}
	return render_to_response('pcract.html', context_dict, context)

def own_xls(gl_id):
	gl = InitialRegistration.objects.get(id=gl_id)
	participants = gl.user.participant_set.all()
	import xlwt
	book = xlwt.Workbook()
	sheet = book.add_sheet('Participant_sheet_full')
	style = xlwt.easyxf('font: name Sans-Serif, color-index blue, bold on')
	sheet.write(0,0,'Group Leader - ' + gl.name,style=style)
	sheet.write(0,2,'college - ' + gl.college,style=style)
	sheet.write(1,0,'Full Name',style = style)
	sheet.write(1,1,'Events',style=style)
	row=2
	for p in participants:
		sheet.write(row,0,p.name)
		eset=p.events.all()
		col=1
		for e in eset :
			sheet.write(row,col,e.name)
			col+=1
		row+=1
	import datetime
	today=datetime.date.today()
	f=open('/home/dvm/oasis/oasis2014/xls-data/%s.xls' %('confirmation '+str(today.strftime('%d-%m-%Y'))+' '+str(gl.id)+' '+gl.college),'wb')
	book.save(f)
	f.close()
	return
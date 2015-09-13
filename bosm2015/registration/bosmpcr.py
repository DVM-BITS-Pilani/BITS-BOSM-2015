from django.http import HttpResponse
from registration.models import *
from barg import code128_image
from django.template import Context
from django.shortcuts import get_object_or_404, render_to_response, render
#import GifImagePlugin
import sys
from django.template import RequestContext
from django.template.loader import get_template
from django.views.static import serve
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail, EmailMessage
import pyPdf
import string
from random import randint
import shutil
import pdfkit
import os
from django.views.decorators.csrf import csrf_exempt
sys.path.append('/home/dvm/taruntest/')
sys.path.append('/home/dvm/taruntest/bosm2015/')


def gen_barcode(gl_id):
	gl_ida = '0'*(4-len(str(gl_id)))+str(gl_id)
	mixed = string.ascii_uppercase + string.ascii_lowercase
	count = 51
	encoded = ''
	for x in gl_ida:
		encoded = encoded + x
		encoded = encoded + mixed[randint(0,51)]
#	gl_ida = '6'
	#image='/home/dvm/taruntest/%s.gif' % str(gl_id)
	image='/home/dvm/bosm/public_html/taruntest/satwik_bosmcode/%s.gif' % str(gl_id)
	code128_image(encoded).save(image)
	return encoded


def write_pdf(gl_id,encoded):
	gl = UserProfile.objects.get(id=gl_id)
	gl_name = gl.firstname + ' ' + gl.lastname
	participant_list = gl.user.participant_set.filter(confirmation=True)
	no_of_males = len([x for x in participant_list if str(x.gender) == 'M' or str(x.gender) == 'male'])
	no_of_females = len(participant_list)-no_of_males
	college = gl.college
	barcode_name = str(gl_id)+'.gif'
	plist_tab1 = []
	linear_list = []
	#linear_list = [((str(p.name ) + '    (' + str(p.gender)[0].upper() + ')'),str(p.events.all()[0].name)) for p in participant_list]
	for p in participant_list:
		x = str(p.name ) + '    (' + str(p.gender)[0].upper() + ')'
		if len(p.events.all()):
			# y = ",".join([x.name for x in p.events.all()])
			# y= p.events.all()[0].name
			if len(p.events.all()) < 5:
				y = ",".join([str(z.name) for z in p.events.all()])
			else:
				y = ",".join([str(z.name) for z in p.events.all()[:5]]) + '...'
		elif p.coach:
			y = 'Faculty in charge'
		else:
			y = ''
		linear_list.append((x,y))

	if len(linear_list)%2 != 0:
		linear_list.append(('',''))					#appending extra for symmetric table format

	glen = len(linear_list)

	if len(linear_list)<=50:						#implies every detail can fit in one page
		#template = get_template('pisatest.html')
		first_half = linear_list[:len(linear_list)/2]
		second_half = linear_list[len(linear_list)/2:]
		plist_tab = []										#participant list for tabular format
		for x in range(0,len(first_half)):
			plist_tab.append((first_half[x],second_half[x]))
		context = Context({'encoded':encoded,'plist_tab':plist_tab,'barcode_name':barcode_name})
		# html = template.render(context)
		# #result = open('/home/dvm/taruntest/%s.pdf' %(str(gl_id)), 'wb')
		# #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
		# #result.close()

		template = get_template('registration/singlepagebosm.html')
		html = template.render(context)
		text_file = open("/home/dvm/taruntest/apogee/output.html", "w")			#temporary only 
		text_file.write(html)
		text_file.close()
		pdfkit.from_file('/home/dvm/taruntest/apogee/output.html', '/home/dvm/taruntest/apogee/%s.pdf' %(str(gl_id)))

	else:
		tempo = linear_list
		if len(tempo)%2 != 0:
			tempo.append(' ', ' ')

		linear_list1 = tempo[:50]
		linear_list2 = tempo[50:]
		first_half = linear_list1[:len(linear_list1)/2]
		second_half = linear_list1[len(linear_list1)/2:]
		first_half1 = linear_list2[:len(linear_list2)/2]
		second_half1 = linear_list2[len(linear_list2)/2:]
		plist_tab = []
		plist_tab1 = []
		for x in range(0,len(first_half)):
			plist_tab.append((first_half[x],second_half[x]))
		for x in range(0,len(first_half1)):
			plist_tab1.append((first_half1[x],second_half1[x]))


		# if (len(plist_tab1)*2) != (glen - 50):
		# 	names = [x for x in participant_list]
		# 	gotnames = []
		# 	for z in plist_tab:
		# 		for k in z:
		# 			gotnames.append(str(k[0]))

		# 	for z in plist_tab1:
		# 		for k in z:
		# 			gotnames.append(str(k[0]))

		# 	for gtest in names:
		# 		for tname in gotnames
		# 		if gtest.name not in gotnames:
		# 			plist_tab1.append( ( (gtest.name, gtest.events.all()[0]), ('', '')) )
		template = get_template('registration/multipage_one.html')
		context = Context({'encoded':encoded,'plist_tab':plist_tab,'plist_tab1':plist_tab1,'barcode_name':barcode_name})
		# html = template.render(context)
		# result = open('/home/dvm/taruntest/%s_1.pdf' %(str(gl_id)), 'wb')
		# pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
		# result.close()
		html = template.render(context)
		text_file = open("/home/dvm/taruntest/apogee/output.html", "w")			#temporary only 
		text_file.write(html)
		text_file.close()
		pdfkit.from_file('/home/dvm/taruntest/apogee/output.html', '/home/dvm/taruntest/%s_1.pdf' %(str(gl_id)))


		template = get_template('registration/multipage_two.html')
		# html = template.render(context)
		# result = open('/home/dvm/taruntest/%s_2.pdf' %(str(gl_id)), 'wb')
		# pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
		# # result.close()
		html = template.render(context)
		text_file = open("/home/dvm/taruntest/apogee/output.html", "w")			#temporary only 
		text_file.write(html)
		text_file.close()
		pdfkit.from_file('/home/dvm/taruntest/apogee/output.html', '/home/dvm/taruntest/%s_2.pdf' %(str(gl_id)))


		output = pyPdf.PdfFileWriter()
		pdfDocument = '/home/dvm/taruntest/%s_1.pdf' %(str(gl_id))
		pdfDocument2 = '/home/dvm/taruntest/%s_2.pdf' %(str(gl_id))
		input1 = pyPdf.PdfFileReader(file(pdfDocument, "rb"))
		input2 = pyPdf.PdfFileReader(file(pdfDocument2, "rb"))
		for page in range(input1.getNumPages()):
			output.addPage(input1.getPage(page))
		for page in range(input2.getNumPages()):
			output.addPage(input2.getPage(page))
		outputStream = file('/home/dvm/taruntest/apogee/%s.pdf' %(str(gl_id)), 'wb')
		output.write(outputStream)
		outputStream.close()

	'''
	participant_list_formatted_n = [str(p.name ) for p in participant_list]
	participant_list_formatted_e = [str(p.events.all()[0].name) for p in participant_list]
	template_list1_n = participant_list_formatted_n[len(participant_list_formatted_n)/2:]
	template_list1_e = participant_list_formatted_e[len(participant_list_formatted_e)/2:]
	template_list2_n = participant_list_formatted_n[:len(participant_list_formatted_n)/2]
	template_list2_e = participant_list_formatted_e[:len(participant_list_formatted_e)/2]
	'''
	
	return html


def myview(request):
	z = write_pdf(44)
	gen_barcode(44)
	return HttpResponse(z)

#@staff_member_required
def pcr_pdf2(request,gl_id):
	id_list = gl_id
	for x in id_list:
		encoded = gen_barcode(x)
		write_pdf_2(x,encoded)
	return HttpResponse('operations completed for id %s' % gl_id)

def pcr_pdf(request, gl_id):
	encoded = gen_barcode(gl_id)
	write_pdf(gl_id,encoded)
#	return HttpResponse('operations completed for id %s' % gl_id)
	return serve(request, os.path.basename('/home/dvm/taruntest/%s.pdf' % gl_id), os.path.dirname('/home/dvm/taruntest/%s.pdf' % gl_id))
def email_participant2(request):
	id_list = [15, 21, 34, 39, 44, 46, 53, 55, 60, 65, 94, 106, 119, 127, 130, 132, 139, 141, 147, 148, 150, 158, 164, 165, 170, 188, 189, 198, 234, 265, 267, 268, 270, 298, 299] #gl_id list here
	s = ''
	for x in id_list:
		our_user = UserProfile.objects.get(id=x)
		send_to = str(our_user.user.email)
		college = str(our_user.college.name)
		body = ''' body here '''
		attachment = '/home/dvm/taruntest/%s.pdf' % x
		a_name = 'BOSM'+str(randint(9901,99000))
		shutil.copy2(attachment, '/home/dvm/taruntest/%s.pdf' % a_name)
		email = EmailMessage('BITS BOSM Barcode', body, 'reachtarunhere@gmail.com', [send_to])
		email.attach_file('/home/dvm/taruntest/%s.pdf' % a_name)
		email.send()
		s += str(x)+' '
	return HttpResponse(s)

def email_participant(request,gl_id):
	our_user = UserProfile.objects.get(id=gl_id)
	send_to = str(our_user.user.email)
	college = str(our_user.college)
	inchaarge = str(our_user.firstname+' '+our_user.lastname)
	if inchaarge is None:
		return HttpResponse("Please assign an incharge first")
#	participant_list = our_user.user.participant_set.all()
	user_ob = our_user.user
	participant_list = Participant.objects.filter(confirmation= True, gleader= user_ob)
	no_of_males = len([x for x in participant_list if str(x.gender) == 'male' or str(x.gender) == 'M'])
	no_of_females = len(participant_list)-no_of_males
	body = '''
Hello,

We are pleased to confirm your participation in BOSM 2015.

College : %s
Total no. of boys :%s
Total no. of girls : %s
College Incharge : %s

Please find attached the list of confirmed participants along with
their events, and note that only these participants will be allowed to
enter the campus.

To complete the registration, you must now send us a
bona fide document bearing the names of all confirmed students on the
official letterhead of your institution along with the signature of
your Dean/Principal. You can scan and email it to us at
pcr@bits-bosm.org

Please make sure that the subject of the mail is "Bonafide Certificates".
Please make sure that the document reaches us before 5:00 PM on
September 10, and do let us know when you send it.

*Make sure the caution deposit amount is given in cash.

On-campus registration will begin at 9:00 AM on September 18, and the
inauguration ceremony will commence from 5:00 PM on the same
day.Accommodation will be provided till 9:00 AM on September 23.
Please make your travel arrangements accordingly.

While entering the campus, please ensure that you carry-
 ENTRY WILL NOT BE ALLOWED WITHOUT THE FOLLOWING

* A printout of this email and the attached list of participants along with the barcode.
* An event-wise list of participants from your college (for instance,
all members in hockey, all members in football etc.)
* Original copy of the bona fide document that you will email to us
* Valid college ID cards for every member in your group
* One passport size photograph for each member in your group, and two
for the Group Leader

You will not be allowed to enter the campus without these documents
and ID cards.

Please acknowledge the receipt of this email at the earliest.

I look forward to your participation in BOSM 2015!

Regards,
Vinit Bhat
CoSSAcn (Head)
Dept. of Publications & Correspondence, BOSM 2015
BITS Pilani
Ph: +91 7240105157 / +91 9928086307
''' % (college,no_of_males,no_of_females,inchaarge+", "+str(our_user.phone))
	attachment = '/home/dvm/taruntest/apogee/%s.pdf' % gl_id
	a_name = 'BOSM'+str(randint(9901,99000))
	shutil.copy2(attachment, '/home/dvm/taruntest/apogee/%s.pdf' % a_name)
	email = EmailMessage('BITS BOSM', body, 'reachtarunhere@gmail.com', [send_to])
	email.attach_file('/home/dvm/taruntest/apogee/%s.pdf' % a_name)
	email.attach_file('/home/dvm/taruntest/apogee/BOSM_checklist.pdf')
	email.send()
	#send_mail('BOSM 2014 Registration', 'Here is the message.', 'reachtarunhere@gmail.com',[send_to], fail_silently=False)
	return HttpResponse('mail sent')

@staff_member_required
def generate_pdf(request, gl_id):
	our_participant = UserProfile.objects.get(id=gl_id)
	if not our_participant.barcode:
		encoded = gen_barcode(gl_id)
		our_participant.barcode = encoded
		our_participant.save()
	else:
		encoded = our_participant.barcode
	write_pdf(gl_id,encoded)
	return HttpResponse('generation sucessful')

@staff_member_required
def view_pdf(request, gl_id):
	#first generating
	our_participant = UserProfile.objects.get(id=gl_id)
	if not our_participant.barcode:
		encoded = gen_barcode(gl_id)
		our_participant.barcode = encoded
		our_participant.save()
	else:
		encoded = our_participant.barcode
	write_pdf(gl_id,encoded)
	return serve(request, os.path.basename('/home/dvm/taruntest/apogee/%s.pdf' % gl_id), os.path.dirname('/home/dvm/taruntest/apogee/%s.pdf' % gl_id))
@staff_member_required
def pcr_act(request):
	gleader_list = UserProfile.objects.all()
	# gleader_list = []
	# for gl in big_list:
	# 	if gl.user and len(gl.user.participant_set.all()):
	# 		gleader_list.append(gl)
	# gleader_list = gleader_list.order_by('-college')
	context = RequestContext(request)
	context_dict = {'gleader_list':gleader_list}
	return render_to_response('registration/pcract.html', context_dict, context)



@csrf_exempt
def get_pdf(request):
	if request.user.is_authenticated():
		try:
			our_participant = request.user.participant_set.all()[0]
		except:
			return HttpResponse('Invalid user')
	gl_id = our_participant.id
	if not our_participant.barcode:
		encoded = gen_barcode(gl_id)
		our_participant.barcode = encoded
		our_participant.save()
	else:
		encoded = our_participant.barcode
	write_pdf(gl_id,encoded)
	return serve(request, os.path.basename('/home/dvm/taruntest/apogee/%s.pdf' % gl_id), os.path.dirname('/home/dvm/taruntest/apogee/%s.pdf' % gl_id))



# def own_xls(gl_id):
# 	gl = InitialRegistration.objects.get(id=gl_id)
# 	participants = gl.user.participant_set.all()
# 	import xlwt
# 	book = xlwt.Workbook()
# 	sheet = book.add_sheet('Participant_sheet_full')
# 	style = xlwt.easyxf('font: name Sans-Serif, color-index blue, bold on')
# 	sheet.write(0,0,'Group Leader - ' + gl.firstname + ' ' + gl.lastname,style=style)
# 	sheet.write(0,2,'college - ' + gl.college,style=style)
# 	sheet.write(1,0,'Full Name',style = style)
# 	sheet.write(1,1,'Events',style=style)
# 	row=2
# 	for p in participants:
# 		sheet.write(row,0,p.name)
# 		eset=p.events.all()
# 		col=1
# 		for e in eset :
# 			sheet.write(row,col,e.name)
# 			col+=1
# 		row+=1
# 	import datetime
# 	today=datetime.date.today()
# 	f=open('/home/dvm/oasis/oasis2014/xls-data/%s.xls' %('confirmation '+str(today.strftime('%d-%m-%Y'))+' '+str(gl.id)+' '+gl.college),'wb')
# 	book.save(f)
# 	f.close()
# 	return

# def view_pdf(request):
# 	#first generating
# 	if request.POST:
# 		our_user = 
# 	our_participant = Participant.objects.get(id=gl_id)
# 	if not our_participant.barcode:
# 		encoded = gen_barcode(gl_id)
# 		our_participant.barcode = encoded
# 		our_participant.save()
# 	else:
# 		encoded = our_participant.barcode
# 	write_pdf(gl_id,encoded)
# 	return serve(request, os.path.basename('/home/dvm/taruntest/apogee/%s.pdf' % gl_id), os.path.dirname('/home/dvm/taruntest/apogee/%s.pdf' % gl_id))

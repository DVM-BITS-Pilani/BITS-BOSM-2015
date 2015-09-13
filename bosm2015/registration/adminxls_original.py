from registration.models import *
import xlwt
from django.http import *

#@staff_member_required
def participant_sheet(request):
  book = xlwt.Workbook()
  sheet = book.add_sheet('Participant_sheet_full')
  style = xlwt.easyxf('font: name Sans-Serif, color-index blue, bold on')
  sheet.write(0,0,'Name',style = style)
  sheet.write(0,1,'Group Leader Name',style = style)
  sheet.write(0,2,'Gender',style = style)
  sheet.write(0,3,'College',style = style)
  sheet.write(0,4,'City',style=style)
  sheet.write(0,5,'Contact',style = style)
  sheet.write(0,6,'Email',style=style)
  sheet.write(0,7,'Events',style = style)
 # sheet.write(0,8,'Username',style = style)

  row = 1
  us = Participant.objects.all()
  us = us.order_by('-gleader')
  for u in us:
    
    sheet.write(row,0,u.name)
    group=u.gleader
    if group is not None:
    	sheet.write(row,1,group.initialregistration_set.all()[0].name)
        profile=InitialRegistration.objects.filter(user=group)
        if len(profile)!=0:
		profile=profile[0]
        	sheet.write(row,3,profile.college)
        	sheet.write(row,4,profile.city)
    sheet.write(row,2,u.gender)
    sheet.write(row,5,str(u.phone))
    sheet.write(row,6,u.email_id)
    event=''
    for x in u.events.all():
	event=event+x.name+","
    sheet.write(row,7,event)
    row+=1
  response = HttpResponse(mimetype='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename=Users_all.xls'
  book.save(response)
  return response


from django.http import HttpResponse, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from events.models import EventNew

# Create your views here.
def geteventdata(request, event_id):
    try:
        eventid = event_id
    except :
        raise Http404
    try :
        event=EventNew.objects.get(pk=eventid)
    except ObjectDoesNotExist:
        raise Http404
    resp = {}
    resp['name']=unicode(event.name)
    # resp['category']=unicode(event.category.name)
    resp['content']=str(unicode(event.content))
    return JsonResponse(resp)
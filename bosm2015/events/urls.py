from events import views
from django.conf.urls import url
urlpatterns = [
    url(r'^(?P<event_id>[0-9]+)/$', views.geteventdata, name='get'),
]
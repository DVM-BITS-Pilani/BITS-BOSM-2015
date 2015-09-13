from pcradmin import views
from django.conf.urls import url, include
urlpatterns = [
    url(r'^(?P<pagename>\w+)/', views.index),
	#url(r'^sendmail$', views.sendmail),
	#url(r'^sentmail$', views.sentmail),
	url(r'^changelimit$', views.change_team_limits),
    url(r'^change_team_limit$', views.change_team_limit_list),
	url(r'^limit_changed$', views.change_limits),
	url(r'^changesportslimit$', views.change_sports_limits),
	url(r'^sports_limits_changed$', views.save_sports_limits),
    url(r'^setstatus', views.set_status),
    url(r'^showstatus', views.save_status),
    url(r'^emailsend', views.send_mail),
    url(r'^compose', views.compose),
	]

from django.conf.urls import include, url
from registration import views
teampatterns = [
    # url(r'^add$', views.register)
]

urlpatterns = [
    url(r'^register/$', views.user_register),
    url(r'^login/$', views.user_login, name='login'),
	url(r'^resetpassword/$', views.reset_password, name='reset_password'),
    url(r'^loginadmin/$', views.user_loginadmin, name='loginadmin'),
    url(r'^dashboard/$', views.user_dashboard, name='dashboard'),
    url(r'^sportview/$', views.user_sport_view, name='sport_view'),
    url(r'^rules/$', views.user_rules, name='rules'),
    # url(r'^participant/$', views.user_participant, name="participant"),
    url(r'^member/add/$', views.user_add, name='add'),   
    url(r'^member/edit/$', views.user_edit, name='edit'),
    url(r'^member/edit/detail/$', views.user_edit_detail, name='edit_detail'),
    url(r'^member/delete/$', views.user_delete, name='delete'),
    url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^addparticipant/$', views.add_participant),
    # url(r'^addcoach/$', views.add_coach),
    # url(r'^editparticipant/$', views.edit_participant_form),
    # url(r'^editparticipantcommit/$', views.edit_participant_commit),
    # url(r'^delparticipant/$', views.remove_participant),
    # url(r'^teamlist/$', views.team_list),
    # url(r'^team/$', include(teampatterns))
]

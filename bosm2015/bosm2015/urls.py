"""bosm2015 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from registration.bosmpcr import *
import events

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^event/', include('events.urls')),
    url(r'^pcradmin/', include('pcradmin.urls', namespace='pcradmin')),
    url(r'^accounts/', include('registration.urls', namespace='registration')),
    url(r'^gpdf/(?P<gl_id>\d+)/$', generate_pdf, name='generate pdf without viewing'),
    url(r'^vpdf/(?P<gl_id>\d+)/$', view_pdf, name='view and generate pdf'),
    url(r'^pcract/$', pcr_act, name='admin panel for the above'),
    url(r'^inviteconfirmation/(?P<gl_id>\d+)/$', email_participant, name='finally sending invites'),
    url(r'^regsoft/', include('regsoft.urls', namespace='regsoft') ),
]

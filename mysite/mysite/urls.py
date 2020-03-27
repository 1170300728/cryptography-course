"""mysite URL Configuration

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
from Eshop.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', mainpage, {'listtype':0}),
	url(r'^(\d)$', mainpage),
	url(r'^login/$', login, {'salenum':-1}),
	url(r'^login/([^/]+)$', login),
	url(r'^login/saleinfo/([^/]+)$', loginforcar),
	url(r'^logout/$', logout),
	url(r'^logged/$', mainpage, {'listtype':0}),
	url(r'^newaccount/$', newaccount),
	url(r'^reset/$', reset),
	url(r'^shoppingcar/([^/]+)$', toshoppingcar),
	url(r'^shoppingcar/$', shoppingcar),
	url(r'^userinfo/$', userinfo),
	url(r'^salesinfo/([^/]+)$', salesinfo),
	url(r'^salesinfo/([^/]+)/carred$', addtocar),
	url(r'^newaddress/([^/]+)$', newaddress, {'flag':0, 'fromuserinfo':'0'}),
	url(r'^newaddress/(?P<sqe>[^/]+)/(?P<flag>[^/]+)$', newaddress, {'fromuserinfo':'0'}),
	url(r'^newaddress/(?P<sqe>[^/]+)/(?P<flag>[^/]+)/(?P<fromuserinfo>.+)/$', newaddress),
	url(r'^deladdress/([^/]+)/([^/]+)$', deladdress),
	url(r'^editaddress/([^/]+)/([^/]+)$', editaddress),
	url(r'^order/$', order, {'addrarg':'0'}),
	url(r'^order/([^/]+)$', order),
	url(r'^delete/([^/]+)$', delete),
	url(r'^alter/([^/]+)$', alter),
	url(r'^add/([^/]+)/([^/]+)/([^/]+)/$', add),
	url(r'^newpassword/([^/]+)/([^/]+)/$', newpassword),
	url(r'^finishpay/([^/]+)/([^/]+)/(.+)', finishpay),
	url(r'^continue/(?P<para>.+)', continuefunction, {'addrarg':'0'}),
	url(r'^(\d+)/continue/(.+)', continuefunction),
	url(r'^dualsignature/$', dualsignature),
]

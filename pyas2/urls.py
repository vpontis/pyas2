from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test
from pyas2 import views

staff_required = user_passes_test(lambda u: u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_superuser)

urlpatterns = patterns('',
    url(r'^login.*', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='login'),
    url(r'^logout.*', 'django.contrib.auth.views.logout',{'next_page': 'home'}, name='logout'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',name='password_change_done'),
    url(r'^home.*', login_required(views.home, login_url='login'), name='home'),
    url(r'^msearch/$', login_required(views.MessageSearch.as_view(), login_url='login'), name='msearch'),
    url(r'^message/$', login_required(views.MessageList.as_view(), login_url='login'), name='messages'),
    url(r'^message/(?P<pk>.+)/$', login_required(views.MessageDetail.as_view(), login_url='login'), name='message_detail'),
    url(r'^payload/(?P<pk>.+)/$', login_required(views.PayloadView.as_view(), login_url='login'), name='payload_view'),
    url(r'^mdnsearch/$', login_required(views.MDNSearch.as_view(), login_url='login'), name='mdnsearch'),
    url(r'^mdn/$', login_required(views.MDNList.as_view(), login_url='login'), name='mdns'),
    url(r'^mdn/(?P<pk>.+)/$', login_required(views.MDNView.as_view(), login_url='login'), name='mdn_view'),
    url(r'^sendmessage/$', login_required(views.SendMessage.as_view(), login_url='login'), name='sendmessage'),
    url(r'^resendmessage/(?P<pk>.+)/$', login_required(views.resendmessage, login_url='login'), name='resendmessage'),
    url(r'^sendasyncmdn/$', login_required(views.sendasyncmdn, login_url='login'), name='sendasyncmdn'),
    url(r'^retryfailedcomms/$', login_required(views.retryfailedcomms, login_url='login'), name='retryfailedcomms'),
    url(r'^cancelretries/(?P<pk>.+)/$', login_required(views.cancelretries, login_url='login'), name='cancelretries'),
    #only superuser
    url(r'^sendtestmail$', superuser_required(views.sendtestmailmanagers), name='sendtestmail'), 
    # as2 asynchronous mdn and message receive url
    url(r'^as2receive$', views.as2receive, name="as2-receive"),
    #catch-all
    url(r'^.*', login_required(views.home, login_url='login'), name='home'),
)


from django.conf.urls import url
from django.contrib.auth import views as auth_views
#project
from ourAuth.views import *

urlpatterns = [
    url(r'^$', home, name='homeAuth'),
    url(r'^login/$', auth_views.login, {'template_name': 'ourAuth/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^manage_address/$', ManageAddress.as_view(), name='ManageAddress'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    ## RESET PASSWORD
    url(r'^password/reset/$',
        auth_views.password_reset,
        {
            'post_reset_redirect': 'password_reset_done',
            'template_name': 'password/password_reset_form.html',
            'email_template_name': 'password/password_reset_email.html',
            'subject_template_name': 'password/password_reset_subject.txt',
            'from_email':'equipo@RIA.com'
        },
        name="password_reset"
    ),
    url(
        r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'password/password_reset_done.html'},
        name="password_reset_done"
    ),
    url(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'post_reset_redirect': 'password_done',
            'template_name': 'password/password_reset_confirm.html'
        },
        name="password_reset_confirm"
    ),
    url(
        r'^password/done/$',
        auth_views.password_reset_complete,
        {'template_name': 'password/password_reset_complete.html'},
        name='password_done'
    ),

    url(r'^password/change$', change_password, name='change_password'),
]
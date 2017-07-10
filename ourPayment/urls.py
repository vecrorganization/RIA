from django.conf.urls import url
from ourPayment.views import *

urlpatterns = [
    url(r'^mptest/$', MPTest, name='MPTest'),
]
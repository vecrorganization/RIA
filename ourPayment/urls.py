from django.conf.urls import url
from ourWeb.views import *

from ourPayment.views import MPTest

urlpatterns = [
    url(r'^mptest/$', MPTest, name='MPTest'),
]
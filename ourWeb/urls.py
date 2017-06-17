from django.conf.urls import url
from ourWeb.views import *

urlpatterns = [
    url(r'^$', home, name='home'),
]
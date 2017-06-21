from django.conf.urls import url
from ourWeb.views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^prodorderadd_ajax/$', ProdOrderAddUpdate.as_view(), name='ProdOrderAddUpdate'),
    url(r'^prodorderdelete_ajax/$', ProdOrderDelete.as_view(), name='ProdOrderDelete'),
    url(r'^prodshow/$', ProdShow.as_view(), name='ProdShow'),
    url(r'^userorder/$', OrderUserShow.as_view(), name='OrderUserShow'),
]
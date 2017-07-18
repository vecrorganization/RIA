from django.conf.urls import url
from ourWeb.views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    
    url(r'^products/$', Products.as_view(), name='Products'),
    url(r'^prod_detail/(?P<pk>[-\w]+)/$', ProdDetail.as_view(), name='ProdDetail'),

    url(r'^userorder/$', OrderUserShow.as_view(), name='OrderUserShow'),
    url(r'^prod_add_ajax/$', ProdOrderAdd.as_view(), name='ProdOrderAdd'),
    url(r'^prod_update_ajax/$', ProdOrderUpdate.as_view(), name='ProdOrderUpdate'),
    url(r'^prod_delete_ajax/$', ProdOrderDelete.as_view(), name='ProdOrderDelete'),
]
from django.conf.urls import url
from ourAdmin.views import *

urlpatterns = [
	# PROD
    url(r'^prodsearch/$', ProdSearch.as_view(), name='ProdSearch'),
    url(r'^prodsearchajax/$', ProdSearchAjax.as_view(), name='ProdSearchAjax'),
	url(r'^prodcreate/$', ProdCreateModify.as_view(), name='ProdCreate'),
    url(r'^prodmodify/(?P<pk>\d+)/$', ProdCreateModify.as_view(), name='ProdModify'),
]
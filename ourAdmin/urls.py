from django.conf.urls import url
from ourAdmin.views import *

urlpatterns = [
	# PROD
    url(r'^prodsearch/$', ProdSearch.as_view(), name='ProdSearch'),
    url(r'^prodsearchajax/$', ProdSearchAjax.as_view(), name='ProdSearchAjax'),
    url(r'^proddeleteajax/$', ProdDeleteAjax.as_view(), name='ProdDeleteAjax'),
	url(r'^prodcreate/$', ProdCreateModify.as_view(), name='ProdCreate'),
    url(r'^prodmodify/(?P<pk>\d+)/$', ProdCreateModify.as_view(), name='ProdModify'),
	# TABLE
    url(r'^tablesearch/$', TableSearch.as_view(), name='TableSearch'),
    url(r'^tablesearchajax/$', TableSearchAjax.as_view(), name='TableSearchAjax'),
	url(r'^tablecreate/$', TableCreateModify.as_view(), name='TableCreate'),
    url(r'^tabledeleteajax/$', TableDeleteAjax.as_view(), name='TableDeleteAjax'),
    url(r'^tablemodify/(?P<pk>\d+)/$', TableCreateModify.as_view(), name='TableModify'),
]
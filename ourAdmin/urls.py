from django.conf.urls import url
from ourAdmin.views import *

urlpatterns = [
    url(r'^$', Home.as_view(), name='ourAdmin'),
	# PROD
    url(r'^prodsearch/$', ProdSearch.as_view(), name='ProdSearch'),
	url(r'^prodcreate/$', ProdCreateModify.as_view(), name='ProdCreate'),
    url(r'^prodmodify/(?P<pk>[-\w]+)/$', ProdCreateModify.as_view(), name='ProdModify'),
    url(r'^prodsearchajax/$', ProdSearchAjax.as_view(), name='ProdSearchAjax'),
    url(r'^proddeleteajax/$', ProdDeleteAjax.as_view(), name='ProdDeleteAjax'),
	# TABLE
    url(r'^tablesearch/$', TableSearch.as_view(), name='TableSearch'),
    url(r'^tablesearchajax/$', TableSearchAjax.as_view(), name='TableSearchAjax'),
	url(r'^tablecreate/$', TableCreateModify.as_view(), name='TableCreate'),
    url(r'^tabledeleteajax/$', TableDeleteAjax.as_view(), name='TableDeleteAjax'),
    url(r'^tablemodify/(?P<pk>\d+)/$', TableCreateModify.as_view(), name='TableModify'),
    # ORDER
    url(r'^ordersearch/$', OrderSearch.as_view(), name='OrderSearch'),
    url(r'^ordersearchajax/$', OrderSearchAjax.as_view(), name='OrderSearchAjax'),
    # ADDRESS
    url(r'^address_search/$', AddressSearch.as_view(), name='AddressSearch'),
    url(r'^address_searchajax/$', AddressSearchAjax.as_view(), name='AddressSearchAjax'),
    url(r'^addresscreate/$', AddressCreateModify.as_view(), name='AddressCreate'),
    url(r'^addressdeleteajax/$', AddressDeleteAjax.as_view(), name='AddressDeleteAjax'),
    url(r'^addressmodify/(?P<pk>\d+)/$', AddressCreateModify.as_view(), name='AddressModify'),
    # PAYMENT
    url(r'^paymentsearch/$', PaymentSearch.as_view(), name='PaymentSearch'),
    url(r'^paymentsearchajax/$', PaymentAjax.as_view(), name='PaymentSearchAjax'),
    url(r'^MP_payments/$', MPPayments.as_view(), name='MPPayments'),
    url(r'^MP_payment/(?P<pk>\d+)/$', MPPaymentData.as_view(), name='MPPaymentData'),
]
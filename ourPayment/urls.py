from django.conf.urls import url
from ourPayment.views import *

urlpatterns = [
    #Summary
    url(r'^purchase_summary/$', PurchaseSummary.as_view(), name='PurchaseSummary'),
    #Address
    url(r'^new_address/$', PaymentAddress.as_view(), name='NewAddress'),
    url(r'^edit_address/(?P<pk>\d+)/$', PaymentAddress.as_view(), name='EditAddress'),
    #Pay
    url(r'^pay/(?P<pk>\d+)/$', PayMp.as_view(), name='PayMp'),
    #IPN (Notificaciones de pago)
    url(r'^ipn/$', IpnMP, name='IpnMP'),
    url(r'^success/$', SuccessMP.as_view(), name='SuccessMP'),
    url(r'^pending/$', PendingMP, name='PendingMP'),
]
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
#from django.contrib import admin

urlpatterns = [
    ## Our Web module's URLs
    url(r'^', include('ourWeb.urls'), name='ourWebApp'),
    ## Our Admin module's URLs
    url(r'^ourAdmin/', include('ourAdmin.urls'), name='ourAdminApp'),
    ## Our Auth module's URLs
    url(r'^accounts/', include('ourAuth.urls'), name='ourAuthApp'),
    ## Our Payment module's URLs
    url(r'^payment/', include('ourPayment.urls'), name='ourPaymentApp'),    
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    (r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
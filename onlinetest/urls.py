from django.conf.urls import url
from TcsProject import settings
from . import views
from django.conf.urls.static import static


app_name = 'onlinetest' 
#This sets application namespace to diffretiate urls of different apps.

urlpatterns = [
    #url for home-page:
    url(r'^$', views.index, name='index'),
    #url for login-page:
    url(r'^studentlogin$', views.studentlogin, name='studentlogin'),
    url(r'^clientlogin$', views.clientlogin, name='clientlogin'),
    #url for signup-page:
    url(r'^clientregister$', views.clientregister, name='clientregister'),
    url(r'^(?P<test_id>[0-9]+)/$', views.clientadmin, name='clientadmin'),
    url(r'^addtest$', views.addtest, name='addtest'),
    url(r'^(?P<test_id>[0-9]+)/deletetest/$', views.deletetest, name='deletetest'),
    url(r'^testIdVal$', views.testIdVal, name='testIdVal'),
    url(r'^studentLogincheck$', views.studentLogincheck, name='studentLogincheck'),
    url(r'^studenthome$', views.studenthome, name='studenthome'),
    url(r'^yourtest$', views.yourtest, name='yourtest'),
    url(r'^studentInfo', views.studentInfo, name='studentInfo'),
    url(r'^clientlogout', views.clientlogout, name='clientlogout'),
    url(r'^paper_submit$',views.paper_submit, name='paper_submit'),
    url(r'^studentmarksdisplay$',views.studentmarksdisplay, name='studentmarksdisplay'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

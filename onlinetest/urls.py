from django.conf.urls import url
from TcsProject import settings
from . import views
from django.conf.urls.static import static


app_name = 'onlinetest' 

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^trytest$', views.trytest, name='trytest'),
    url(r'^studentlogin$', views.studentlogin, name='studentlogin'),
    url(r'^clientlogin$', views.clientlogin, name='clientlogin'),
    url(r'^clientloginVal$', views.clientloginVal, name='clientloginVal'),
    url(r'^clientregister$', views.clientregister, name='clientregister'),
    url(r'^adminhome$', views.adminhome, name='adminhome'),
    url(r'^home$', views.home, name='home'),
    url(r'^studentReg$', views.studentReg, name='studentReg'),
    url(r'^addtest$', views.addtest, name='addtest'),
    url(r'^(?P<test_id>[0-9]+)/deletetest/$', views.deletetest, name='deletetest'),
    url(r'^studentLogincheck$', views.studentLogincheck, name='studentLogincheck'),
    url(r'^studenthome$', views.studenthome, name='studenthome'),
    url(r'^yourtest$', views.yourtest, name='yourtest'),
    url(r'^studentRegSave', views.studentRegSave, name='studentRegSave'),
    url(r'^studentInfo', views.studentInfo, name='studentInfo'),
    url(r'^clientlogout', views.clientlogout, name='clientlogout'),
    url(r'^studentmarksAnalysis', views.studentmarksAnalysis, name='studentmarksAnalysis'),
    url(r'^studentlogout', views.studentlogout, name='studentlogout'),
    url(r'^simple_upload', views.simple_upload, name='simple_upload'),
    url(r'^paper_submit$',views.paper_submit, name='paper_submit'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import patterns, url, include

from BajarCaja import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^upload_file/$',views.upload_file,name='upload_file'),
    url(r'^show_files/$',views.show_files,name='show_files'),
    url(r'^download_file/(?P<file_id>\d+)$',views.download_file,name='download_file'),
    url(r'^swap_public/$',views.swap_public,name='swap_public'),
    url(r'^delete_file/(?P<file_id>\d+)$',views.delete_file,name='delete_file'),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^register/$', views.register, name='register')

)
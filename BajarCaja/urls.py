from django.conf.urls import patterns, url

from BajarCaja import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^upload_file/',views.upload_file,name='upload_file'),
    url(r'^view_files/',views.view_files,name='view_files'),
)
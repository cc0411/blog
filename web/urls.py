from django.conf.urls import url
from web import views

urlpatterns = [
    url(r'^upload_file.html$', views.upload_file),
    url(r'^manager_file.html$', views.manager_file),


]
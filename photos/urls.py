from django.conf.urls import url


from .views import *


app_name = 'photos'


urlpatterns = [
    url(r'^delete_comment/(?P<pk>[0-9]+)/$', delete_comment, name='delete_comment'),
    url(r'^create_comment/(?P<pk>[0-9]+)/$', create_comment, name='create_comment'),
    url(r'^view_photo/(?P<pk>[0-9]+)/$', view_photo, name='view_photo'),
    url(r'^delete_photo/(?P<pk>[0-9]+)/$', delete_photo, name='delete_photo'),
    url(r'^create_photo/$', create_photo, name='create_photo'),
    url(r'^$', list_photos, name='list_photos'),
]
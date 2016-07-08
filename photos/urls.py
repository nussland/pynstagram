from django.conf.urls import url
from django.contrib.auth.decorators import login_required


from . import views


app_name = 'photos'


urlpatterns = [
    url(r'^view_photo/(?P<pk>[0-9]+)/$', views.PhotoView.as_view(), name='view_photo'),

    url(r'^delete_photo/(?P<pk>[0-9]+)/$', login_required(views.PhotoDelete.as_view()), name='delete_photo'),

    url(r'^create_photo/$', login_required(views.PhotoCreate.as_view()), name='create_photo'),

    url(r'^list_photos/$', views.PhotoList.as_view(), name='list_photos'),

    url(r'^$', views.PhotoList.as_view(), name='default'),
]
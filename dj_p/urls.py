from django.conf.urls import url
from dj_p import views


urlpatterns = [
    url(r'^dj_p/$', views.post, name="dj_p"),
    url(r'^list/$', views.post_list, name="list"),
    url(r'^detail/(?P<post_slug>[-\w]+)/$', views.post_detail, name="detail"),
    url(r'^create/$',views.post_create, name="create"),
    url(r'^update/(?P<post_slug>[-\w]+)/$', views.post_update, name="update"),
    url(r'^delete/(?P<post_slug>[-\w]+)/$', views.post_delete, name="delete"),
]

from django.conf.urls import url
from dj_p import views


urlpatterns = [
    url(r'^dj_p/$', views.post, name="dj_p"),
    url(r'^list/$', views.post_list, name="list"),
    url(r'^detail/(?P<post_id>\d+)/$', views.post_detail, name="detail"),
]

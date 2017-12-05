from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^place/search/$', views.place_text_search, name="place_search"),
    url(r'^place/detail/$', views.place_detail, name="place_detail"),
]
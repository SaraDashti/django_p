from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^twitter/$', views.tweet_search, name="twitter"),
   
]
"""django_p URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^more/', include('dj_p.urls')),
]

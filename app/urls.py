from django.conf.urls import url, include

from app.views import *

urlpatterns = [
    url(r'v1.0/', include([
        url(r'index/$', index, name='index'),
    ]))
]

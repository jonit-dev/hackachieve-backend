
from django.conf.urls import url, include
from django.contrib import admin

from .apiUrls import urlpatterns as api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include(api_urls)),


]

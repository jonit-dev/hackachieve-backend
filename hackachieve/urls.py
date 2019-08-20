from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apiUrls import urlpatterns as api_urls

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include(api_urls)),
    url('api-auth/', include('rest_framework.urls')),
    url('api/token/', TokenObtainPairView.as_view()),
    url('api/token/refresh/', TokenRefreshView.as_view())
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
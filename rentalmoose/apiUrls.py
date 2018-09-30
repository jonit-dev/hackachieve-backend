from django.conf.urls import url, include

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('provinces', views.ProvinceView)
router.register('cities', views.CityView)
router.register('resumes', views.ResumeView)
router.register('countries', views.CountryView)

urlpatterns = [

    url('', include(router.urls)),
    url('user/create', views.user_register)

]

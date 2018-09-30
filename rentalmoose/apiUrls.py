from django.conf.urls import url, include

from . import views
from rest_framework import routers

from apps.users import views as user_views

router = routers.DefaultRouter()
router.register('provinces', views.ProvinceView)
router.register('cities', views.CityView)
router.register('resumes', views.ResumeView)
router.register('countries', views.CountryView)




urlpatterns = [

    url('', include(router.urls)),
    url('user/create', user_views.user_register),
    url('user/dashboard', user_views.user_dashboard)

]

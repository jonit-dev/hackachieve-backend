from django.conf.urls import url, include

from . import views
from rest_framework import routers

from apps.users import views as user_views
from apps.provinces import views as provinces_views
from apps.properties import views as properties_view

router = routers.DefaultRouter()
router.register('properties', views.PropertyView)
router.register('provinces', views.ProvinceView)
router.register('cities', views.CityView)
router.register('resumes', views.ResumeView)
router.register('countries', views.CountryView)

urlpatterns = [

    url('', include(router.urls)),
    url('user/create', user_views.user_register),
    url('user/resume/create', user_views.resume_create),
    url('user/dashboard', user_views.user_dashboard),
    url(r'^province/(?P<id>[0-9]+)/cities$', provinces_views.provinces_cities),

    url(r'^properties/create$', properties_view.create),

]

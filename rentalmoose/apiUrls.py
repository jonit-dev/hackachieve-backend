from django.conf.urls import url, include

from . import views
from rest_framework import routers

from apps.users import views as user_views
from apps.provinces import views as provinces_views
from apps.properties import views as properties_view
from apps.neighborhoods import views as neighborhoods_view
from apps.requests import views as requests_view

router = routers.DefaultRouter()
router.register('properties', views.PropertyView)
router.register('provinces', views.ProvinceView)
router.register('cities', views.CityView)
router.register('resumes', views.ResumeView)
router.register('countries', views.CountryView)

urlpatterns = [

    url('', include(router.urls)),

    # USER ROUTES =========================== #

    url('user/info', user_views.user_info),
    url('user/create', user_views.user_register),
    url('user/resume/create', user_views.resume_create),
    url('user/dashboard', user_views.user_dashboard),
    url('user/apply/(?P<property_id>[0-9]+)', user_views.user_apply),

    # PROVINCES =========================== #

    url(r'^province/(?P<id>[0-9]+)/cities$', provinces_views.provinces_cities),

    # NEIGHBORHOODS from specific city=========================== #
    url(r'^(?P<city_id>[0-9]+)/neighborhoods/(?P<keyword>[\w\-]+)/$', neighborhoods_view.fetch_neighborhoods),

    url(r'^(?P<city_id>[0-9]+)/has-neighborhoods',neighborhoods_view.has_neighborhoods),


    # PROPERTIES ROUTES (REAL ESTATE LISTINGS) =========================== #

    url(r'^properties/create$', properties_view.create),
    url(r'^properties/show/dashboard', properties_view.show_dashboard),
    url(r'^properties/(?P<id>[0-9]+)', properties_view.show),



    #FETCH ALL PROPERTIES THAT SOME PARTICULAR LANDLORD OWNS
    url(r'^property/landlord', properties_view.properties_listing),


    #FETCH ALL APPLICANTS FROM SPECIFIC APPLICATION
    url(r'^property/(?P<property_id>[0-9]+)/applications', properties_view.applications),

    #FETCH ONLY ONE APPLICANT FROM APPLICATION
    url(r'^property/(?P<property_id>[0-9]+)/applicant/(?P<applicant_id>[0-9]+)', properties_view.applicant_info),


    # ================================================================= #
    #                      EXTERNAL REQUISITIONS (APIs)
    # ================================================================= #

    url(r'^walkscore/(?P<address>[\w\-]+)/(?P<lat>[0-9]+)/(?P<lng>[0-9]+)', requests_view.walkscore),

]

from django.conf.urls import url, include

from . import views
from rest_framework import routers


# Views =========================== #
from apps.users import views as user_views
from apps.provinces import views as provinces_views  # function based serializer
from apps.provinces.api import views as api_provinces_view  # class based serializer
from apps.properties import views as properties_view  # function based serializer
from apps.properties.api import views as api_properties_view  # class based serializer
from apps.property_types import views as properties_types_view
from apps.cities.api import views as api_cities_view
from apps.countries.api import views as api_countries_view
from apps.neighborhoods import views as neighborhoods_view
from apps.requests import views as requests_view
from apps.tests import views as tests_view
from apps.places import views as places_view

router = routers.DefaultRouter()
router.register('properties', api_properties_view.PropertyView)
router.register('provinces', api_provinces_view.ProvinceView)
router.register('cities', api_cities_view.CityView)
router.register('countries', api_countries_view.CountryView)

urlpatterns = [

    url('', include(router.urls)),

    # USER ROUTES =========================== #


    url('user/info', user_views.user_info),
    url('user/create', user_views.user_register),
    url('user/resume/create', user_views.resume_create),
    url('user/dashboard', user_views.user_dashboard),
    url('user/apply/(?P<property_id>[0-9]+)', user_views.user_apply),

    # PROVINCES =========================== #

    url(r'^provinces/(?P<id>[0-9]+)/cities$', provinces_views.provinces_cities),

    # NEIGHBORHOODS from specific city=========================== #
    url(r'^(?P<city_id>[0-9]+)/neighborhoods/(?P<keyword>[\w\-]+)/$', neighborhoods_view.fetch_neighborhoods),
    url(r'^places/(?P<keyword>[\w\-]+)/$', places_view.fetch_places),

    url(r'^(?P<city_id>[0-9]+)/has-neighborhoods', neighborhoods_view.has_neighborhoods),

    # PROPERTIES ROUTES (REAL ESTATE LISTINGS) =========================== #

    url(r'^properties/create$', properties_view.create),
    url(r'^properties/show/dashboard', properties_view.show_dashboard),
    # url(r'^properties/(?P<id>[0-9]+)', properties_view.show),
    url(r'^properties/types', properties_types_view.fetch_types),

    # FETCH ALL PROPERTIES THAT SOME PARTICULAR LANDLORD OWNS
    url(r'^property/landlord', properties_view.properties_listing),

    # FETCH ALL APPLICANTS FROM SPECIFIC APPLICATION
    url(r'^property/(?P<property_id>[0-9]+)/applications', properties_view.applications),

    # FETCH ONLY ONE APPLICANT FROM APPLICATION
    url(r'^property/(?P<property_id>[0-9]+)/applicant/(?P<applicant_id>[0-9]+)', properties_view.applicant_info),

    # ================================================================= #
    #                      EXTERNAL REQUISITIONS (APIs)
    # ================================================================= #

    url(r'^walkscore/(?P<address>[\w|\W]+)/(?P<lat>-?\d+.?\d+)/(?P<lng>-?\d+.?\d+)', requests_view.walkscore),

    # url(r'^test/email/threading', tests_view.email_threading),
    # url(r'^test/ip', tests_view.ipcheck),
    # url(r'^test/phone', tests_view.phonecheck),
    # url(r'^test/mailchimp', tests_view.mailchimp),

    url(r'^prerender/property/(?P<property_id>[0-9]+)', properties_view.prerender),

]

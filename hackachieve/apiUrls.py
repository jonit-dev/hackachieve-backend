from django.conf.urls import url, include
from rest_framework import routers

# Views =========================== #
from apps.provinces.api import views as api_provinces_view  # class based serializer
from apps.cities.api import views as api_cities_view
from apps.countries.api import views as api_countries_view
from apps.users import views as user_views

router = routers.DefaultRouter()

router.register('provinces', api_provinces_view.ProvinceView)
router.register('cities', api_cities_view.CityView)
router.register('countries', api_countries_view.CountryView)

urlpatterns = [

    url('', include(router.urls)),

    # USER ROUTES =========================== #

    url('user/register', user_views.user_register),

]

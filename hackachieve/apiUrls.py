from django.conf.urls import url, include
from rest_framework import routers

# Views =========================== #
from apps.provinces.api import views as api_provinces_view  # class based serializer
from apps.cities.api import views as api_cities_view
from apps.countries.api import views as api_countries_view
from apps.users import views as user_views

from apps.boards import views as board_views

router = routers.DefaultRouter()
router.register('provinces', api_provinces_view.ProvinceView)
router.register('cities', api_cities_view.CityView)
router.register('countries', api_countries_view.CountryView)

urlpatterns = [

    url('', include(router.urls)),

    # USER ROUTES =========================== #

    url('user/register', user_views.user_register),

    # Boards

    url(r'^boards/create$', board_views.create_board),
    url(r'^boards/$', board_views.show_all_boards),
    url(r'^boards/show/(?P<board_id>[0-9]+)/$', board_views.show_board),
    url(r'^boards/delete/(?P<board_id>[0-9]+)/$', board_views.delete_board),

]

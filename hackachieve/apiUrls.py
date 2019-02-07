from django.conf.urls import url, include
from rest_framework import routers

# Views =========================== #
from apps.provinces.api import views as api_provinces_view  # class based serializer
from apps.cities.api import views as api_cities_view
from apps.countries.api import views as api_countries_view
from apps.users import views as user_views

from apps.boards import views as board_views
from apps.columns import views as column_views
from apps.goals import views as goal_views
from apps.users_goals_categories import views as categories_views

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
    url(r'^boards/attach/goals/$', board_views.attach_to_goal),
    url(r'^boards/(?P<board_id>[0-9]+)/goals/$', board_views.show_goals),
    # list of goals associated with a particular board

    # columns
    url(r'^columns/create/$', column_views.create),
    url(r'^columns/board/(?P<board_id>[0-9]+)/$', column_views.show_columns_from_board),
    # show all columns from a particular board
    url(r'^columns/delete/(?P<column_id>[0-9]+)/$', column_views.delete),

    # goals
    url(r'^goals/create/$', goal_views.create),
    url(r'^goals/delete/(?P<goal_id>[0-9]+)/$', goal_views.delete),
    url(r'^goals/attach/columns/$', goal_views.attach_to_column),
    url(r'^goals/show/(?P<goal_id>[0-9]+)/$', goal_views.show),
    url(r'^goals/long-short/(?P<goal_id>[0-9]+)/$', goal_views.long_short),
    # fetch list of short term goals associated with a long term one

    # categories
    url(r'^categories/create$', categories_views.create),
    url(r'^categories/delete/(?P<category_id>[0-9]+)/$', categories_views.delete),
    url(r'^categories/attach/goals', categories_views.attach),

]
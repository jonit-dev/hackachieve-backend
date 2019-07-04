from django.conf.urls import url, include
from rest_framework import routers

# Views =========================== #
from apps.columns.views import UpdateColumnViewSets
from apps.countries.api import views as api_countries_view
from apps.goals.views import GoalFeedsViewSet, PublicGoalUpdateView, OrderUpdateGoalView
from apps.goals.views import GoalFeedsViewSet, PublicGoalUpdateView, CommentPublicGoal, CommentVoteViewset
from apps.projects.views import ProjectViewSet
from apps.users import views as user_views
from apps.labels import views as labels_view
from apps.boards import views as board_views
from apps.columns import views as column_views
from apps.goals import views as goal_views
from apps.area_of_knowledges import views as aok_views


router = routers.SimpleRouter()
router.register(r'goals/comment', CommentPublicGoal)
router.register(r'goals/comment-vote', CommentVoteViewset)
router.register(r'project', ProjectViewSet)
urlpatterns = router.urls

urlpatterns += [

    # DRF SERIALIZED BASED ROUTES =========================== #
    url('', include('apps.checklists.api.urls')),
    url('', include('apps.area_of_knowledges.api.urls')),
    url('', include('apps.labels.api.urls')),



    # USER ROUTES =========================== #

    url('user/register', user_views.user_register),
    url('user/info/$', user_views.info),

    # Boards

    url(r'^boards/create/$', board_views.create_board),
    url(r'^boards/$', board_views.show_all_boards),
    url(r'^boards/show/(?P<board_id>[0-9]+)/(?P<goal_type>[a-zA-z]+)$', board_views.show_board),
    url(r'^boards/delete/(?P<board_id>[0-9]+)/$', board_views.delete_board),
    # list of goals associated with a particular board

    # columns
    url(r'^columns/update-order/(?P<pk>[0-9]+)/$', UpdateColumnViewSets.as_view()),
    url(r'^columns/create/$', column_views.create),
    url(r'^columns/update/(?P<column_id>[0-9]+)/$', column_views.update),

    url(r'^columns/board/(?P<board_id>[0-9]+)/$', column_views.show_columns_from_board),
    # show all columns from a particular board
    url(r'^columns/delete/(?P<column_id>[0-9]+)/$', column_views.delete),
    url(r'^columns/attach-category/(?P<column_id>[0-9]+)/$', column_views.attach_category),

    # goals
    url(r'^goals/feeds/$', GoalFeedsViewSet.as_view({'get': 'list'})),
    url(r'^goals/update-public/(?P<pk>[0-9]+)/$', PublicGoalUpdateView.as_view()),
    url(r'^goals/update-order/(?P<pk>[0-9]+)/$', OrderUpdateGoalView.as_view()),
    url(r'^goals/update/(?P<goal_id>[0-9]+)/$', goal_views.update),
    url(r'^goals/create/$', goal_views.create),
    url(r'^goals/delete/(?P<goal_id>[0-9]+)/$', goal_views.delete),
    url(r'^goals/attach/columns/$', goal_views.attach_to_column),
    url(r'^goals/show/(?P<goal_id>[0-9]+)/$', goal_views.show),
    url(r'^goals/long-short/(?P<goal_id>[0-9]+)/$', goal_views.long_short),
    url(r'^goals/update-status/(?P<goal_id>[0-9]+)/(?P<status_id>[0-9]+)$', goal_views.update_status),
    url(r'^goals/update-priority/(?P<goal_id>[0-9]+)/(?P<priority>[0-1]+)$', goal_views.update_priority),
    # fetch list of short term goals associated with a long term one

    # categories
    # url(r'^categories/create/$', categories_views.create),
    # url(r'^categories/delete/(?P<category_id>[0-9]+)/$', categories_views.delete),
    # url(r'^categories/attach/goals/$', categories_views.attach),


    # LABELS =========================== #

    url(r'^labels/(?P<label_id>[0-9]+)/attach/(?P<resource_name>[-\w]+)/(?P<resource_id>[0-9]+)/$', labels_view.attach),







    url(r'^areas-of-knowledge/search/(?P<keyword>[-\w]+)/$', aok_views.keyword),

    # TESTING ROUTS =========================== #

    # url(r'^test/mailgun/newuser/$', test_view.mailgun),



]

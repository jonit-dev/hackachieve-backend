from rest_framework import routers

from apps.goals.views import CommentPublicGoal

router = routers.SimpleRouter()
router.register(r'comment', CommentPublicGoal)
urlpatterns = router.urls
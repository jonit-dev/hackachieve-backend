from django.conf.urls import url
from .views import AreaOfKnowledgeView

app_name = "areas_of_knowledge"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    url(r'^areas-of-knowledge/(?P<pk>\d+)/', AreaOfKnowledgeView.as_view()), # ROUTES WITH ARGUMENTS COMES FIRST!!
    url(r'areas-of-knowledge/', AreaOfKnowledgeView.as_view()),
]

from django.conf.urls import url
from .views import LabelView

app_name = "labels"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    url(r'^labels/(?P<pk>\d+)/', LabelView.as_view()),
    url(r'^labels/goal/(?P<pk>\d+)/', LabelView.as_view()),



    # ROUTES WITH ARGUMENTS COMES FIRST!!
    # url(r'labels/', LabelView.as_view()),
]

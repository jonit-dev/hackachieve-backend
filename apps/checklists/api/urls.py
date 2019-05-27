from django.conf.urls import url
from .views import ChecklistView

app_name = "checklists"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    url(r'^checklists/(?P<pk>\d+)/', ChecklistView.as_view()), # ROUTES WITH ARGUMENTS COMES FIRST!!
    url(r'checklists/', ChecklistView.as_view()),
]

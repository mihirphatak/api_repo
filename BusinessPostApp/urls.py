from django.urls import path

from .views import BusinessPostsListAPI
from .apps import BusinesspostappConfig

app_name = BusinesspostappConfig.name

urlpatterns = [
    path('businesspostlistview', BusinessPostsListAPI.as_view(), name='BusinesspostListView'),
    
]
from django.urls import path

from .views import BusinessPostsListAPI,CreateBusinessPostsAPI,BusinessPostsListUserAPI,EditBusinessPostsAPI,BusinessCategoryList
from .apps import BusinesspostappConfig

app_name = BusinesspostappConfig.name

urlpatterns = [
    path('businesspostlistview', BusinessPostsListAPI.as_view(), name='BusinesspostListView'),
    path('createbusinesspost',CreateBusinessPostsAPI.as_view(),name='CreateBusinessPost'),
    path('businesspostlistuser', BusinessPostsListUserAPI.as_view(), name='BusinesspostListUser'),
    path('editbusinesspost', EditBusinessPostsAPI.as_view(), name='EditBusinesspostView'),
    path('businesscategorylist',BusinessCategoryList.as_view(),name='businesscategorylist')

]
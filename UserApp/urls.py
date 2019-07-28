from django.urls import path

from .views import Login, UserProfile,Register,EditProfile
from .apps import UserappConfig

app_name = UserappConfig.name

urlpatterns = [
    path('login', Login.as_view(), name='Login'),
    path('profile', UserProfile.as_view(), name='UserProfile'),
    path('register', Register.as_view(), name='Register'),
    path('editprofile', EditProfile.as_view(), name='EditProfile'),

]
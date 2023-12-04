from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistration, Logout


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', Logout.as_view()),
    path('register/', UserRegistration.as_view()),
]

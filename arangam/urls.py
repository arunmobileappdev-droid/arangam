from django.urls import path
from .views import get_user_list,create_user,user_login

urlpatterns = [
    path('user_list/',get_user_list),
    path('create_user/',create_user),
    path('user_login/',user_login)
]

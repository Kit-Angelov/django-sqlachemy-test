from django.urls import path
from api.auth.views import login, logout

urlpatterns = [
    path('login/', login),
    path('logout/', logout)
]
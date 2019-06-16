from django.urls import path
from api.profile.views import me

urlpatterns = [
    path('me/', me),
]

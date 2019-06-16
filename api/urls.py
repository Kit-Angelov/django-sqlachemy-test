from django.urls import path, include

urlpatterns = [
    path('', include('api.auth.urls')),
    path('profile/', include('api.profile.urls')),
]
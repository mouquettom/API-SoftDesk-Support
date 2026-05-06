from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet


# DefaultRouter génère automatiquement les routes standards du ViewSet
router = DefaultRouter()

# Génère les routes autour de /users/
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),  # Inclut toutes les routes générées par le router
]
from rest_framework import routers
from django.urls import path, include
from .api import ParticipantViewSet, WinnerSelectionViewSet

router = routers.DefaultRouter()
router.register(r'participants', ParticipantViewSet, basename='participants')
router.register(r'winner', WinnerSelectionViewSet, basename='winner')  

urlpatterns = [
    path('', include(router.urls)),
]

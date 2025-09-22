from rest_framework import routers
from .api import UserViewSet
from django.urls import path, include
from .views import VerifyUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = routers.DefaultRouter()

router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/verify/<uuid:code>/', VerifyUserView.as_view(), name='verify-user'),
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # obtener token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

]
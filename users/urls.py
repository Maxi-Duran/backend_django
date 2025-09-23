from rest_framework import routers
from .api import UserViewSet
from django.urls import path, include
from .views import VerifyUserView

router = routers.DefaultRouter()

router.register('users', UserViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/verify/<uuid:code>/', VerifyUserView.as_view(), name='verify-user')
]
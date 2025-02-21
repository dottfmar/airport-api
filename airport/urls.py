from django.urls import path, include
from rest_framework import routers

from airport import views

router = routers.DefaultRouter()
router.register("airplanes", views.AirplaneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
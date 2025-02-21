from django.urls import path, include
from rest_framework import routers

from airport import views

router = routers.DefaultRouter()
router.register("airplanes", views.AirplaneViewSet)
router.register("crews", views.CrewViewSet)
router.register("airports", views.AirportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
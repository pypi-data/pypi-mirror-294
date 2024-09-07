from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .viewsets import AuthorViewSet


router = DefaultRouter()
router.register("", AuthorViewSet, "author")

urlpatterns = [
    path("", include(router.urls)),
]

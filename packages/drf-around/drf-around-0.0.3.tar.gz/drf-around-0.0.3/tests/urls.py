from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .viewsets import AuthorViewSet, AuthorViewSetWithIsRelatedToUserPermission


router = DefaultRouter()
router.register("authors", AuthorViewSet, "author")
router.register(
    "related_authors", AuthorViewSetWithIsRelatedToUserPermission, "related-author"
)

urlpatterns = [
    path("", include(router.urls)),
]

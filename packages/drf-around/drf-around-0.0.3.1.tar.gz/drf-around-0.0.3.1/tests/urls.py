from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .viewsets import ProtectedAuthorViewSet, AuthorViewSet
from .views import AuthorCreateView


router = DefaultRouter()
router.register(
    "authors_viewset",
    AuthorViewSet,
    "author-viewset",
)
router.register(
    "protected_authors_viewset",
    ProtectedAuthorViewSet,
    "protected-author-viewset",
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "authors_view/",
        AuthorCreateView.as_view(),
        name="author-view",
    ),
]

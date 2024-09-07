from drf_around.permissions import IsRelatedToUserOrReadOnly
from drf_around.mixins import OverrideDataMixin

from rest_framework.viewsets import ModelViewSet

from .serializers import AuthorSerializer
from .models import Author


class ProtectedAuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        permissions = super().get_permissions()
        return permissions + [IsRelatedToUserOrReadOnly("user")]


class AuthorViewSet(OverrideDataMixin, ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_overriding_data(self):
        return {"user": self.request.user.pk}

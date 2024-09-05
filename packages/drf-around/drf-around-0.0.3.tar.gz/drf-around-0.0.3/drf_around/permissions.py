from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsRelatedToUser(BasePermission):
    error_message = "You need to be related to this object."

    def __init__(self, field_name):
        self.message = {field_name: self.error_message}
        self.field_name = field_name

    def has_object_permission(self, request, view, obj):
        for field in self.field_name.split("."):
            obj = getattr(obj, field)

        return self.is_user_related(obj, request.user)

    def is_user_related(self, obj, user):
        return obj == user


class IsRelatedToUserOrReadOnly(IsRelatedToUser):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or super().has_object_permission(
            request, view, obj
        )

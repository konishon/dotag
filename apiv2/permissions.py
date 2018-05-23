from rest_framework.permissions import BasePermission
from .models import ReportRating

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, ReportRating):
            return obj.reporter == request.user
        return obj.reporter == request.user
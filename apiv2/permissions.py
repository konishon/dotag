from rest_framework.permissions import BasePermission
from .models import Bucketlist

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Bucketlist):
            return obj.reporter == request.user
        return obj.reporter == request.user
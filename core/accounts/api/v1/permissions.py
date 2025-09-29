from rest_framework.permissions import BasePermission
from django.contrib.auth import logout


class NoPostForLoggedInUsers(BasePermission):
    def has_permission(self, request, view):
        # Deny POST if user is authenticated
        if request.method == "POST" and request.user.is_authenticated:
            logout(request)
            return False
        return True

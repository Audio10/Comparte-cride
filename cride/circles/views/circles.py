"""Circle view set.
    A View set its a class that extends from GenericViewSet.
    And other mixins, It's a special class that use the behavior of the mixins.

    - GenericAPIView: Class that implements a behavior for the CRUD.
    - MIXINS: Are classes that implements a specific behavior for a class that inherit GenericAPIView.
"""

# Django REST Framework
from rest_framework import viewsets, mixins

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsCircleAdmin

from cride.circles.models import Circle, Membership
from cride.circles.serializers import CircleModelSerializer


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Circle view set.

    The GenericViewSet class inherits from GenericAPIView, and provides the default set of get_object, get_queryset
    methods and other generic view base behavior, but does not include any actions by default.

    In order to use a GenericViewSet class you'll override the class and either mixin the required mixin classes,
     or define the action implementations explicitly.
    """

    serializer_class = CircleModelSerializer
    # Is the id that we going to use /platzi-mexico.
    lookup_field = 'slug_name'

    def get_queryset(self):
        """Restrict list to public-only.
        This method defined the default queryset.
        You can use the different data for different methods CRUD.
        """
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action.

        To override the permission you need to specify the condition for get other permission,
        You can create a new permission with the BasePermission class, and appends at the permission.

        We need to create a instance for each permission and return it.
        """
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )

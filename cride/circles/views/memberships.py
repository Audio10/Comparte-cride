"""Circle membership views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Models
from cride.circles.models import Circle, Membership

from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

# Serializers
from cride.circles.serializers import MembershipModelSerializer


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """"Circle membership view set."""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists.
        The method dispatch handlers how the request are response.
        IS ALWAYS RUNNING.
        So we need to get the circle to be access for all the request in this view.

        We override dispatch to be able verify that the circle exists.
        The kwargs can be arguments in the url.

        """
        slug_name = kwargs['slug_name']
        # specify the the model to get the object is Circle and the conditions.
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        return [permission() for permission in permissions]

    def get_queryset(self):
        """Return circle members."""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )

    def get_object(self):
        """
        Return the circle member by using the user's username
        {{host}}/circles/platzi-Mexico/members/mario

        The get_object is a method to override how we get a object from the model.
        """
        # specify the the model to get the object is Membership and the conditions.
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True
        )

    def perform_destroy(self, instance):
        """Disable membership.
        Overrides how the object is destroy.
        In this case we only going to change the is_active field.
        """
        instance.is_active = False
        instance.save()

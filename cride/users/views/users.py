"""Users views."""

# Django REST Framework
# This is the import for inherit the functionality for the Class based view.
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

# Permission
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from cride.users.permissions import IsAccountOwner

# Models
from cride.users.models import User
from cride.circles.models import Circle

# Serializers
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    ProfileModelSerializer
)

from cride.circles.serializers import CircleModelSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    """User view set.
    Handle sign up, login and account verification.

    The detail actions are the ones that needs the lookup_field in the url.
    When a method has the action decorator the name of the method is the url for the action.
        - example localhost:8000/verify
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'verify', 'login']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
            permissions = [IsAccountOwner, IsAuthenticated]
        else:
            permissions = [IsAuthenticated]

        return [permission() for permission in permissions]

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """User login. """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """User signup."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data,

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now go share some rides!'}

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data.
        In this case we can use self.get_object() -> get the user, This searchs in the kwargs
        a Slug or pk if this is present return the object like Model.objects.get(slug=slug)


        the user has the profile and we use a ProfileModelSerializer to get the data.


        """
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # The UserModelSerializer, has the Serializer for the profile.
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response.

        Retrieve the user and the circles that it has.
        Override the retrieve method for UserViewSet.
        """
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )

        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }

        response.data = data
        return response

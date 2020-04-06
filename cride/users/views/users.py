"""Users views."""

# Django REST Framework we use viewsets form implements actions.
from rest_framework import status, viewsets
from rest_framework.response import Response

# Actions
from rest_framework.decorators import action

# Serializers
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
)

class UserViewSet(viewsets.GenericViewSet):
    """User view set.
    Handle sign up, login and account verification.
    """

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
    
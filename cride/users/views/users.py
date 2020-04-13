"""Users views."""

# Django REST Framework we use viewsets form implements actions.
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

# Models
from cride.users.models import User
from cride.circles.models import Circle

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
) 

# Permissions Custom
from cride.users.permissions import IsAccountOwner

# Actions
from rest_framework.decorators import action

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
)

class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """User view set.
    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

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

    
    def retrieve(self, request, *args, **kwargs):
        """Adds extra data to the response."""
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

    @action(detail=True, methods=['PUT','PATCH'])
    def profile(self, request, *args, **kwargs):
        """Update  profile data."""
        
        # Takes the object that we going to update.
        user = self.get_object()
        profile = user.profile
        partial = request.method = 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)


    
"""Circle view set.
    A View set its a class that extends from GenericViewSet.
    And other mixins, It's a special class that use the behavior of the mixins.

    - GenericAPIView: Class that implements a behavior for the CRUD.
    - MIXINS: Are classes that implements a specific behavior for a class that inherit GenericAPIView.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from cride.circles.models import Circle
from cride.circles.serializers import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only.
        This method defined the default queryset.
        You can use the different data for different methods CRUD.
        """
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset


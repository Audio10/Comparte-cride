"""Circles views."""

# Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from cride.circles.models import Circle
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer


@api_view(['GET'])
def list_circles(request):
    """List circles."""
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_circle(request):
    """Create circles.
        For this method we going create a instance of CreateCircleSerializer,
        when you are using a serializer you can pass the data with the argument data.
        We can validate the data and save that in the serializer and we can use other serializer
        to create a specific type of data to return.
    """
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)

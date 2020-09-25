""""Circle serializers."""

# Django Rest Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from cride.circles.models import Circle


class CircleSerializer(serializers.Serializer):
    """" Circle serializer. """

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """ Create circle serializer. """

    def create(self, validated_data):
        """ Create circle:

            You can override the method create to implements something
            like that in you view:

            serializer.save() -> This method gets that functionality.

        """
        return Circle.objects.create(**validated_data)

    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[
            UniqueValidator(queryset=Circle.objects.all())
        ]
    )
    about = serializers.CharField(
        max_length=255,
        required=False
    )

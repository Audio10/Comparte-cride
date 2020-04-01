"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle

# Validators
from rest_framework.validators import UniqueValidator


class CircleSerializer(serializers.Serializer):
    """Circle serializer."""
    
    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()
    

class CreateCircleSerializer(serializers.Serializer):
    """Create circle serializer."""
    
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[
            # It validate that is unique inside the model.
            UniqueValidator(queryset=Circle.objects.all())
        ]
    )
    about = serializers.CharField(
        max_length=255, 
        required=False
    )
    
    def create(self, validated_data):
        """Create circle."""
        return Circle.objects.create(**validated_data)
    
    
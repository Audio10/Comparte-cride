"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer.
    We specify the members_limit and the is_limited fields because we going to use that,
    for the data validation.
    """

    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000
    )

    is_limited = serializers.BooleanField(default=False)

    class Meta:
        """Meta class."""
        model = Circle
        fields = (
            'name', 'slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'
        )

        # Specifies the read fields.
        read_only_fields = (
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken'
        )

    def validate(self, attrs):
        """Ensure both members_limit and is_limited are present."""
        members_limit = attrs.get('members_limit', None)
        is_limited = attrs.get('is_limited', False)
        # xor true only for 1-1 and 0-0.
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limited, a member limit must be provided')
        return attrs

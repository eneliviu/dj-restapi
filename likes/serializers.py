from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        # We don't need a get_is_owner method here because we
        # don't need to know if the currently logged in user is
        # the owner of a like.
        model = Like
        fields = [
            'id', 'created_at', 'owner', 'post'
        ]  # the fields of the Likes model + 'id'

    # Handle duplicate likes
    def create(self, validated_data):
        try:
            # create is on the serializers.ModelSerializer, call super()
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    'detail': 'possible duplicate'
                }
            )


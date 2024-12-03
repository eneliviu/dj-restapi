from django.db import IntegrityError
from rest_framework import serializers
from .models import Likes


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        # We don't need a get_is_owner method here because we
        # don't need to know if the currently logged in user is
        # the owner of a like.
        model = Likes
        fields = [
            'id', 'created_at', 'owner', 'post'
        ]  # the fields of the Likes model + 'id'

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

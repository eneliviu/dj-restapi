from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile()
        # When extending Django model class using models.Model, 
        # the 'id' field is created automatically. If we want it to be 
        # included into response, we have to add it to the serializes's fields array
        fields = [
            'id', 'owner', 'created_at', 'updated_at',
            'name', 'content', 'image'
        ]
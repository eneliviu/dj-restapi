from rest_framework import serializers
from .models import Profile
from followers.models import Follower
from cloudinary.utils import cloudinary_url


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    image = serializers.ImageField()

    def get_is_owner(self, obj):
        request = self.context['request']
        # print(f'profile serializer: ${request.user}')
        return request.user == obj.owner

    def get_following_id(self, obj):
        # check if the user is authenticated
        user = self.context['request'].user

        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user,
                followed=obj.owner
            ).first()
            # print(following)
            return following.id if following else None
        return None

    def get_image(self, obj):
        if obj.image:
            return cloudinary_url(obj.image.name)[0]
        return None

    class Meta:
        model = Profile
        # When extending Django model class using models.Model,
        # the 'id' field is created automatically. If we want it to be
        # included into response, we have to add it to the serializes's fields array
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]

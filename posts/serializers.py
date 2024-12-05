from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def get_like_id(self, obj):
        # check if the user is authenticated
        user = self.context['request'].user
        if user.is_authenticated:
            # check if the user likes the post 
            like = Like.objects.filter(
                owner=user,
                post=obj
            ).first()
            return like.id if like else None
        return None

    def validate_image(self, value):  # naming convention: 'validate_ + field name'
        # value is the uploaded image
        if value.size > 1024 * 1024 * 2:  # 2MB size limit
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:  # max 4096 px width
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        # When extending Django model class using models.Model,
        # the 'id' field is created automatically. If we want it to be
        # included into response, we have to add it to the serializes's fields array
        fields = [
           'id', 'owner', 'is_owner', 'profile_id',
           'profile_image', 'created_at', 'updated_at',
           'title', 'content', 'image', 'image_filter', 'like_id',
           'comments_count', 'likes_count'
        ]

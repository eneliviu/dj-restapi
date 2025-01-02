import os
from rest_framework import serializers
from .models import Post
from likes.models import Like
from cloudinary.utils import cloudinary_url


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    # profile_image = serializers.URLField(
    #     source='owner.profile.image.url',
    #     read_only=True
    # )
    # profile_image = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    image = serializers.ImageField()

    # naming convention: 'validate_ + field name'
    def validate_image(self, value):
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

        print(f'Image: {value}')
        file_extension = os.path.splitext(value.name)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png', '.gif']:
            raise serializers.ValidationError("Unsupported file extension.")

        return value

    # def get_is_owner(self, obj):
    #     request = self.context['request']
    #     return request.user == obj.owner

    # def get_like_id(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         like = Like.objects.filter(
    #             owner=user, post=obj).first()
    #         print(f'User: {user}, Like: {like}')  # Debugging statement
    #         return like.id if like else None
    #     return None

    def get_is_owner(self, obj):
        user = self.context.get('user')  # Access user from context
        return user and user == obj.owner

    def get_like_id(self, obj):
        user = self.context.get('user')  # Access user from context
        if user and user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            print(f'User: {user}, Like: {like}')  # Debugging statement
            return like.id if like else None
        return None

    def get_image(self, obj):
        if obj.image:
            return cloudinary_url(obj.image.name)[0]
        return None

    class Meta:
        model = Post
        # When extending Django model class using models.Model,
        # the 'id' field is created automatically. If we want it to be
        # included into response, we have to add it to the serializes's fields array
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'title', 'content', 'image',
            'image_filter', 'like_id', 'likes_count', 'comments_count'
        ]


from django.db.models import Count  # Count model instances
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),  # how many posts an user has
        followers_count=Count('owner__followed', distinct=True),  # no of users following a profile
        following_count=Count('owner__following', distinct=True)  # no of profiles a profile owner is following
    ).order_by('-created_at')  # newest profiles first

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at'
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),  # how many posts an user has
        followers_count=Count('owner__followed', distinct=True),  # no of users following a profile
        following_count=Count('owner__following', distinct=True)  # no of profiles a profile owner is following
    ).order_by('-created_at')


from django.db.models import Count
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, BooleanFilter
from drf_api.permissions import IsOwnerOrReadOnly
from posts.models import Post
from posts.serializers import PostSerializer

class PostFilter(FilterSet):
    liked_by_user = BooleanFilter(method='filter_liked_by_user')

    class Meta:
        model = Post
        fields = ['liked_by_user']

    def filter_liked_by_user(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(likes__owner=user)
        return queryset


class PostList(generics.ListCreateAPIView):
    """
    List posts or create a post if logged in
    The perform_create method associates the post with the logged in user.
    """
    # permission_classes = [IsOwnerOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')

    filterset_class = PostFilter
  
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
        'liked_by_user',
    ]

    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a post and edit or delete it if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

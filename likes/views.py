from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer


# Create your views here.
class LikeList(generics.ListCreateAPIView):
    """
    List likes or create a like if logged in.
    """
    # Only authenicated users can post likes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    # Set the user creating the like as its owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a like or delete it by id if you own it.
    """
    # Set the permission_classes to  our custom IsOwnerOrReadOnly permission,
    # which will allow only the user who liked a post to un-like it
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()


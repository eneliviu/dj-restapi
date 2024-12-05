from rest_framework import permissions, generics
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# Create your views here.
class CommentList(generics.ListCreateAPIView):
    '''
    Extending the List APIView : Don't need to implement GET
    Extending the Create APIView : Don't need to implement POST
    '''
    # Only authenicated users can post likes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    filter_backends = [
        DjangoFilterBackend
    ]
    filterset_fields = [
        'post'
    ]

    # Set the user creating the comment as its owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    




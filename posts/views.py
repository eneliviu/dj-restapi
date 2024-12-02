from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


# Create your views here.
class PostList(APIView):
    # create POST form:
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):  # List all posts
        posts = Post.objects.all()  # Get all objects from database
        serializer = PostSerializer(
            posts,
            many=True,
            context={'request': request})  # Serialize objects
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data,
            context={'request': request}
        )  # de-serialize
        if serializer.is_valid():
            serializer.save(owner=request.user)
            # Return serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return serialized data
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

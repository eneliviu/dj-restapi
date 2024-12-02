from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly


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


class PostDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]  # only the post's owner can edit or delete it
    serializer_class = PostSerializer  # Post edit form

    def get_object(self, pk):
        # Handle the 'post doesn't exist' exception
        try:
            post = Post.objects.get(pk=pk)
            # Make sure that the request's user has permission to edit7delete that post and return it
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):  # retrieve the post
        post = self.get_object(pk)
        serializer = PostSerializer(
            post,
            context={'request': request}
        )
        return Response(serializer.data)

    # Update the post
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
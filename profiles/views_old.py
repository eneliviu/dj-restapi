# from django.http import Http404
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response  # retrun content negotiated with API responses
# from .models import Profile
# from .serializers import ProfileSerializer
# from drf_api.permissions import IsOwnerOrReadOnly


# # Create your views here.
# class ProfileList(APIView):
#     '''
#     List all profiles.
#     No Create View (post method), as profile creation handled by django signals
#     '''
#     def get(self, request):
#         profiles = Profile.objects.all()  # Return all profiles
#         serializer = ProfileSerializer(
#             profiles,
#             many=True,
#             context={'request': request}
#         )  # serialize many profile instances
#         return Response(serializer.data)  # json data ready for the frontend to use


# class ProfileDetail(APIView):
#     serializer_class = ProfileSerializer  # render HTML form based on the model
#     permission_classes = [IsOwnerOrReadOnly]
    
#     def get_object(self, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile,
#             context={'request': request}
#         )  # single profile instance
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile,
#             data=request.data,
#             context={'request': request}
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

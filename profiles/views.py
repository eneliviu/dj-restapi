from rest_framework.views import APIView
from rest_framework.response import Response  # retrun content negotiated with API responses
from .models import Profile
from .serializers import ProfileSerializer
# Create your views here.


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles,
            many=True
        )  # serialize many profile instances
        return Response(serializer.data)  # json data ready for the fronend to use

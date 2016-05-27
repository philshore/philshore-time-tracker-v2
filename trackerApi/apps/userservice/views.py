from rest_framework.views import APIView
from serializers import UserSerializer
from models import TimeTrackerUser
import resp

# Create your views here.


class UsersView(APIView):
    '''
    Retrieves a Time Tracker User
    '''

    def get(self, request, format=None):
        users = UserSerializer(TimeTrackerUser.objects.all(), many=True)
        return resp.resp_ok(users.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return resp.resp_create(serializer.data)
        return resp.resp_error(serializer.errors)

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
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return resp.resp_create(user.data)
        return resp.resp_error(user.errors)

    def put(self, request, format=None):
        try:
            username = request.data['username']
        except:
            return resp.resp_error_none()

        queryset = TimeTrackerUser.objects.get(username=username)
        user = UserSerializer(queryset, data=request.data)
        if user.is_valid():
            user.save()
            return resp.resp_ok(user.data)
        else:
            return resp.resp_error(user.errors)

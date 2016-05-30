from rest_framework.views import APIView
from serializers import UserSerializer
from models import TimeTrackerUser
import resp


class UsersView(APIView):
    '''
    Creates, Retrieves and Updates a specific Time Tracker User
    '''

    def get(self, request, format=None):
        try:
            username = request.query_params.get('username', None)
            users = UserSerializer(TimeTrackerUser.objects.get(
                username=username))
            return resp.resp_ok(users.data)
        except:
            return resp.resp_error_none()

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


class UserListView(APIView):
    '''
    Retrieves all users with a specific project and component.
    '''

    def get(self, request, project=None, component=None):
        try:
            userlist = TimeTrackerUser.objects.filter(
                project=project).filter(component=component)
            users = UserSerializer(userlist)
            return resp.resp_ok(users.data)

        except:
            return resp.resp_error_none()

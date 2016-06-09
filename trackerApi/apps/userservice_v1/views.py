from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import TimeTrackerUser
from . import resp


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

    # This will be the registration endpoint
    def post(self, request, format=None):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return resp.resp_create(user.data)
        return resp.resp_error(user.errors)

    # This will be the update profile endpoint
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
    This will be used when creating a dashboard for a project leader.
    '''
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        try:
            component = request.query_params.get('component', None)
            project = request.query_params.get('project', None)
            userlist = TimeTrackerUser.objects.filter(
                project=project).filter(component=component)
            users = UserSerializer(userlist, many=True)
            return resp.resp_ok(users.data)

        except:
            return resp.resp_error_none()
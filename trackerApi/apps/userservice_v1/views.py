from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import TimeTrackerUser
from . import resp


class UsersView(APIView):
    '''
    Creates, Retrieves and Updates a specific Time Tracker User
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Requires an Token Authentication
    def get(self, request, format=None):
        try:
            username = request.user.username
            users = UserSerializer(TimeTrackerUser.objects.get(
                username=username))
            return resp.resp_ok(users.data)
        except:
            return resp.resp_error_none()

    # This will be the update profile endpoint
    # This also requires a token authentication
    def put(self, request, format=None):
        try:
            username = request.user.username
        except:
            return resp.resp_error_none()

        queryset = TimeTrackerUser.objects.get(username=username)
        user = UserSerializer(queryset, data=request.data)
        if user.is_valid():
            user.save()
            return resp.resp_ok(user.data)
        else:
            return resp.resp_error(user.errors)


class CreateUserView(APIView):
    '''
    Creates a user for the DTR tracker.
    '''
    def post(self, request, format=None):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return resp.resp_create(user.data)
        return resp.resp_error(user.errors)


class UserListView(APIView):
    '''
    Retrieves all users with a specific project and component.
    This will be used when creating a dashboard for a project leader.
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get(self, request):
        try:
            project = request.user.project
            userlist = TimeTrackerUser.objects.filter(
                project=project)
            users = UserSerializer(userlist, many=True)
            return resp.resp_ok(users.data)

        except:
            return resp.resp_error_none()


class AuthView(APIView):
    '''
    Creates a token for the api. If the user already has a token return
    the user token.
    '''
    def post(self, request, format=None):
        username = request.query_params.get('username')
        password = request.query_params.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                usertoken = Token.objects.create(user=user)
                return Response(usertoken.key)
            except:
                usertoken = Token.objects.get(user_id=user.id)
                return Response(usertoken.key)
        return Response("Invalid credentials.")

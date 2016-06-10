from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import TimeTrackerUser
import json


class UserTest(APITestCase):
    def setUp(self):
        """
        Create a test data and store it into a tmp.db
        """
        data = {
            "username": "testusername",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "project": "testproject",
            "component": "testcomponent",
            "password": "testpassword",
            "is_admin": True,
            "is_staff": True,
        }
        url = '/api/v1/userservice/create/'
        self.client.post(url, data, format='json')
        # url = "/api/v1/userservice/auth/?username=testusername&password=testpassword"
        # self.client.post(url, format='json')

    def test_models_create_user(self):
        user = TimeTrackerUser.objects.create_superuser(
            "testusername122", "testpassword", "philshore")
        self.assertEqual(user.username, "testusername122")

    def test_createuser_post(self):
        """
        Ensure we can create a user object.
        """
        data = {
            "username": "testusername333",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "project": "testproject",
            "component": "testcomponent",
            "password": "testpassword",
            "is_admin": True

        }
        url = '/api/v1/userservice/create/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TimeTrackerUser.objects.count(), 2)

    def test_user_put(self):
        """
        Ensure we can update a user.
        """
        data = {
            "username": "testusername",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "project": "testproject111",
            "component": "testcomponent",
            "password": "testpassword333",
            "is_admin": True

        }
        usertoken = getToken(self)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(usertoken))
        url = '/api/v1/userservice/user/'
        self.client.put(url, data, format='json')
        tracker_user = TimeTrackerUser.objects.get(username=data["username"])
        self.assertTrue(tracker_user.check_password('testpassword333'))
        self.assertEqual(tracker_user.project, "testproject")

    def test_user_get(self):
        """
        Ensure we can retrieve a stored user.
        """
        usertoken = getToken(self)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(usertoken))
        url = '/api/v1/userservice/user/'
        response = self.client.get(url, format='json')
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json["first_name"], "testfirstname")

    def test_userlist_get(self):
        """
        Ensure we can retrieve a list of users given a complete set of params.
        """
        usertoken = getToken(self)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(usertoken))
        url = '/api/v1/userservice/list/?project=testproject&component=testcomponent'
        response = self.client.get(url, format=json)
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json[0]["first_name"], "testfirstname")

    def test_login_post_success(self):
        """
        Returns a user authenticated token from the posted credentials.
        """
        url = '/api/v1/userservice/auth/?username=testusername&password=testpassword'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_post_failed(self):
        """
        Returns an invalid credentials json.
        """
        url = '/api/v1/userservice/auth/?username=testusern23&password=testpassword'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json, "Invalid credentials.")


def getToken(self):
    url = "/api/v1/userservice/auth/?username=testusername&password=testpassword"
    response = self.client.post(url, format='json')
    return json.loads(response.content.decode())

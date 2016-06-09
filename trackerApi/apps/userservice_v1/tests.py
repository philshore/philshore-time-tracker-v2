from rest_framework import status
from rest_framework.test import APITestCase
from .models import TimeTrackerUser
import json


class UserTest(APITestCase):
    def test_createuser_post(self):
        """
        Ensure we can create a user object.
        """
        data = {
            "username": "testusername",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "project": "testproject",
            "component": "testcomponent",
            "password": "testpassword",
            "is_admin": True

        }
        url = '/api/v1/userservice/user/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TimeTrackerUser.objects.count(), 1)
        self.assertEqual(
            TimeTrackerUser.objects.get().username, 'testusername')

    def test_user_put(self):
        """
        Ensure we can update a user.
        """
        setup_data(self)
        usertoken = getToken(self)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(usertoken))
        data = {
            "username": "testusername",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "project": "testproject111",
            "component": "testcomponent",
            "password": "testpassword333",
            "is_admin": True

        }
        url = '/api/v1/userservice/user/'
        self.client.put(url, data, format='json')
        tracker_user = TimeTrackerUser.objects.get(username=data["username"])
        self.assertTrue(tracker_user.check_password('testpassword333'))
        self.assertEqual(tracker_user.project, "testproject")

    def test_user_get(self):
        """
        Ensure we can retrieve a stored user.
        """
        setup_data(self)
        usertoken = getToken(self)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(usertoken))
        url = '/api/v1/userservice/user/?username=testusername'
        response = self.client.get(url, format='json')
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json["first_name"], "testfirstname")

    def test_userlist_none_get(self):
        """
        Ensure the there is no list of users if there are no given params.
        """
        setup_data(self)
        usertoken = getToken(self)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {}'.format(usertoken))
        url = '/api/v1/userservice/list/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '[]')

    def test_userlist_get(self):
        """
        Ensure we can retrieve a list of users given a complete set of params.
        """
        setup_data(self)
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
        setup_data(self)
        url = '/api/v1/userservice/auth/?username=testusername&password=testpassword'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_post_failed(self):
        """
        Returns an invalid credentials json.
        """
        setup_data(self)
        url = '/api/v1/userservice/auth/?username=testusern23&password=testpassword'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertEqual(response_json, "Invalid credentials.")


def setup_data(self):
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

    url = '/api/v1/userservice/user/'
    self.client.post(url, data, format='json')


def getToken(self):
    url = "/api/v1/userservice/auth/?username=testusername&password=testpassword"
    response = self.client.post(url, format='json')
    return json.loads(response.content.decode())

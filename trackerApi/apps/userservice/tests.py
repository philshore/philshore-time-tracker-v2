from rest_framework import status
from rest_framework.test import APITestCase
from models import TimeTrackerUser
# Create your tests here.


class UserTest(APITestCase):
    def test_createuser_post(self):
        """
        Ensure we can create a new scene object.
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
        url = '/api/user/users/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TimeTrackerUser.objects.count(), 1)
        self.assertEqual(
            TimeTrackerUser.objects.get().username, 'testusername')

    def test_user_update(self):
        setup_data(self)
        data = {
            "username": "testusername",
            "first_name": "testfirstname",
            "last_name": "testlastname",
            "project": "testproject111",
            "component": "testcomponent",
            "password": "testpassword333",
            "is_admin": True

        }
        url = '/api/user/users/'
        self.client.put(url, data, format='json')
        tracker_user = TimeTrackerUser.objects.get(username=data["username"])
        self.assertTrue(tracker_user.check_password('testpassword333'))

        self.assertEqual(tracker_user.project, "testproject")


def setup_data(self):
    data = {
        "username": "testusername",
        "first_name": "testfirstname",
        "last_name": "testlastname",
        "project": "testproject",
        "component": "testcomponent",
        "password": "testpassword",
        "is_admin": True

    }

    url = '/api/user/users/'
    self.client.post(url, data, format='json')



from rest_framework import status
from rest_framework.test import APITestCase
from models import TimeTrackerUser
# Create your tests here.


class UserTest(APITestCase):
    def test_create_scene_post(self):
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

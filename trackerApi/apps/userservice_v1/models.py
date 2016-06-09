from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class TimeTrackerUserManager(BaseUserManager):

    def create_user(self, project, username, password):
        timetracker_user = self.model(username=username, project=project)
        timetracker_user.set_password(password)
        timetracker_user.save(using=self._db)
        return timetracker_user

    def create_superuser(self, username, password, project):
        '''
        Creates a TimeTracker Super User from the CLI
        '''
        tracker_user = self.create_user(
            username=username, password=password, project=project)
        tracker_user.set_password(password)
        tracker_user.component = "admin"
        tracker_user.is_admin = True
        tracker_user.is_staff = True
        tracker_user.save(using=self._db)
        return tracker_user


class TimeTrackerUser(AbstractBaseUser):
    '''
    Base model of the timetracker user.
    '''

    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    project = models.CharField(max_length=250)
    component = models.CharField(max_length=250)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['project']

    objects = TimeTrackerUserManager()

    class Meta:
        '''
        Sorts the list with respect to their last names.
        '''

        ordering = ['last_name']

        def __str__(self):
            '''
            Returns the username of the timetracker user.
            '''
            return self.username

    def has_perm(self, perm, obj=None):
        '''
        Returns the permission settings of the user.
        '''
        return self.is_admin

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

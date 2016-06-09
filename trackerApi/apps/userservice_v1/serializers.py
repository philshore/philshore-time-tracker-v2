from rest_framework import serializers
from .models import TimeTrackerUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTrackerUser
        fields = ('username', 'first_name', 'password',
                  'last_name', 'project', 'component',
                  'is_staff', 'is_admin')

    def create(self, validated_data):
        '''
        Create and return a new User with their corresponding parameters.
        '''
        password = validated_data.pop('password')
        timetrackeruser = TimeTrackerUser.objects.create(**validated_data)
        timetrackeruser.set_password(password)
        timetrackeruser.save()
        return timetrackeruser

    def update(self, instance, validated_data):
        '''
        Update the password
        '''
        instance.set_password(validated_data.get(
            'password', instance.password
        ))

        instance.save()
        return instance

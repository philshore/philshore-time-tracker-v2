from rest_framework import serializers
from models import TimeTrackerUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTrackerUser
        fields = ('username', 'first_name',
                  'last_name', 'project', 'component', 'is_admin')

    def create(self, validated_data):
        '''
        Create and return a new User with their corresponding parameters.
        '''
        return TimeTrackerUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''
        Update the password
        '''
        instance.password = validated_data.get(
            'password', instance.password
        )

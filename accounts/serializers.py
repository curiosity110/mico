from django.contrib.auth.models import Group
from rest_framework import serializers

from accounts.models import User, GroupDescription


class GroupDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDescription
        fields = ['description']


class GroupSerializer(serializers.ModelSerializer):
    description = GroupDescriptionSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", 'date_joined', 'groups')

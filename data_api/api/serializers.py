from django.contrib.auth.models import User, Group
from rest_framework import serializers
from data_api.models import Dataset


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DataSerializer(serializers.ModelSerializer):
    group_by = serializers.CharField(read_only=True)
    cpi = serializers.FloatField(read_only=True)

    class Meta:
        model = Dataset
        fields = [
            'date', 'channel', 'country', 'os', 'impressions', 'clicks',
            'installs', 'spend', 'revenue', 'group_by', 'cpi'
        ]
        read_only_fields = [
            'date', 'channel', 'country', 'os', 'impressions', 'clicks',
            'installs', 'spend', 'revenue'
        ]

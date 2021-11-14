from django.contrib.auth.models import User, Group
from django.db.models import ExpressionWrapper, F, FloatField, Sum
from rest_framework.renderers import BrowsableAPIRenderer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from data_api.api.serializers import UserSerializer, GroupSerializer, DataSerializer
from data_api.api.permissions import IsOwnerOrReadOnly
from data_api.models import Dataset
from data_api.utils import http_import


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class DataApiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows DataAPI to be viewed or edited.
    """
    queryset = Dataset.objects.all()
    serializer_class = DataSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = {
        'date': ['gte', 'lte', 'range'],
        'channel': ['exact'],
        'country': ['exact'],
        'os': ['exact'],
    }
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        group_by = self.request.query_params.getlist('group_by')
        cpi = self.request.query_params.getlist('cpi')
        limit = self.request.query_params.getlist('limit')
        if group_by:
            queryset = Dataset.objects.values(*group_by).annotate(
                clicks=Sum('clicks'),
                impressions=Sum('impressions'),
                installs=Sum('installs'),
                revenue=Sum('revenue'),
                spend=Sum('spend'))
        if cpi:
            queryset = queryset.annotate(cpi=ExpressionWrapper(
                F('spend') / F('installs'), output_field=FloatField()))
        if limit:
            queryset = queryset.values(*group_by, *cpi, *limit)
        return queryset


@api_view(['POST'])
@renderer_classes([BrowsableAPIRenderer])
def import_dataset(request):
    message = http_import(request.data)
    return Response(message)

import django_filters
from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at= django_filters.DateFromToRangeFilter(field_name='created_at')
    status = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Advertisement
        fields = ['title', 'created_at', 'status']

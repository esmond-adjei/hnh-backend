import django_filters
from django.db.models import Q
from .models import Hostel, Room


class HostelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    rating__lt = django_filters.NumberFilter(
        field_name='rating', lookup_expr='lt')
    rating__gt = django_filters.NumberFilter(
        field_name='rating', lookup_expr='gt')

    class Meta:
        model = Hostel
        fields = ['name', 'location', 'rating__lt', 'rating__gt']

    @property
    def qs(self):
        queryset = super().qs
        # Check if any of the filter parameters exist in the URL query parameters
        if any(param in self.data for param in self.filters.keys()):
            return queryset
        else:
            # If no filter parameters are present, return an empty queryset
            return Hostel.objects.none()


class RoomFilter(django_filters.FilterSet):
    price__lt = django_filters.NumberFilter(
        field_name='price', lookup_expr='lt')
    price__gt = django_filters.NumberFilter(
        field_name='price', lookup_expr='gt')
    bedspace = django_filters.CharFilter(
        field_name='bedspace', lookup_expr='icontains')

    class Meta:
        model = Room
        fields = ['price__lt', 'price__gt', 'bedspace']

    @property
    def qs(self):
        queryset = super().qs
        if any(param in self.data for param in self.filters.keys()):
            return queryset
        else:
            return Room.objects.none()

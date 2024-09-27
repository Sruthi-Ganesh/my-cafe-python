from django_filters import rest_framework as filters

from cafe.models import Cafe


class CafeFilter(filters.FilterSet):
    location = filters.CharFilter()

    class Meta:
        model = Cafe
        fields = ['location']

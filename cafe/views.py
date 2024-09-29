from django.db.models import Count, F
from django_countries import countries
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets, views, parsers
from rest_framework.request import Request
from rest_framework.response import Response

from cafe.filters import CafeFilter
from cafe.models import Cafe
from cafe.serializers import CafeSerializer, \
    CafeLogoSerializer, CafeListSerializer
from common.serializers import FilterSerializer


class CafeView(mixins.CreateModelMixin, mixins.UpdateModelMixin,
               mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer


class CafeLogoUploadView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeLogoSerializer
    parser_classes = [parsers.MultiPartParser]


class CafeListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CafeListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CafeFilter

    def get_queryset(self):
        return Cafe.objects.all().prefetch_related("employee_cafes").annotate(
            employees_count=Count("employee_cafes")).order_by("-employees_count")


class CafeCountryListView(views.APIView):
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        keys = ["value", "label"]
        cafe_country_serializer = FilterSerializer(data=[
            dict(zip(keys, values))
            for values in list(countries)
        ], many=True)
        if cafe_country_serializer.is_valid():
            return Response(cafe_country_serializer.data)
        return Response({"message": cafe_country_serializer.errors})


class CafeFilterListView(views.APIView):
    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        cafes = list(
            Cafe.objects.all().annotate(
                label=F('name'),
                value=F('id')).values(
                'label',
                'value'))
        cafes_str = [{'label': c['label'], 'value': str(c['value'])} for c in cafes]
        cafe_country_serializer = FilterSerializer(data=cafes_str, many=True)
        if cafe_country_serializer.is_valid():
            return Response(cafe_country_serializer.data)
        return Response({"message": cafe_country_serializer.errors})

from django.urls import path, include
from rest_framework import routers

from cafe.views import CafeView, CafeListView, CafeCountryListView, CafeLogoUploadView, \
    CafeFilterListView

app_name = "cafe"

router = routers.DefaultRouter()
router.register(r"cafe", CafeView, basename='cafe')
router.register(r"cafe/logo/upload", CafeLogoUploadView, basename='cafe-logo-upload')
router.register(r"cafes", CafeListView, basename='cafe_list')

urlpatterns = [
    path(r"cafe/filter", CafeFilterListView.as_view(), name="cafe_filter"),
    path("", include(router.urls)),
    path(r"countries", CafeCountryListView.as_view(), name="cafe_country"),
]

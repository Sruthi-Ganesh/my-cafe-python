"""
URL configuration for my_cafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

patterns = [
    path('admin/', admin.site.urls),
    path(
        "api/v1/",
        include("employee.urls", namespace="employee"),
    ),
    path(
        "api/v1/",
        include("cafe.urls", namespace="cafe"),
    ),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Cafe API V1",
        default_version="v1",
        description="My Cafe",
        contact=openapi.Contact(email="s.sruthiganesh@gmail.com"),
    ),
    public=False,
    patterns=patterns,
)

urlpatterns = [
                  path(
                      "api/v1/swagger/",
                      schema_view.with_ui("swagger", cache_timeout=0),
                      name="schema-swagger-ui",
                  ),
              ] + patterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

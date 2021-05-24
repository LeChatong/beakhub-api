"""BeakHub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

admin.autodiscover()

schema_view = get_schema_view(
    openapi.Info(
        title="BeakHub API",
        default_version="v1",
        description="Core API Routes",
        terms_of_service="Copyright LeChatong 2021",
        contact=openapi.Contact(email="ulrich.tchatong@gmail.com"),
        license=openapi.License(name="MIT")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = i18n_patterns[
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/account/", include("Apps.account.urls")),
    path("api/v1/address/", include("Apps.address.urls")),
    path("api/v1/job/", include("Apps.job.urls")),
    path("api/v1/comment/", include("Apps.comment.urls")),
    path("api/v1/", schema_view.with_ui(
        'swagger', cache_timeout=0
    ), name='schema-swagger-ui'),
] + static("/static/", document_root=settings.STATIC_ROOT)
urlpatterns += static("/media/mail/", document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import warnings

    try:
        import debug_toolbar
    except ImportError:
        warnings.warn("The debug toolbar was not installed")
    else:
        urlpatterns += [url(r"^__debug__/", include(debug_toolbar.urls))]

    urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT)

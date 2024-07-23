from userapp.sitemap import *
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# sitemaps = {
#     'blog_sitepap':BlogSiteMap,
#     'service_sitemap': ServiceSiteMap,
#     'static_sitemap': StaticSitemap,
# }

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("userapp.urls")),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# urlpatterns += i18n_patterns(
#     path('i18n/', include('django.conf.urls.i18n')),
#     re_path(r'^rosetta/', include('rosetta.urls')),
#     path('', include("oneapp.urls")),
#     path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
# )

urlpatterns += static (settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from common import views
from common.routers import router
from environment.base import STATIC_ROOT, MEDIA_ROOT, MEDIA_URL
from environment.variables import EnvironmentVariable


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=True):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
   openapi.Info(
      title="Leadspace api",
      default_version='v1',
      description="Documentation for DRF Template Api",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="bernardnamangala@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes = (permissions.AllowAny,),
   generator_class=BothHttpAndHttpsSchemaGenerator
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HealthView.as_view(), name="Health-Check"),
    path('api/user/', include(('user.urls', 'user'), namespace='user_management')),
  
    # OAuth
    path('api/token/', TokenObtainPairView.as_view(serializer_class=TokenObtainPairSerializer),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(serializer_class=TokenObtainPairSerializer),
         name='token_refresh'),
    

    # Router
     path('api/', include(router.urls)),
     
    # API Documentation
     path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('logo.png', RedirectView.as_view(url=staticfiles_storage.url('logo.png')), name='logo'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

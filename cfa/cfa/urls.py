from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cfaRegister.views import CfaUserViewSet

router = DefaultRouter()
router.register(r'register-cfa', CfaUserViewSet, basename='register-cfa')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]

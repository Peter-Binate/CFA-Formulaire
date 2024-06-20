from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from cfaRegister.views import CfaUserViewSet, LoginView, InvitationViewSet, StudentRegisterView

router = DefaultRouter()
router.register(r'register-cfa', CfaUserViewSet, basename='register-cfa')
router.register(r'invite', InvitationViewSet, basename='invite')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('student-register/', StudentRegisterView.as_view(), name='student-register'),
]

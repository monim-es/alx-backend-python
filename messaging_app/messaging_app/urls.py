from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include API routes from the chats app
    path('api/', include('chats.urls')),  # ✅ correct app-level URL include

    # JWT auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Optional: DRF browsable API login
    path('api-auth/', include('rest_framework.urls')),
]

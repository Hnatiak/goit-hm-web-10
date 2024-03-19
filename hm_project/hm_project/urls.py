from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", include("quotes.urls")),
    path('auth/', include('app_auth.urls')),
    path('admin/', admin.site.urls),
    # path("users/", include("users.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

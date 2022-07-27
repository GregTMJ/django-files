from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Posts/', include('News.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('protect.urls')),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.relatorios.urls')),
    path('gastos/', include('apps.gastos.urls')),
    path('cartoes/', include('apps.cartoes.urls')),
    path('proventos/', include('apps.proventos.urls')),
]

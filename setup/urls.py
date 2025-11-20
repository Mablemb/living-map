"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve
from mapa.views import (
    BiomaViewSet,
    PersonagemViewSet,
    LojaViewSet,
    AssentamentoViewSet,
    MapaMundoViewSet,
    maps_list,
    map_editor,
    map_delete,
    bioma_editor,
    s3_health,
)

router = routers.DefaultRouter()
router.register('biomas', BiomaViewSet, basename='Biomas')
router.register('personagens', PersonagemViewSet, basename='Personagenss')
router.register('lojas', LojaViewSet, basename='Lojas')
router.register('assentamentos', AssentamentoViewSet, basename='Assentamentos')
router.register('mapas', MapaMundoViewSet, basename='Mapas')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth (login/logout/password) views
    path('accounts/', include('django.contrib.auth.urls')),
    # Registro de usuário
    path('accounts/', include('mapa.urls')),
    # Logout direto na raiz
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # API
    path('api/', include(router.urls)),
    # HTML pages
    path('', maps_list, name='map_list'),
    path('mapas/<int:mapa_id>/', map_editor, name='map_editor'),
    path('mapas/<int:mapa_id>/biomas/', bioma_editor, name='bioma_editor'),
    path('mapas/<int:mapa_id>/delete/', map_delete, name='map_delete'),
    path('health/s3/', s3_health, name='s3_health'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media in production if no reverse proxy is configured
if not settings.DEBUG and settings.MEDIA_URL:
    # This is a lightweight fallback. Prefer Nginx or a CDN in production.
    media_url = settings.MEDIA_URL.lstrip('/')
    urlpatterns += [
        path(f"{media_url}<path:path>", static_serve, {"document_root": settings.MEDIA_ROOT}),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
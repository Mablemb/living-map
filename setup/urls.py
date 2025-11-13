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
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
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
    # API
    path('api/', include(router.urls)),
    # HTML pages
    path('', maps_list, name='map_list'),
    path('mapas/<int:mapa_id>/', map_editor, name='map_editor'),
    path('mapas/<int:mapa_id>/biomas/', bioma_editor, name='bioma_editor'),
    path('mapas/<int:mapa_id>/delete/', map_delete, name='map_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

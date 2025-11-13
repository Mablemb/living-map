from django.contrib import admin
from mapa.models import Bioma, Loja, Personagem, Assentamento, MapaMundo

class Biomas(admin.ModelAdmin):
    list_display = ('id','nome','tipo',)
    list_display_links = ('nome',)
    list_per_page = 10
    search_fields = ('nome','tipo',)

admin.site.register(Bioma,Biomas)

class Lojas(admin.ModelAdmin):
    list_display = ('id','nome','tipo','lojista')
    list_display_links = ('nome','tipo','lojista')
    list_per_page = 10
    search_fields = ('nome','tipo','lojista',)

admin.site.register(Loja,Lojas)

class Personagens(admin.ModelAdmin):
    list_display = ('id','nome','raca','origem','aparencia','segredo',)
    list_display_links = ('nome','origem',)
    list_per_page = 10
    search_fields = ('nome','raca')

admin.site.register(Personagem,Personagens)

class Assentamentos(admin.ModelAdmin):
    list_display = ('id','nome','tipo','listar_biomas','caracteristica','fama','calamidade','lider',)
    list_display_links = ('id',)
    list_per_page = 10
    search_fields = ('nome','tipo','lider',)

    def listar_biomas(self,obj):
        return ", ".join(b.nome for b in obj.bioma.all())

admin.site.register(Assentamento,Assentamentos)

# Register your models here.

@admin.register(MapaMundo)
class MapaMundoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'largura', 'altura', 'criado_em')
    search_fields = ('nome',)

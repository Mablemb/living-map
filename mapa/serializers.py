from django.contrib.auth.models import Group, User
from mapa.models import Bioma, Personagem, Loja, Assentamento, MapaMundo
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class BiomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bioma
        fields = '__all__'
        read_only_fields = ['largura','altura']
        
class PersonagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personagem
        fields = '__all__'

class LojaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loja
        fields = '__all__'

class AssentamentoSerializer(serializers.ModelSerializer):
    # Embute os personagens que têm origem neste assentamento
    personagens = serializers.SerializerMethodField()
    bioma = BiomaSerializer(many=True, read_only=True)
    lojas = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    lider_display = serializers.CharField(source='get_lider_display', read_only=True)
    fama_display = serializers.CharField(source='get_fama_display', read_only=True)

    class Meta:
        model = Assentamento
        fields = '__all__'

    def get_personagens(self, obj):
        # Usa o reverse accessor padrão personagem_set
        qs = getattr(obj, 'personagem_set', None)
        if qs is None:
            return []
        return PersonagemSerializer(qs.all(), many=True).data

    def get_lojas(self, obj):
        qs = getattr(obj, 'loja_set', None)
        if qs is None:
            return []
        return LojaSerializer(qs.all(), many=True).data

class AssentamentoMarkerSerializer(serializers.ModelSerializer):
    personagem_count = serializers.IntegerField(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    bioma_ids = serializers.PrimaryKeyRelatedField(source='bioma', many=True, read_only=True)

    class Meta:
        model = Assentamento
        fields = ["id", "nome", "tipo", "tipo_display", "pos_x", "pos_y", "mapa", "personagem_count", "bioma_ids"]

class MapaMundoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapaMundo
        fields = "__all__"

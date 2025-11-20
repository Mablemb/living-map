from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from mapa.models import Bioma, Personagem, Loja, Assentamento, MapaMundo, ponto_em_poligono
from mapa.serializers import (
    GroupSerializer,
    UserSerializer,
    BiomaSerializer,
    PersonagemSerializer,
    LojaSerializer,
    AssentamentoSerializer,
    AssentamentoMarkerSerializer,
    MapaMundoSerializer,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class BiomaViewSet(viewsets.ModelViewSet):
    queryset = Bioma.objects.all()
    serializer_class = BiomaSerializer
    filterset_fields = ['mapa', 'tipo', 'nome']

class PersonagemViewSet(viewsets.ModelViewSet):
    queryset = Personagem.objects.all()
    serializer_class = PersonagemSerializer

class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer
    
class AssentamentoViewSet(viewsets.ModelViewSet):
    queryset = Assentamento.objects.all().prefetch_related('bioma','personagem_set','mapa')
    serializer_class = AssentamentoSerializer

    @action(detail=False, methods=['get'])
    def markers(self, request):
        qs = (self.get_queryset()
              .annotate(personagem_count=Count('personagem'))
              .only('id','nome','tipo','pos_x','pos_y','mapa'))
        mapa_id = request.query_params.get('mapa')
        if mapa_id:
            qs = qs.filter(mapa_id=mapa_id)
        serializer = AssentamentoMarkerSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Cria o assentamento e, se bioma não for enviado, tenta auto-atribuir
        com base no ponto (pos_x,pos_y) dentro dos polígonos dos biomas do mapa.
        """
        data = self.request.data
        instance = serializer.save()
        # Se veio _bioma_ids manual (hack via front), atribui primeiro
        manual_ids = data.get('_bioma_ids')
        if manual_ids and isinstance(manual_ids, list):
            try:
                instance.bioma.set([int(i) for i in manual_ids])
            except Exception:
                pass
        # Se já veio bioma na requisição, não precisa auto-atribuir
        if instance.bioma.exists():
            return
        if instance.mapa_id and instance.pos_x is not None and instance.pos_y is not None:
            candidatos = Bioma.objects.filter(mapa_id=instance.mapa_id)
            biomas_ids = []
            for b in candidatos:
                try:
                    for poli in b.poligonos or []:
                        if ponto_em_poligono(instance.pos_x, instance.pos_y, poli):
                            biomas_ids.append(b.id)
                            break
                except Exception:
                    # ignora biomas com dados inválidos
                    continue
            if biomas_ids:
                instance.bioma.set(biomas_ids)

class MapaMundoViewSet(viewsets.ModelViewSet):
    queryset = MapaMundo.objects.all().order_by('-criado_em')
    serializer_class = MapaMundoSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        obj = self.get_queryset().first()
        if not obj:
            return Response({'detail': 'Nenhum mapa encontrado.'}, status=404)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


# ----------------------- Views HTML (autenticadas) -----------------------

@login_required
def maps_list(request):
    """Página inicial: lista mapas, permite criar e deletar."""
    error_message = None
    if request.method == 'POST' and request.FILES.get('imagem'):
        nome = request.POST.get('nome') or 'Mapa sem nome'
        imagem = request.FILES['imagem']
        try:
            MapaMundo.objects.create(nome=nome, imagem=imagem)
            # Log último mapa e URL real após salvar
            ultimo = MapaMundo.objects.order_by('-id').first()
            if ultimo and ultimo.imagem:
                logger.warning("Mapa salvo. nome=%s chave=%s url=%s", ultimo.nome, ultimo.imagem.name, ultimo.imagem.url)
            return redirect('map_list')
        except Exception as e:
            error_message = f"Falha ao enviar imagem: {e}"

    mapas = MapaMundo.objects.all().order_by('-criado_em')
    return render(request, 'mapa/map_list.html', {'mapas': mapas, 'error_message': error_message})


@login_required
def s3_health(request):
    """Retorna informações de saúde do backend S3 para diagnóstico rápido."""
    info = {}
    from django.conf import settings
    info['DEFAULT_FILE_STORAGE'] = settings.DEFAULT_FILE_STORAGE
    info['STATICFILES_STORAGE'] = settings.STATICFILES_STORAGE
    info['AWS_BUCKET'] = settings.AWS_STORAGE_BUCKET_NAME
    info['AWS_DOMAIN'] = settings.AWS_S3_CUSTOM_DOMAIN
    info['AWS_MEDIA_LOCATION'] = settings.AWS_MEDIA_LOCATION
    info['AWS_QUERYSTRING_AUTH'] = settings.AWS_QUERYSTRING_AUTH
    ultimo = MapaMundo.objects.order_by('-id').first()
    if ultimo and ultimo.imagem:
        info['ultimo_mapa_nome'] = ultimo.nome
        info['ultimo_mapa_chave'] = ultimo.imagem.name
        try:
            info['ultimo_mapa_url'] = ultimo.imagem.url
        except Exception as e:
            info['ultimo_mapa_url_error'] = str(e)
        # Tenta HEAD no objeto
        try:
            s3 = boto3.client('s3', region_name=os.getenv('AWS_S3_REGION_NAME'))
            s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=ultimo.imagem.name)
            info['head_object'] = 'OK'
        except ClientError as ce:
            info['head_object_error'] = str(ce)
    return Response(info)


@require_http_methods(["POST"])
@login_required
def map_delete(request, mapa_id: int):
    mapa = get_object_or_404(MapaMundo, pk=mapa_id)
    # Remove arquivo físico antes de deletar o objeto (opcional)
    if mapa.imagem:
        mapa.imagem.delete(save=False)
    mapa.delete()
    return redirect('map_list')


@login_required
def map_editor(request, mapa_id: int):
    mapa = get_object_or_404(MapaMundo, pk=mapa_id)
    return render(request, 'mapa/map_detail.html', {'mapa': mapa})

@login_required
def bioma_editor(request, mapa_id: int):
    """Página para desenhar polígonos de biomas sobre o mapa usando Leaflet.draw."""
    mapa = get_object_or_404(MapaMundo, pk=mapa_id)
    return render(request, 'mapa/bioma_editor.html', {'mapa': mapa})


def register(request):
    """Tela de registro de novo usuário usando UserCreationForm padrão."""
    error_message = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('map_list')
        except Exception as e:
            # Em produção, exibe o erro para facilitar o diagnóstico
            error_message = f"Ocorreu um erro ao criar o usuário: {e}"
    else:
        form = UserCreationForm()

    context = {
        'form': form,
        'error_message': error_message,
    }
    return render(request, 'registration/register.html', context)

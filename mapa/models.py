from django.db import models
from django.core.files.images import get_image_dimensions

class Bioma(models.Model):
    '''
    Biomas
    Id [int]
    Tipo [1 opção]
    Nome [ex: <Tipo> + Caracteristica/Toponimo]
    '''
    TIPO = (
        ('1','Artico'),
        ('2','Costeiro'),
        ('3','Deserto'),
        ('4','Floresta'),
        ('5','Campo'),
        ('6','Morro'),
        ('7','Montanha'),
        ('8','Pantano'),
        ('9','Subterraneo'),
        ('10','Urbano'),
        ('11','Maritmo'),
    )

    nome = models.CharField(max_length=120, unique=True, blank=False, null=False)
    tipo = models.CharField(max_length=2, choices=TIPO, blank=False, null=False, default='2')
    # Polígonos em coordenadas de imagem (px) no(s) mapa(s).
    # Estrutura: lista de polígonos; cada polígono é lista de [x,y]. Ex: [ [[x1,y1],[x2,y2],...], ... ]
    poligonos = models.JSONField(default=list, blank=True)
    # Mapa ao qual o bioma pertence (opcional para compatibilidade)
    mapa = models.ForeignKey('MapaMundo', on_delete=models.CASCADE, related_name='biomas', null=True, blank=True)
    # cor sugerida para exibição
    cor = models.CharField(max_length=7, default='#88cc66', blank=True)

    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome


class MapaMundo(models.Model):
    """
    Mapa de Mundo para o RPG. Contém a imagem base e suas dimensões.
    A imagem é usada como "tile" único (CRS.Simple) para posicionar Assentamentos por pixel (pos_x,pos_y).
    """
    nome = models.CharField(max_length=120, unique=True)
    imagem = models.ImageField(upload_to='mapas/')
    largura = models.PositiveIntegerField(editable=False, null=True, blank=True)
    altura = models.PositiveIntegerField(editable=False, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Salva primeiro para garantir que o arquivo exista em disco
        super().save(*args, **kwargs)
        # Após salvar, se não houver dimensões persistidas, calcule-as
        if self.imagem and (not self.largura or not self.altura):
            try:
                w, h = get_image_dimensions(self.imagem)
                type(self).objects.filter(pk=self.pk).update(largura=w, altura=h)
                # Também atualiza em memória para quem usa a instância após save
                self.largura, self.altura = w, h
            except Exception:
                # Evita quebrar o fluxo caso Pillow não esteja disponível ou arquivo inválido
                pass

    def __str__(self):
        return self.nome

class Personagem(models.Model):
    '''
    Personagens
    Id [int]
    Nome []
    Raça []
    Assentamento de Origem [1 assentamento]
    Aparencia [1 ou 2 opções]
    Segredos [1 opção]
    '''

    APARENCIA = (
        ('1','Ostenta Joias Diferenciadas'),
        ('2','Roupas Diferenciadas (Chamativas, Estrangeiras, Formais ou Trapos)'),
        ('3','Dispositivo Auxiliar de Marcha elegante (Bengala, cadeira de rodas/flutuante, tala/exoesqueleto)'),
        ('4','Cicatriz Marcante'),
        ('5','Olhos de cor incomum (ou de 2 cores diferentes)'),
        ('6','Tatuagens/Piercings'),
        ('7','Marca de Nascença'),
        ('8','Cabelos de cor incomum'),
        ('9','Careca OU Barba/Cabelo trançado'),
        ('10','Nariz distinto (grande/pequeno ou quebrado ou bulboso)'),
        ('11','Postura distinta (Encurvado ou Rígido)'),
        ('12','Extremamente belo/feio'),
    )

    SEGREDO = (
        ('1','Disfarçado, ocultando identidade ou aspecto especifico da aparencia'),
        ('2','Planejando/Executando/Escondendo um crime'),
        ('3','Esta pessoa ou a família dela foi ameaçada de morte caso deixe de fazer algo'),
        ('4','Magicamente influenciada a se comportar de determinada forma'),
        ('5','Terrivelmente doente ou acometido por dor crônica'),
        ('6','Se sente responsável pela morte/infortúnio de alguém'),
        ('7','Prestes a falir catastroficamente'),
        ('8','Desesperadamente carente ou nutrindo paixão não correspondida'),
        ('9','Nutrindo uma ambição poderosa'),
        ('10','Profundamente insatisfeito/deprimido'),
    )   

    nome = models.CharField(max_length=120, unique=True, blank = False, null = False)
    raca = models.CharField(max_length=60, unique=True, blank = False, null = False)
    origem = models.ForeignKey('Assentamento',on_delete = models.CASCADE)
    aparencia = models.CharField(max_length = 2, choices = APARENCIA, blank = False, null = False, default = '1')
    segredo = models.CharField(max_length = 2, choices = SEGREDO, blank = False, null = False, default = '1')

    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Loja(models.Model):
    '''
    Lojas
    Id [int]
    nome [CharField max 120]
    Tipo [1 opção]
    Lojista [Personagem]
    '''

    TIPO = (
        ('1','Penhora'),
        ('2','Apotecário'),
        ('3','Mercearia'),
        ('4','Iguarias Finas/Exóticas'),
        ('5','Olaria'),
        ('6','Funerária'),
        ('7','Livraria'),
        ('8','Banco'),
        ('9','Armoraria'),
        ('10','Velas e Incensos'),
        ('11','Forja/Oficina'),
        ('12','Carpintaria'),
        ('13','Ateliê'),
        ('14','Joalheria'),
        ('15','Padaria'),
        ('16','Cartografo'),
        ('17','Alfaiate'),
        ('18','Cordoaria'),
        ('19','Construtora'),
        ('20','Biblioteca'),
    )

    nome = models.CharField(max_length=120, unique=True, blank = False, null = False)
    tipo = models.CharField(max_length = 2, choices = TIPO, blank = False, null = False, default = '13')
    lojista = models.OneToOneField(Personagem, on_delete=models.CASCADE, related_name='loja', null=True)

    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

class Assentamento(models.Model):
    '''
    Assentamentos
    Id [int]
    Nome [CharField 120 max]
    Tipo [V, C ou M]
    Bioma [1 ou 2 biomas]
    Caracteristicas Marcantes [1 para Vilarejo, 2 para Cidade, 3 para Metropole]
    Fama [1 opção para Vilarejo e Cidade, 2 opções para Metrópole]
    Calamidade Atual [1 para Vilarejo, 2 para Cidade, 3 para Metropole]
    Lider Local [Tipo de Lider]
    Lojas [Lista de Lojas]
    Pessoas Notaveis [Lista de Personagens]
    '''

    TIPO = (
        ('V','Vilarejo, até 500 habitantes, preço máximo de itens a venda 50 GP'),
        ('C','Cidade, de 5001 a 5000 habitantes, preço máximo de itens a venda 2.000 GP'),
        ('M','Metrópole, mais de 5000 habitantes, preço máximo de itens a venda 200.000 GP'),
    )

    CARACTERISTICAS = (
        ('1', 'Muralhas Fortificadas'),
        ('2', 'Parques, Jardins e Vegetação Abundante'),
        ('3', 'Lama, lixo e imundice'),
        ('4', 'Cemitério extenso'),
        ('5', 'Nevoeiro Persistente'),
        ('6', 'Sons e Fumaça de Forjas'),
        ('7', 'Canais Substituem as ruas muitas pontes os cruzam'),
        ('8', 'Fronteira com penhasco'),
        ('9', 'Ruas e Construções bem mantidas e limpas'),
        ('10', 'Ruínas Antigas em meio ao assentamento'),
        ('11', 'Mercado/Bazar com aromas e itens exóticos'),
        ('12', 'Estrutura Impressionante (Castelo, Templo, Circulo de pedras ou Zigurate/Piramide)'), 
    )

    FAMA = (
        ('1', 'Comida Deliciosa'),
        ('2', 'População Rude'),
        ('3', 'População Amigável'),
        ('4', 'Artistas e Escritores'),
        ('5', 'Grande Heroi/Salvador local'),
        ('6', 'Flores'),
        ('7', 'Festival Anual'),
        ('8', 'Assombrações'),
        ('9', 'Conjuradores de Magia'),
        ('10', 'Decadencia'),
        ('11', 'Piedade'),
        ('12', 'Apostas'),
        ('13', 'Aversão a Religião'),
        ('14', 'Educação'),
        ('15', 'Vinhos/Vinhedos'),
        ('16', 'Moda/Alta Costura'),
        ('17', 'Intriga Política'),
        ('18', 'Guildas Poderosas'),
        ('19', 'Patriotismo'),
        ('20', 'Ruínas Antigas'),
    )

    CALAMIDADES = (
        ('1','Infestção de Monstros'),
        ('2','Suspeita de assassinato do lider local'),
        ('3','Guerra iminente entre guildas/gangues locais'),
        ('4','Pragas/Fome provocam rebelião'),
        ('5','Monstros atacam qualquer um que se aproxima ou tenta deixar o assentamento'),
        ('6','Disputas comerciais criam crise economica'),
        ('7','Desastre natural ameaça o assentamento'),
        ('8','Profecia terrivel assusta moradores'),
        ('9','População em alistamento para guerra'),
        ('10','Violencia devido a intrigas políticas/religiosas'),
        ('11','Assentamento sob cerco'),
        ('12','Escandalo ameaça famílias nobres'),
    )

    LIDER = (
        ('1','Lider/Conselho Justos e Respeitados'),
        ('2','Tirano Temido'),
        ('3','Covarde Manipulado por outros'),
        ('4','Lider conhecidamente Ilegítmo e rejeitado'),
        ('5','Monstro poderoso'),
        ('6','Conspiradores anonimos misteriosos'),
        ('7','Liderança em disputa aberta e violenta'),
        ('8','Conselho disputado incapaz de tomar decisões'),
        ('9','Lider conhecidamente Imbecil/Idiota'),
        ('10','Lider moribundo com sucessão disputada'),
        ('11','Lider/Conselho mão-de-ferro respeitado'),
        ('12','Lider/Conselho religioso'),
    )

    nome = models.CharField(max_length=120, unique=True, blank = False, null = False)
    tipo = models.CharField(max_length = 2, choices = TIPO, blank = False, null = False, default = 'V')
    bioma = models.ManyToManyField(Bioma, blank=True)
    caracteristica = models.CharField(max_length = 2, choices = CARACTERISTICAS, blank = False, null = False, default ='2')
    fama = models.CharField(max_length = 2, choices = FAMA, blank = False, null = False, default = '1')
    calamidade = models.CharField(max_length = 2, choices = CALAMIDADES, blank = False, null = False, default = '1')
    lider = models.CharField(max_length = 2, choices = LIDER, blank = False, null = False, default = '1')
    # Referência ao mapa no qual o assentamento existe
    mapa = models.ForeignKey(MapaMundo, on_delete=models.CASCADE, related_name='assentamentos', null=True, blank=True)
    # Coordenadas na imagem do mapa (pixels)
    pos_x = models.FloatField(blank=True, null=True, help_text="Coordenada X (px) na imagem do mapa")
    pos_y = models.FloatField(blank=True, null=True, help_text="Coordenada Y (px) na imagem do mapa")
    #personagens_notaveis = models.ManyToManyField(Personagem)

    class Meta:
        ordering = ["nome"]
    
    def __str__(self):
        return self.nome

    # Utilitário: checa se um ponto (x,y) está dentro de algum polígono do bioma
def ponto_em_poligono(x: float, y: float, poligono: list[list[float]]):
    # Ray casting (par ímpar)
    inside = False
    n = len(poligono)
    if n < 3:
        return False
    j = n - 1
    for i in range(n):
        xi, yi = poligono[i]
        xj, yj = poligono[j]
        intersect = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi
        )
        if intersect:
            inside = not inside
        j = i
    return inside
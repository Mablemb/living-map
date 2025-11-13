# RPG World Manager (Django)

Aplicação web para gerenciar mundo de RPG através de um mapa fantasioso. Permite:

- Upload de imagem do mapa (MapaMundo)
- Desenho de áreas (Biomas) sobre a imagem via polígonos
- Criação de assentamentos clicando no mapa (coordenadas em pixels)
- Associação automática de biomas ao assentamento se ele cair dentro de um polígono
- Visualização opcional dos biomas sobre o mapa
- Listagem e edição (polígonos) ou remoção de biomas
- Inclusão de personagens ligados a assentamentos (já suportado pelo modelo)

## Tecnologias
- Django 5
- Django REST Framework
- Leaflet + Leaflet.draw (front-end simples em templates)
- python-dotenv para gerenciamento de variáveis de ambiente

## Estrutura principal
```
manage.py
setup/            # Configurações Django
mapa/             # App principal (models, views, serializers)
templates/        # Templates (map_list, map_detail, bioma_editor, login)
media/            # Uploads (mapas enviados)
```

## Variáveis de Ambiente
Copiar `/.env.example` para `.env` e ajustar:

```
DJANGO_SECRET_KEY=uma-string-grande-aleatoria
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Nunca versionar `.env` real.

## Instalação

```bash
# Clonar
git clone <URL_DO_REPO>
cd RPDjango

# Criar venv (opcional se já existir .venv)
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar .env
cp .env.example .env

# Migrar banco
python manage.py migrate

# Criar superusuário (para /admin)
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

## Fluxo de Uso
1. Acesse `/admin/` e faça login.
2. Crie um `MapaMundo` enviando a imagem base (o sistema detecta largura/altura).
3. Vá para `/` (dashboard): verá o mapa listado. Clique em "Abrir".
4. Na página do mapa (`/mapas/<id>/`) clique para capturar X/Y e criar assentamentos.
5. Use "Editar Biomas" para desenhar áreas (polígonos) e salvar biomas.
6. Volte ao mapa e use o botão "Mostrar Biomas" para alternar visualização das áreas.
7. Assentamentos criados dentro de polígonos têm bioma atribuído automaticamente.

## Endpoints Principais (API)
- `POST /api/mapas/` – cria mapa (imagem)
- `GET /api/mapas/latest/` – último mapa
- `GET /api/assentamentos/markers/?mapa=<id>` – lista leve de assentamentos
- `POST /api/assentamentos/` – cria assentamento (campos: nome, tipo, pos_x, pos_y, mapa, opcional `_bioma_ids`)
- `GET /api/biomas/?mapa=<id>` – lista biomas de um mapa
- `POST /api/biomas/` – cria bioma (`nome`, `tipo`, `cor`, `mapa`, `poligonos`)
- `PUT /api/biomas/<id>/` – atualiza bioma (substitui polígonos)
- `DELETE /api/biomas/<id>/` – remove bioma e suas camadas

## Representação de Polígonos
Campo `poligonos` em Bioma (JSON):
```
[
  [  # conjunto (coleção) de polígonos
    [ [x,y], [x,y], ... ],  # polígono 1
    [ [x,y], [x,y], ... ]   # polígono 2
  ]
]
```
Cada polígono: lista de vértices em coordenadas de pixel da imagem.

## Segurança / Produção
- Usar um SECRET_KEY forte em `.env`.
- Ajustar `DJANGO_ALLOWED_HOSTS` para incluir domínio.
- Servir `media/` por Nginx/Apache (não recomendado usar Django para isso em produção).
- Considerar adicionar HTTPS, cache e cabeçalhos de segurança.

## Próximas Melhorias (Ideias)
- Modal de detalhes do assentamento e criação de personagens inline.
- Controle de sobreposição de biomas e prioridade.
- Exportação/importação de dados (JSON).
- Tests automatizados (pytest ou unittest) para endpoints.
- Suporte a múltiplos mapas na UI principal.

## Licença
Defina a licença desejada (ex: MIT). Adicione um arquivo LICENSE se necessário.

Boa exploração do mundo! 🎲

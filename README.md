git clone <URL_DO_REPO>
# RPG World Manager (Django)

Uma aplicação web para gerenciar e visualizar mundos de RPG através de mapas e entidades vivas. Hoje o foco é edição de mapas (biomas, assentamentos) e associação básica de dados. A visão de futuro evolui esse projeto para um gerador e simulador narrativo interativo: um ecossistema que combina gestão de mundo (worldbuilding), automação narrativa com IA e mecânicas emergentes inspiradas em experiências como Dwarf Fortress.

---
## 🔭 Visão Evolutiva
O objetivo é transformar dados estruturados do mundo em histórias dinâmicas e coerentes. Três pilares orientam o design:

1. Worldbuilding: cadastro e organização de personagens, facções, locais, nações, eventos, itens e linhas do tempo.
2. Simulação: evolução sistêmica das relações (alianças, guerras, comércio, desastres, mudanças culturais) por "ticks" temporais e regras probabilísticas + heurísticas.
3. Narrativa Emergente: geração de notícias, crônicas e resumos diegéticos sobre os eventos mais relevantes; um "jornal do mundo" com tom configurável.

📝 Exemplo narrativo gerado:
"Na fortaleza de Durnhelm, rumores dizem que o Conde Varric foi envenenado. A Casa Mourn mobiliza seus guardas enquanto o comércio de especiarias permanece suspenso no porto de Atheria." 

---
## ✅ Estado Atual (MVP Implementado)
Recursos já disponíveis no repositório:
- Upload de imagem de mapa (MapaMundo) com detecção de largura/altura.
- Desenho e edição de áreas (Biomas) via polígonos Leaflet.draw.
- Criação de assentamentos clicando no mapa (coordenadas em pixel).
- Atribuição automática de bioma a assentamentos dentro de polígonos.
- Visualização opcional das camadas de biomas.
- Modelos prontos para relacionar personagens a assentamentos.

---
## 🧩 Arquitetura Futura (Proposta)
### 1. Backend (Core / API)
Base atual: Django + Django REST Framework.
Futuro: manter DRF ou avaliar migração/serviço complementar em FastAPI para componentes de alta performance.

Modelos planejados (alguns já implícitos ou parcialmente existentes):
- World
- Faction (reinos, impérios, guildas)
- Character
- Location (cidades, fortalezas, regiões)
- Biome (já existente como Bioma/Mapa)
- Settlement (assentamentos – já existente)
- Event (instâncias de acontecimentos discretos)
- Timeline (agregações e cortes temporais)
- NewsArticle (texto gerado pela IA)

Banco: migrar para PostgreSQL (melhor para relacionamentos, queries avançadas e extensões futuras como PostGIS se coordenadas geográficas forem adotadas).

### 2. Motor Narrativo / IA
Modularidade em três camadas:
1. Extração de Fatos: consolida estado (quem, onde, quando, o quê) dos modelos.
2. Interpretação Contextual (IA + regras): avalia relevância, impacto, causalidade e escalonamento de tensão.
3. Redação Estilizada: gera texto jornalístico, épico, sombrio ou futurista conforme "perfil de mundo".

### 3. Simulador de Mundo
Primeira versão: probabilidade de eventos baseada em atributos e relações.
Exemplo:
```python
if faction_a.is_at_war_with(faction_b) and random() < 0.2:
    create_event("Battle", location=random_border_city())
```
Evolução: incorporar métricas como estabilidade política, moral, clima, recursos, trade routes.

### 4. Frontend
Fase atual: templates Django + Leaflet.
Futuro: Next.js + Tailwind para painel rico e feed dinâmico; potencial app móvel (React Native) para interface de jogadores.

Funcionalidades previstas:
- Painel do mestre: CRUD avançado + visualizações relacionais.
- Mapa interativo com camadas temporais (time slider / playback).
- Feed de notícias e crônicas (rolagem infinita / busca por período).
- Área de jogador: inventário, diários e impacto direto em eventos.

### 5. Pipelines de Processamento
```
Estado do Mundo -> (Regra + IA estrutural) -> Eventos -> (Ranking/Relevância) -> Notícias -> (Armazenamento + Indexação)
```
Cache e fila: usar Celery + Redis para ticks e geração assíncrona de artigos.

---
## 🧠 Pipeline de Geração de Notícias
1. Seleção de eventos brutos.
2. Filtragem (relevância, diversidade temática, evitar redundância).
3. Enriquecimento contextual (antecedentes, consequências prováveis).
4. Redação IA (prompt baseado em estilo configurado por mundo + guardrails para tons inadequados).
5. Pós-processamento (checar referências existentes, evitar contradições, adicionar metadados).

### Estilos (Prompting)
Manter templates fixos por estilo:
- Fantasia Épica
- Ficção Científica
- Terror Gótico
- Solar Punk
Cada template define vocabulário, tom, densidade de detalhes e formalidade.

---
## 🛠 Tecnologias Atuais
- Django 5
- Django REST Framework
- Leaflet + Leaflet.draw
- python-dotenv (variáveis de ambiente)

Planejadas / Futuras:
- PostgreSQL / PostGIS
- Celery + Redis (jobs/ticks)
- Vetorização (FAISS ou pgvector) para memória contextual.
- Modelos de linguagem (via API externa ou servidor próprio) para geração narrativa.

---
## 📁 Estrutura Principal
```
manage.py
setup/            # Configurações Django
mapa/             # App principal (models, views, serializers)
templates/        # Templates (map_list, map_detail, bioma_editor, login)
media/            # Uploads (mapas enviados)
```

---
## 🔐 Variáveis de Ambiente
Copiar `/.env.example` para `.env` e ajustar:
```
DJANGO_SECRET_KEY=uma-string-grande-aleatoria
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```
Não versionar o `.env` real.

---
## 🚀 Instalação
```bash
# Clonar
git clone <URL_DO_REPO>
cd RPDjango

# Criar venv (opcional)
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar .env
cp .env.example .env

# Migrar banco
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

---
## 🧪 Fluxo de Uso Atual
1. Acesse `/admin/` e faça login.
2. Crie um `MapaMundo` enviando a imagem base.
3. Vá para `/` (dashboard) e abra o mapa desejado.
4. Na página do mapa (`/mapas/<id>/`) clique para capturar X/Y e criar assentamentos.
5. Use "Editar Biomas" para desenhar polígonos e salvar biomas.
6. Alternar "Mostrar Biomas" para visualizar camadas.
7. Assentamentos dentro de biomas recebem ligação automática.

---
## 🌐 Endpoints Principais (API)
- `POST /api/mapas/` – cria mapa (imagem)
- `GET /api/mapas/latest/` – último mapa
- `GET /api/assentamentos/markers/?mapa=<id>` – lista leve de assentamentos
- `POST /api/assentamentos/` – cria assentamento (`nome`, `tipo`, `pos_x`, `pos_y`, `mapa`, opcional `_bioma_ids`)
- `GET /api/biomas/?mapa=<id>` – lista biomas de um mapa
- `POST /api/biomas/` – cria bioma (`nome`, `tipo`, `cor`, `mapa`, `poligonos`)
- `PUT /api/biomas/<id>/` – atualiza bioma (substitui polígonos)
- `DELETE /api/biomas/<id>/` – remove bioma

### Representação de Polígonos
```json
[
  [
    [[x,y],[x,y],...],
    [[x,y],[x,y],...]
  ]
]
```
Cada polígono: lista de vértices em coordenadas de pixel.

---
## 🔄 Roadmap Evolutivo (Sugerido)
### Fase 0 (MVP) – Concluído Parcial
- Upload mapa, biomas, assentamentos.

### Fase 1 – Estrutura de Mundo
- Adicionar entidades: Faction, Location, Event.
- Migrar para PostgreSQL.

### Fase 2 – Simulação Básica
- Rotina de "tick" temporal (Celery).
- Regras probabilísticas iniciais (conflitos, comércio, desastres).

### Fase 3 – Narrativa Emergente
- Pipeline de eventos -> artigos.
- Geração de notícias estilizadas.

### Fase 4 – Interação de Jogadores
- Área de jogador, ações que influenciam estado.
- Eventos reagindo a entradas humanas.

### Fase 5 – Profundidade e Expansões
- Vetorização de memória e contexto.
- Exportação de crônicas (PDF/e-book).
- Imagens geradas (retratos/mapas estilizados).

---
## 🛡 Segurança / Produção
- SECRET_KEY forte e protegido.
- `DJANGO_ALLOWED_HOSTS` configurado.
- Servir `media/` por Nginx/Apache.
- HTTPS, cabeçalhos de segurança (CSP, HSTS), cache.

---
## 🔧 Próximas Ideias
- Modal de detalhes de assentamento + criação inline de personagens.
- Prioridade/overlap de biomas (camadas com z-index lógico).
- Import/Export JSON do mundo.
- Testes automatizados (pytest) para endpoints e simulação.
- Suporte multi-mapas na UI principal.
- Módulo de timeline visual interativa.

---
## 🗃 Licença
Defina a licença (ex: MIT) e adicione arquivo `LICENSE`.

---
Boa exploração do mundo e das histórias emergentes! 🎲

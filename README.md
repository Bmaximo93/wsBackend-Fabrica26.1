# 🔥CopyTaste

Aplicação web para extrair e salvar receitas de vídeos do YouTube utilizando a API do Google Gemini.

<img width="1603" height="582" alt="image" src="https://github.com/user-attachments/assets/2d23a1c4-4888-4abf-8dc3-6441999e17a3" /> 
<img width="1417" height="1446" alt="image" src="https://github.com/user-attachments/assets/3706c765-cd95-4e1b-b7c3-255fdeb199ce" />

## Sobre

Sabe quando você salva um vídeo de receita no YouTube ou no Shorts para fazer depois, mas voce nunca faz porque acaba esquecendo? E quando finalmente vai cozinhar, precisa ficar pausando e reassistindo o vídeo a cada passo?

O CopyTaste é uma aplicação web que resolve esse problema. O usuário cria uma conta, cola o link de um vídeo de culinária do YouTube e a aplicação envia o vídeo para a API do Google Gemini, que analisa o conteúdo e extrai automaticamente uma receita estruturada: título, descrição, lista de ingredientes com quantidades, modo de preparo passo a passo e tempo estimado de preparo. Toda a resposta é validada através de um schema Pydantic com structured output, garantindo consistência nos dados antes mesmo de salvar no banco.

A receita fica salva na conta do usuário, funcionando como um livro de receitas digital pessoal. O usuário pode visualizar, editar e excluir suas receitas a qualquer momento, e o link do vídeo original fica sempre acessível na receita caso queira reassistir.

## Stack

- **Backend:** Django 6.x
- **Banco de dados:** PostgreSQL
- **IA:** Google Gemini API (gemini-2.5-flash)
- **Validação:** Pydantic v2
- **Frontend:** Django Templates + Bootstrap 5 (CDN)

## Como funciona

### Integração com Gemini

A extração de receitas utiliza a [API do Google Gemini](https://ai.google.dev/gemini-api/docs) através do SDK Python [`google-genai`](https://ai.google.dev/gemini-api/docs/libraries).

O vídeo do YouTube é enviado para o Gemini como um [`Part.from_uri`](https://ai.google.dev/gemini-api/docs/video-understanding) com `mime_type="video/youtube"`, permitindo que o modelo analise o conteúdo visual e de áudio do vídeo diretamente pela URL.

Para garantir que a resposta da IA siga uma estrutura consistente, a aplicação utiliza o [structured output](https://ai.google.dev/gemini-api/docs/structured-output) do Gemini. Um schema [Pydantic](https://docs.pydantic.dev/latest/) (`RecipeSchema`) é passado como `response_schema` na configuração da chamada, forçando o Gemini a retornar JSON no formato exato esperado. A resposta é então validada com `model_validate_json()` do Pydantic antes de ser salva no banco de dados.

O prompt instrui o modelo a:
- Extrair receitas mesmo de vídeos sem narração, inferindo a partir do conteúdo visual
- Retornar todos os campos de texto em português brasileiro, independente da lingua original do vídeo
- Inferir o tempo de preparo quando não explicitado no vídeo
- Manter ingredientes com suas quantidades juntos
- Separar cada passo como uma ação atômica individual
- Não fabricar informações que não estejam presentes no vídeo

### Modelo de dados

A aplicação utiliza um model `Recipe` que representa uma receita extraída de um vídeo. Cada receita pertence a um usuário através de uma relação de composição 1:N. O model utiliza `JSONField` para ingredientes e passos, aproveitando o suporte nativo do PostgreSQL a JSON para armazenar listas diretamente, sem necessidade de tabelas auxiliares. O ordering padrão é por `-created_at`.

**Campos do model Recipe:**

| Campo | Tipo | Descrição |
|---|---|---|
| `user` | `ForeignKey(User)` | Usuário dono da receita |
| `title` | `CharField(255)` | Título da receita |
| `description` | `TextField` | Descrição completa, exibida na página de detalhe |
| `summary` | `CharField(255)` | Resumo curto (~20 palavras), gerado pelo Gemini para os cards de preview |
| `ingredients` | `JSONField` | Lista de ingredientes com quantidades |
| `steps` | `JSONField` | Lista de passos do modo de preparo |
| `duration_minutes` | `IntegerField` | Tempo estimado de preparo em minutos (nullable, inferido pelo Gemini quando não explícito) |
| `source_url` | `URLField(300)` | Link original do vídeo do YouTube |
| `created_at` | `DateTimeField` | Data de criação (auto_now_add) |

### Autenticação

A aplicação utiliza o sistema de autenticação built-in do Django (`django.contrib.auth`). O registro usa `UserCreationForm` e o login usa `AuthenticationForm`. Todas as views de receitas são protegidas com `@login_required`, e cada usuário só tem acesso às suas próprias receitas.

### Formulários

- **RegisterForm:** Estende `UserCreationForm`, removendo os textos de ajuda padrão
- **AddRecipeForm:** Formulário simples com campo de URL do YouTube
- **EditRecipeForm:** `ModelForm` que converte os `JSONField` (ingredientes e passos) em textarea com um item por linha, e reconverte para lista no `clean`

Os formulários utilizam `django-crispy-forms` com `crispy-bootstrap5` para renderização.

## Como rodar localmente

### Com Docker (recomendado)

```bash
git clone https://github.com/Bmaximo93/wsBackend-Fabrica26.1.git
cd wsBackend-Fabrica26.1
cp .env.example .env
# Edite o .env e adicione sua GEMINI_API_KEY
docker compose up --build
```

Acesse em http://localhost:8000

### Sem Docker

```bash
git clone https://github.com/Bmaximo93/wsBackend-Fabrica26.1.git
cd wsBackend-Fabrica26.1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edite o .env com suas credenciais
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta do Django |
| `GEMINI_API_KEY` | Chave da API do Google Gemini |
| `DB_NAME` | Nome do banco PostgreSQL (sem essa variável, usa SQLite) |
| `DB_USER` | Usuário do PostgreSQL |
| `DB_PASSWORD` | Senha do PostgreSQL |
| `DB_HOST` | Host do banco (usar `db` no Docker) |
| `DB_PORT` | Porta do banco (padrão: 5432) |



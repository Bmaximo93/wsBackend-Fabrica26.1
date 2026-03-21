# CopyTaste

Aplicação web para extrair e salvar receitas de vídeos do YouTube utilizando a API do Google Gemini.

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

A aplicação utiliza um model `Recipe` que representa uma receita extraída de um vídeo. Cada receita pertence a um usuário através de uma relação de composição 1:N . O model utiliza `JSONField` para ingredientes e passos, aproveitando o suporte nativo do PostgreSQL a JSON para armazenar listas diretamente, sem necessidade de tabelas auxiliares. O ordering padrão é por `-created_at`.

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
| `created_at` | `DateTimeField` | Data de criação (auto\_now\_add) |



# Captura de mensagens do Discord com Python

Este projeto mostra o caminho correto para ler mensagens de um servidor do Discord usando a API oficial. O fluxo e assim:

1. Voce cria um bot no Discord Developer Portal.
2. Adiciona esse bot ao servidor.
3. Habilita o `Message Content Intent`.
4. Executa o script para capturar mensagens em tempo real.
5. Opcionalmente, baixa um pequeno historico inicial do canal.

## O que este exemplo faz

- Escuta novas mensagens em canais que o bot consegue acessar.
- Salva cada mensagem em `data/messages.jsonl`.
- Pode capturar tambem as ultimas `N` mensagens de um canal especifico quando inicia.

Cada linha do arquivo `jsonl` vira um registro JSON independente, o que facilita depois carregar no Python, Pandas ou Spark.

## Aviso importante

O caminho correto e usar um **bot**. Nao use token de usuario nem self-bot. Isso viola os termos do Discord e pode bloquear a conta.

## 1. Criar a aplicacao e o bot

1. Abra o Discord Developer Portal.
2. Clique em `New Application`.
3. Dê um nome para a aplicacao.
4. Entre em `Bot`.
5. Clique em `Reset Token` ou `Copy` para obter o token do bot.
6. Em `Privileged Gateway Intents`, habilite `Message Content Intent`.

Sem esse intent, o bot costuma receber a estrutura da mensagem, mas o campo `content` pode vir vazio.

## 2. Adicionar o bot ao servidor

1. No Developer Portal, entre em `OAuth2 > URL Generator`.
2. Marque `bot` em `Scopes`.
3. Em `Bot Permissions`, marque pelo menos:
   - `View Channels`
   - `Read Message History`
4. Abra a URL gerada.
5. Escolha o servidor onde voce tem permissao para adicionar bots.

## 3. Descobrir os IDs do servidor e do canal

1. No Discord, ative `Modo Desenvolvedor` nas configuracoes avancadas.
2. Clique com o botao direito no servidor e copie o ID do servidor.
3. Clique com o botao direito no canal e copie o ID do canal.

## 4. Preparar o ambiente

No PowerShell, dentro desta pasta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Depois edite o arquivo `.env` com os seus valores:

```env
DISCORD_BOT_TOKEN=cole_o_token_aqui
DISCORD_GUILD_ID=123456789012345678
DISCORD_CHANNEL_ID=123456789012345678
DISCORD_HISTORY_LIMIT=20
```

### Significado das variaveis

- `DISCORD_BOT_TOKEN`: token do bot.
- `DISCORD_GUILD_ID`: limita a captura a um servidor especifico.
- `DISCORD_CHANNEL_ID`: limita a captura a um canal especifico.
- `DISCORD_HISTORY_LIMIT`: quantas mensagens antigas buscar na inicializacao.

Se voce deixar `DISCORD_HISTORY_LIMIT=0`, o bot captura so mensagens novas.

## 5. Executar

```powershell
python bot.py
```

Se tudo estiver certo, voce vai ver logs como:

```text
Bot conectado como MeuBot#1234.
Servidor alvo: MeuServidor (123456789012345678)
[LIVE] MeuServidor / #geral / usuario: ola pessoal
```

## 6. Estrutura do arquivo de saida

O arquivo `data/messages.jsonl` tera uma linha JSON por mensagem, por exemplo:

```json
{"id": 1, "created_at": "2026-07-26T18:00:00+00:00", "guild_id": 123, "guild_name": "MeuServidor", "channel_id": 456, "channel_name": "geral", "author_id": 789, "author_name": "usuario", "content": "ola pessoal", "attachments": [], "capture_source": "live"}
```

## 7. Ler os dados depois no Python

Exemplo rapido com Pandas:

```python
import pandas as pd

df = pd.read_json("data/messages.jsonl", lines=True)
print(df.head())
```

## 8. Limites e observacoes

- O bot so enxerga canais em que foi adicionado e tem permissao.
- O bot nao entra em servidores sozinho; voce precisa autoriza-lo pela URL OAuth2.
- Se quiser minerar muito historico, faca isso com cuidado para nao gerar duplicidade nos arquivos.
- Para analise etica, avise os participantes do minicurso que as mensagens estao sendo coletadas.

## 9. Proximo passo sugerido

Depois que isso estiver funcionando, o passo natural e criar um notebook ou script de analise para:

- contar mensagens por usuario,
- medir horarios de maior atividade,
- extrair palavras frequentes,
- analisar sentimento ou temas.
# Slide 20 — Adicionando Auth ao MCP Server

## Arquivos

| Arquivo | O que é |
|---------|---------|
| `auth.py` | Módulo de autenticação: validação JWT + controle de escopos |
| `server_com_auth.py` | Server do LB2 evoluído com auth (middleware + escopos) |
| `demo_auth.py` | Demo dos 3 cenários: sem token, sem escopo, com escopo |

## Setup

```bash
pip install mcp PyJWT
```

## Como testar

### 1. Rodar a demo de auth (sem server)
```bash
python demo_auth.py
```

### 2. Gerar tokens de teste
```bash
python auth.py
```

### 3. Rodar o server
```bash
python server_com_auth.py
```

## Escopos disponíveis

| Escopo | Acesso |
|--------|--------|
| `tools:aprovar_ferias` | Executar apenas aprovar_ferias |
| `tools:criar_solicitacao` | Executar apenas criar_solicitacao |
| `tools:enviar_resposta` | Executar apenas enviar_resposta |
| `tools:*` | Executar qualquer tool |
| `resources:read` | Ler qualquer resource |
| `resources:*` | Acesso total a resources |
| `prompts:read` | Ativar qualquer prompt |
| `prompts:*` | Acesso total a prompts |

## Para produção

Troque em `auth.py`:
- `SECRET_KEY` → public key do seu IdP (RS256)
- `ALGORITHM` → `"RS256"`
- `ISSUER` → URL do seu IdP (ex: `https://empresa.auth0.com/`)

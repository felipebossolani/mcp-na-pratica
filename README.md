# MCP na Prática

Código-fonte do curso "Model Context Protocol (MCP) e padrões abertos para integração de IA".

## Estrutura

```
mcp-na-pratica/
├── lb2-code/                # LB2 — Construindo MCP Servers na prática
│   ├── slide-05/            # Server mínimo (10 linhas)
│   ├── slide-06/            # Demo no Inspector
│   ├── slide-08/            # Tools (@server.tool)
│   ├── slide-09/            # Resources (@server.resource)
│   ├── slide-10/            # Prompts (@server.prompt)
│   ├── slide-11/            # Server completo do copiloto de RH
│   ├── slide-14/            # Transports: stdio vs HTTP
│   ├── slide-15/            # Erros comuns (print vs stderr)
│   ├── slide-19/            # Config do Claude Desktop
│   ├── slide-25/            # Desafio + solução
│   └── README.md
│
├── lb3-code/                # LB3 — Segurança, Auth e Arquiteturas
│   ├── slide-20/            # Auth com OAuth 2.1
│   │   ├── auth.py          # Módulo de validação JWT + escopos
│   │   ├── server_com_auth.py
│   │   ├── demo_auth.py     # 3 cenários: 401, 403, 200
│   │   └── README.md
│   └── README.md
│
└── README.md                # Este arquivo
```

## Requisitos

- Python 3.10+
- Node.js 18+ (para o MCP Inspector)

## Setup

```bash
pip install mcp PyJWT
```

## Como usar

Rodar qualquer server:

```bash
python lb2-code/slide-11/server.py
```

Testar no MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

## Progressão do curso

**LB1** — O que é o MCP e por que ele importa (conceitual, sem código)

**LB2** — Construindo MCP Servers na prática

| Slide | Conteúdo |
|-------|----------|
| 5-6 | Server mínimo + demo no Inspector |
| 8 | Tools: aprovar_ferias |
| 9 | Resources: saldo-ferias, política |
| 10 | Prompts: responder-colaborador, aprovar-solicitacao |
| 11 | Server completo (3 tools + 3 resources + 2 prompts) |
| 14 | Transports: stdio vs HTTP |
| 15 | Erros comuns: print() quebra o protocolo |
| 25 | Desafio: expandir o copiloto |

**LB3** — Segurança, Authorization e Arquiteturas Multi-Agente

| Slide | Conteúdo |
|-------|----------|
| 20 | Auth com OAuth 2.1: middleware + escopos granulares |

## Referências

- [Spec MCP](https://spec.modelcontextprotocol.io)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

## Autor

Felipe Bossolani
# LB2 — Construindo MCP Servers na prática

Código-fonte dos slides do Learning Block 2 do curso MCP da Tera.

## Estrutura

```
lb2-code/
├── slide-05/           # Server mínimo (10 linhas)
│   └── server.py
├── slide-06/           # Demo no Inspector (mesmo server)
│   └── server.py
├── slide-08/           # Tools na prática (@server.tool)
│   └── server.py
├── slide-09/           # Resources na prática (@server.resource)
│   └── server.py
├── slide-10/           # Prompts na prática (@server.prompt)
│   └── server.py
├── slide-11/           # Server completo do copiloto de RH
│   └── server.py       # ← Server principal usado no resto do curso
├── slide-14/           # Transports: stdio vs HTTP
│   └── server.py
├── slide-15/           # Erros comuns (demo ao vivo)
│   ├── server_com_bug.py      # print() quebra o protocolo
│   └── server_corrigido.py    # sys.stderr funciona
├── slide-19/           # Config do Claude Desktop
│   └── claude_desktop_config.json
├── slide-25/           # Desafio: expandir o copiloto
│   ├── desafio.py             # Esqueleto com TODOs
│   └── desafio_solucao.py     # Solução completa
└── README.md
```

## Setup

```bash
pip install mcp
```

## Como usar

### Rodar qualquer server
```bash
python slide-05/server.py
```

### Testar no MCP Inspector
```bash
npx @modelcontextprotocol/inspector
```

### Conectar ao Claude Desktop
Copie `slide-19/claude_desktop_config.json` para:
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

Ajuste o caminho do `server.py` e reinicie o Claude Desktop.

## Progressão dos slides

| Slide | Conteúdo | Primitivas |
|-------|----------|-----------|
| 5-6 | Server mínimo + demo | 1 tool (ping) |
| 8 | Tools | aprovar_ferias |
| 9 | Resources | saldo-ferias, politica-ferias |
| 10 | Prompts | responder-colaborador, aprovar-solicitacao |
| 11 | **Server completo** | **3 tools + 3 resources + 2 prompts** |
| 14 | Transports | stdio vs HTTP |
| 15 | Erros comuns | Bug com print() |
| 25 | Desafio | +1 tool, +1 resource, +1 prompt |

# Guia de Testes — MCP na Prática

Passo a passo para testar todos os servers do curso antes da gravação.

## Setup

```bash
cd mcp-na-pratica
source .venv/bin/activate
```

Em um segundo terminal:
```bash
npx @modelcontextprotocol/inspector
```

O Inspector abre no browser. Em todos os testes abaixo, use:
- Transport: **stdio**
- Command: **.venv/bin/python** (caminho completo do venv)
- Arguments: (muda por teste, indicado abaixo)

Entre cada teste: **Disconnect** no Inspector → Ctrl+C no terminal do server → rodar o próximo server → mudar Arguments no Inspector → **Connect**.

---

## Teste 1 — Slide 5/6 (Server mínimo)

**Terminal:**
```bash
python lb2/slide-05/server.py
```

**Inspector — Arguments:** `lb2/slide-05/server.py`

**Connect → Aba Tools:**
- Clicar em **ping**
- Clicar **Run**

**Resultado esperado:**
```
pong
```

---

## Teste 2 — Slide 8 (Tools)

**Terminal:**
```bash
python lb2/slide-08/server.py
```

**Inspector — Arguments:** `lb2/slide-08/server.py`

**Connect → Aba Tools:**
- Clicar em **aprovar_ferias**
- Preencher:
  - colaborador_id: `1`
  - data_inicio: `2026-03-01`
  - data_fim: `2026-03-15`
- Clicar **Run**

**Resultado esperado:**
```json
{
  "status": "aprovado",
  "protocolo": "MCP-2025-RH-0001",
  "colaborador": "Maria Silva",
  "periodo": "2026-03-01 a 2026-03-15",
  "notificacao_enviada": true
}
```

---

## Teste 3 — Slide 9 (Resources)

**Terminal:**
```bash
python lb2/slide-09/server.py
```

**Inspector — Arguments:** `lb2/slide-09/server.py`

**Connect → Aba Resources:**
- Clicar em **rh://colaboradores/{colaborador_id}/saldo-ferias**
- Preencher colaborador_id: `1`
- Clicar **Read**

**Resultado esperado:**
```json
{
  "colaborador": "Maria Silva",
  "saldo_dias": 15,
  "periodo_aquisitivo": "2024-2025",
  "vencimento": "2026-12-31"
}
```

Testar também:
- Clicar em **rh://politica/ferias-2025** → **Read**
- Deve retornar JSON com versao "2025.1" e lista de regras

---

## Teste 4 — Slide 10 (Prompts)

**Terminal:**
```bash
python lb2/slide-10/server.py
```

**Inspector — Arguments:** `lb2/slide-10/server.py`

**Connect → Aba Prompts:**
- Clicar em **responder_colaborador**
- Preencher:
  - colaborador_id: `1`
  - assunto: `férias`
- Clicar **Get Prompt**

**Resultado esperado:**
Template expandido contendo "Maria Silva" e "férias", com instruções de tom profissional e formato email corporativo.

Testar também:
- Clicar em **aprovar_solicitacao**
- Preencher colaborador_id: `1`, tipo_solicitacao: `férias`
- Deve retornar template com "Maria Silva" e instruções de aprovação

---

## Teste 5 — Slide 11 (Server completo)

**Terminal:**
```bash
python lb2/slide-11/server.py
```

**Inspector — Arguments:** `lb2/slide-11/server.py`

**Connect → Verificar as 3 abas:**

**Aba Tools (3 tools):**
- aprovar_ferias
- criar_solicitacao
- enviar_resposta

Testar **aprovar_ferias**:
- colaborador_id: `1`, data_inicio: `2026-03-01`, data_fim: `2026-03-15`
- Resultado: status "aprovado", protocolo gerado

Testar **criar_solicitacao**:
- tipo: `ferias`, descricao: `Solicitação de férias março`, prioridade: `media`
- Resultado: status "criada", protocolo gerado

Testar **enviar_resposta**:
- colaborador_id: `1`, mensagem: `Suas férias foram aprovadas conforme solicitado.`
- Resultado: status "enviado", destinatario "maria.silva@empresa.com"

**Aba Resources (3 resources):**
- rh://colaboradores/{colaborador_id}/saldo-ferias → colaborador_id: `1` → saldo_dias 15
- rh://politica/ferias-2025 → JSON com regras
- rh://colaboradores/{colaborador_id}/dados → colaborador_id: `1` → nome, depto, cargo, email

**Aba Prompts (2 prompts):**
- responder_colaborador → colaborador_id: `1`, assunto: `férias` → template expandido
- aprovar_solicitacao → colaborador_id: `1`, tipo_solicitacao: `férias` → template de aprovação

---

## Teste 6 — Slide 14 (Transports)

**Teste HTTP:**
```bash
python lb2/slide-14/server.py --http
```
Verificar no terminal: `Iniciando em modo HTTP (streamable-http)...`
Ctrl+C.

**Teste stdio:**
```bash
python lb2/slide-14/server.py
```
Inspector — Arguments: `lb2/slide-14/server.py`
Connect → Aba Tools → aprovar_ferias deve aparecer e funcionar.
Ctrl+C.

---

## Teste 7 — Slide 15 (Erro de retorno inválido)

**Teste do bug:**
```bash
python lb2/slide-15/server_com_bug.py
```

Inspector — Arguments: `lb2/slide-15/server_com_bug.py`
Connect → funciona normalmente, tool "ping" aparece na lista.
Clicar em **ping** → **Run** → deve dar **ERRO**. O retorno é um objeto não-serializável.
O terminal fica silencioso — nenhuma pista do erro. Esse é o ponto: sem o Inspector, você não saberia onde está o problema.
Ctrl+C.

**Teste da correção:**
```bash
python lb2/slide-15/server_corrigido.py
```

Inspector — Arguments: `lb2/slide-15/server_corrigido.py`
Connect → Aba Tools → **ping** → Run → deve retornar "pong" normalmente.
No terminal, aparece `debug: ping chamado` (via sys.stderr, sem interferir no protocolo).
Ctrl+C.

---

## Teste 8 — Slide 20 (Auth)

Esses testes não precisam do Inspector.

**Teste 8a — Gerar e validar tokens:**
```bash
python lb3/slide-20/auth.py
```

**Resultado esperado:**
```
=== Gerando tokens de teste ===

Token admin (acesso total):
eyJ... (token longo)

Token restrito (só aprovar_ferias + resources):
eyJ... (token longo)

=== Validando token admin ===
Sub: admin-rh
Scopes: ['tools:*', 'resources:*', 'prompts:*']
Válido!

=== Testando token inválido ===
Erro (esperado): Token inválido: ...

=== Testando sem token ===
Erro (esperado): Token não fornecido. ...
```

**Teste 8b — 3 cenários de auth:**
```bash
python lb3/slide-20/demo_auth.py
```

**Resultado esperado:**
```
CENÁRIO 1: Sem token
🚨 401 Unauthorized: Token não fornecido

CENÁRIO 2: Token válido, escopo insuficiente
🚨 403 Forbidden: Escopo insuficiente

CENÁRIO 3: Token válido com escopo correto
✅ 200 OK: Autorizado!
   Resultado: {status: "aprovado", protocolo: "MCP-2025-RH-0848"}

BÔNUS: Wildcard (tools:*)
   ✅ aprovar_ferias: autorizado
   ✅ criar_solicitacao: autorizado
   ✅ enviar_resposta: autorizado
   ✅ transferir_departamento: autorizado
```

---

## Checklist final

- [ ] Slide 05: ping → pong
- [ ] Slide 08: aprovar_ferias → status aprovado
- [ ] Slide 09: saldo-ferias → saldo_dias 15
- [ ] Slide 10: responder_colaborador → template com Maria Silva
- [ ] Slide 11: 3 tools + 3 resources + 2 prompts funcionando
- [ ] Slide 14: --http mostra mensagem, sem flag roda stdio
- [ ] Slide 15: server_com_bug conecta mas ping dá erro, server_corrigido retorna "pong"
- [ ] Slide 20: auth.py gera tokens, demo_auth.py mostra 401 → 403 → 200
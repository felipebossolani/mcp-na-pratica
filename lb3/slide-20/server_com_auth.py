"""
server_com_auth.py — Copiloto de RH com autenticação OAuth 2.1
MCP Course - LB3 - Slide 20

Evolução do server do LB2 com:
- Middleware de validação de token JWT
- Escopos granulares por primitiva
- Separação: auth é camada acima, tool não muda

Dependências: pip install mcp PyJWT
"""

import json
import sys
from datetime import datetime

from mcp.server.fastmcp import FastMCP
from auth import validate_token, require_scope

server = FastMCP("rh-copilot")

# ============================================================
# MOCK DATA (mesmo do LB2)
# ============================================================

COLABORADORES = {
    "1": {
        "nome": "Maria Silva",
        "depto": "Engineering",
        "cargo": "Senior Developer",
        "email": "maria.silva@empresa.com",
        "saldo_ferias": 15,
        "vencimento": "2026-12-31",
        "historico": [],
    },
    "2": {
        "nome": "João Santos",
        "depto": "Product",
        "cargo": "Product Manager",
        "email": "joao.santos@empresa.com",
        "saldo_ferias": 20,
        "vencimento": "2026-06-30",
        "historico": [],
    },
    "3": {
        "nome": "Ana Costa",
        "depto": "Design",
        "cargo": "UX Designer",
        "email": "ana.costa@empresa.com",
        "saldo_ferias": 10,
        "vencimento": "2026-12-31",
        "historico": [],
    },
    "4": {
        "nome": "Pedro Lima",
        "depto": "Engineering",
        "cargo": "Tech Lead",
        "email": "pedro.lima@empresa.com",
        "saldo_ferias": 5,
        "vencimento": "2026-03-31",
        "historico": [],
    },
    "5": {
        "nome": "Carla Souza",
        "depto": "HR",
        "cargo": "HR Business Partner",
        "email": "carla.souza@empresa.com",
        "saldo_ferias": 25,
        "vencimento": "2026-12-31",
        "historico": [],
    },
}

POLITICA_FERIAS = {
    "versao": "2025.1",
    "min_dias_antecedencia": 30,
    "max_dias_consecutivos": 30,
    "periodo_aquisitivo_meses": 12,
    "abono_pecuniario": True,
    "regras": [
        "Férias devem ser solicitadas com 30 dias de antecedência",
        "Máximo de 30 dias consecutivos por período",
        "Possibilidade de fracionamento em até 3 períodos",
        "Um dos períodos deve ter no mínimo 14 dias",
        "Abono pecuniário de 1/3 pode ser solicitado",
    ],
}

_protocolo_seq = 847


def _proximo_protocolo() -> str:
    global _protocolo_seq
    _protocolo_seq += 1
    return f"MCP-2025-RH-{_protocolo_seq:04d}"


# ============================================================
# MIDDLEWARE DE AUTENTICAÇÃO
# ============================================================
# Em uma implementação real com FastMCP, o middleware intercepta
# toda requisição MCP antes de chegar nas tools/resources/prompts.
#
# O padrão exato depende da versão do SDK. Aqui mostramos o
# conceito — a lógica é a mesma independente da implementação.
#
# Fluxo:
#   1. Extrai token do header Authorization
#   2. Valida (assinatura, expiração, issuer)
#   3. Injeta claims no contexto da requisição
#   4. Se inválido, rejeita ANTES de qualquer tool/resource
# ============================================================

# @server.middleware
# async def auth_middleware(request, call_next):
#     token = request.headers.get("Authorization")
#     try:
#         claims = validate_token(token)
#         request.state.user = claims
#         request.state.scopes = claims.get("scopes", [])
#         print(f"[AUTH] Usuário: {claims['sub']} | Escopos: {claims['scopes']}", file=sys.stderr)
#     except PermissionError as e:
#         print(f"[AUTH] Rejeitado: {e}", file=sys.stderr)
#         raise
#     return await call_next(request)


# ============================================================
# TOOLS (model-controlled — com escopos)
# ============================================================


@server.tool()
# @require_scope("tools:aprovar_ferias")  # ← escopo granular
def aprovar_ferias(colaborador_id: str, data_inicio: str, data_fim: str) -> dict:
    """Aprova solicitação de férias de um colaborador.

    Recebe o ID do colaborador e o período desejado (formato YYYY-MM-DD).
    Valida se o colaborador existe e retorna confirmação com protocolo.
    Use quando o usuário pedir para aprovar férias de alguém.

    Requer escopo: tools:aprovar_ferias
    """
    if colaborador_id not in COLABORADORES:
        return {"status": "erro", "mensagem": f"Colaborador {colaborador_id} não encontrado"}

    colaborador = COLABORADORES[colaborador_id]
    protocolo = _proximo_protocolo()

    colaborador["historico"].append({
        "tipo": "ferias",
        "data": data_inicio,
        "status": "aprovado",
        "protocolo": protocolo,
    })

    return {
        "status": "aprovado",
        "protocolo": protocolo,
        "colaborador": colaborador["nome"],
        "periodo": f"{data_inicio} a {data_fim}",
        "notificacao_enviada": True,
    }


@server.tool()
# @require_scope("tools:criar_solicitacao")
def criar_solicitacao(tipo: str, descricao: str, prioridade: str) -> dict:
    """Cria uma nova solicitação no sistema de RH.

    Tipos válidos: ferias, abono, transferencia, desligamento.
    Prioridades válidas: baixa, media, alta, urgente.
    Use quando o usuário pedir para criar ou abrir uma nova solicitação.

    Requer escopo: tools:criar_solicitacao
    """
    tipos_validos = ["ferias", "abono", "transferencia", "desligamento"]
    prioridades_validas = ["baixa", "media", "alta", "urgente"]

    if tipo not in tipos_validos:
        return {"status": "erro", "mensagem": f"Tipo inválido. Use: {', '.join(tipos_validos)}"}

    if prioridade not in prioridades_validas:
        return {"status": "erro", "mensagem": f"Prioridade inválida. Use: {', '.join(prioridades_validas)}"}

    protocolo = _proximo_protocolo()
    return {
        "status": "criada",
        "protocolo": protocolo,
        "tipo": tipo,
        "descricao": descricao,
        "prioridade": prioridade,
        "criado_em": datetime.now().isoformat(),
    }


@server.tool()
# @require_scope("tools:enviar_resposta")
def enviar_resposta(colaborador_id: str, mensagem: str) -> dict:
    """Envia uma resposta formal por email para um colaborador.

    Recebe o ID do colaborador e o texto da mensagem.
    Use quando o usuário pedir para enviar uma comunicação ou resposta.

    Requer escopo: tools:enviar_resposta
    """
    if colaborador_id not in COLABORADORES:
        return {"status": "erro", "mensagem": f"Colaborador {colaborador_id} não encontrado"}

    colaborador = COLABORADORES[colaborador_id]
    return {
        "status": "enviado",
        "destinatario": colaborador["email"],
        "nome": colaborador["nome"],
        "mensagem_preview": mensagem[:100] + "..." if len(mensagem) > 100 else mensagem,
        "enviado_em": datetime.now().isoformat(),
    }


# ============================================================
# RESOURCES (application-controlled — com escopos)
# ============================================================


@server.resource("rh://colaboradores/{colaborador_id}/saldo-ferias")
# @require_scope("resources:read")  # ← escopo por categoria
def saldo_ferias(colaborador_id: str) -> str:
    """Retorna o saldo de férias disponível do colaborador.

    Requer escopo: resources:read
    """
    if colaborador_id not in COLABORADORES:
        return json.dumps({"erro": f"Colaborador {colaborador_id} não encontrado"})

    dados = COLABORADORES[colaborador_id]
    return json.dumps({
        "colaborador": dados["nome"],
        "saldo_dias": dados["saldo_ferias"],
        "periodo_aquisitivo": "2024-2025",
        "vencimento": dados["vencimento"],
    })


@server.resource("rh://politica/ferias-2025")
# @require_scope("resources:read")
def politica_ferias() -> str:
    """Retorna a política de férias vigente da empresa.

    Requer escopo: resources:read
    """
    return json.dumps(POLITICA_FERIAS)


@server.resource("rh://colaboradores/{colaborador_id}/dados")
# @require_scope("resources:read")
def dados_colaborador(colaborador_id: str) -> str:
    """Retorna os dados cadastrais completos do colaborador.

    Requer escopo: resources:read
    """
    if colaborador_id not in COLABORADORES:
        return json.dumps({"erro": f"Colaborador {colaborador_id} não encontrado"})

    dados = COLABORADORES[colaborador_id]
    return json.dumps({
        "nome": dados["nome"],
        "departamento": dados["depto"],
        "cargo": dados["cargo"],
        "email": dados["email"],
        "total_solicitacoes": len(dados["historico"]),
    })


# ============================================================
# PROMPTS (user-controlled — com escopos)
# ============================================================


@server.prompt()
# @require_scope("prompts:read")
def responder_colaborador(colaborador_id: str, assunto: str) -> str:
    """Gera template de resposta formal para colaborador.

    Requer escopo: prompts:read
    """
    if colaborador_id not in COLABORADORES:
        return f"Colaborador {colaborador_id} não encontrado. Verifique o ID."

    dados = COLABORADORES[colaborador_id]
    return f"""Gere uma resposta formal para {dados["nome"]} ({dados["depto"]})
sobre {assunto}, incluindo:
- Prazos aplicáveis
- Próximos passos claros
- Referência à política da empresa quando relevante

Tom: profissional e empático.
Formato: email corporativo."""


@server.prompt()
# @require_scope("prompts:read")
def aprovar_solicitacao(colaborador_id: str, tipo_solicitacao: str) -> str:
    """Gera template de comunicação de aprovação de solicitação.

    Requer escopo: prompts:read
    """
    if colaborador_id not in COLABORADORES:
        return f"Colaborador {colaborador_id} não encontrado. Verifique o ID."

    dados = COLABORADORES[colaborador_id]
    return f"""Gere uma comunicação formal de aprovação para {dados["nome"]} ({dados["depto"]})
referente à solicitação de {tipo_solicitacao}.

Inclua:
- Confirmação da aprovação
- Número de protocolo (formato: MCP-2025-RH-XXXX)
- Datas relevantes
- Orientações sobre próximos passos
- Contato do RH para dúvidas

Tom: profissional, positivo e acolhedor.
Formato: email corporativo."""


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    print("[INFO] Iniciando rh-copilot com auth habilitado", file=sys.stderr)
    server.run()

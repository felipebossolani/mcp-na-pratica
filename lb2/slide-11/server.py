"""
Slide 11 — Copiloto de RH: server completo
MCP Course - LB2 - Cap 2.2

Server MCP completo com todas as primitivas:
- 3 Tools: aprovar_ferias, criar_solicitacao, enviar_resposta
- 3 Resources: saldo-ferias, politica-ferias, dados-colaborador
- 2 Prompts: responder-colaborador, aprovar-solicitacao

Mock data com 5 colaboradores fictícios (in-memory dict).
Sem banco de dados, sem API externa.
"""

import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")

# ============================================================
# MOCK DATA
# ============================================================

COLABORADORES = {
    "1": {
        "nome": "Maria Silva",
        "depto": "Engineering",
        "cargo": "Senior Developer",
        "email": "maria.silva@empresa.com",
        "saldo_ferias": 15,
        "vencimento": "2026-12-31",
        "historico": [
            {"tipo": "ferias", "data": "2025-07-01", "status": "aprovado"},
            {"tipo": "ferias", "data": "2025-01-15", "status": "aprovado"},
        ],
    },
    "2": {
        "nome": "João Santos",
        "depto": "Product",
        "cargo": "Product Manager",
        "email": "joao.santos@empresa.com",
        "saldo_ferias": 20,
        "vencimento": "2026-06-30",
        "historico": [
            {"tipo": "ferias", "data": "2025-06-01", "status": "aprovado"},
        ],
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
        "historico": [
            {"tipo": "ferias", "data": "2025-09-01", "status": "aprovado"},
            {"tipo": "ferias", "data": "2025-04-01", "status": "aprovado"},
            {"tipo": "ferias", "data": "2024-12-20", "status": "aprovado"},
        ],
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

# Contador de protocolos
_protocolo_seq = 847


def _proximo_protocolo() -> str:
    global _protocolo_seq
    _protocolo_seq += 1
    return f"MCP-2025-RH-{_protocolo_seq:04d}"


# ============================================================
# TOOLS (model-controlled — ações que mudam estado)
# ============================================================


@server.tool()
def aprovar_ferias(colaborador_id: str, data_inicio: str, data_fim: str) -> dict:
    """Aprova solicitação de férias de um colaborador.

    Recebe o ID do colaborador e o período desejado (formato YYYY-MM-DD).
    Valida se o colaborador existe e retorna confirmação com protocolo.
    Use quando o usuário pedir para aprovar férias de alguém.
    """
    if colaborador_id not in COLABORADORES:
        return {"status": "erro", "mensagem": f"Colaborador {colaborador_id} não encontrado"}

    colaborador = COLABORADORES[colaborador_id]
    protocolo = _proximo_protocolo()

    # Registra no histórico
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
def criar_solicitacao(tipo: str, descricao: str, prioridade: str) -> dict:
    """Cria uma nova solicitação no sistema de RH.

    Tipos válidos: ferias, abono, transferencia, desligamento.
    Prioridades válidas: baixa, media, alta, urgente.
    Use quando o usuário pedir para criar ou abrir uma nova solicitação.
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
def enviar_resposta(colaborador_id: str, mensagem: str) -> dict:
    """Envia uma resposta formal por email para um colaborador.

    Recebe o ID do colaborador e o texto da mensagem.
    Use quando o usuário pedir para enviar uma comunicação ou resposta.
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
# RESOURCES (application-controlled — leitura passiva)
# ============================================================


@server.resource("rh://colaboradores/{colaborador_id}/saldo-ferias")
def saldo_ferias(colaborador_id: str) -> str:
    """Retorna o saldo de férias disponível do colaborador."""
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
def politica_ferias() -> str:
    """Retorna a política de férias vigente da empresa."""
    return json.dumps(POLITICA_FERIAS)


@server.resource("rh://colaboradores/{colaborador_id}/dados")
def dados_colaborador(colaborador_id: str) -> str:
    """Retorna os dados cadastrais completos do colaborador."""
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
# PROMPTS (user-controlled — templates parametrizados)
# ============================================================


@server.prompt()
def responder_colaborador(colaborador_id: str, assunto: str) -> str:
    """Gera template de resposta formal para colaborador.

    Cria uma instrução estruturada para o LLM gerar uma resposta
    profissional e empática sobre o assunto solicitado.
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
def aprovar_solicitacao(colaborador_id: str, tipo_solicitacao: str) -> str:
    """Gera template de comunicação de aprovação de solicitação.

    Cria uma instrução para o LLM montar a comunicação formal
    de aprovação para o colaborador.
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
    server.run()

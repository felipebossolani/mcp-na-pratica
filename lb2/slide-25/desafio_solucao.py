"""
Slide 25 — Solução do desafio
MCP Course - LB2 - Cap 2.4

Solução completa com as 3 novas primitivas implementadas.
Compare com desafio.py para ver as diferenças.
"""

import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")

# Mock data
COLABORADORES = {
    "1": {"nome": "Maria Silva", "depto": "Engineering", "saldo_ferias": 15},
    "2": {"nome": "João Santos", "depto": "Product", "saldo_ferias": 20},
    "3": {"nome": "Ana Costa", "depto": "Design", "saldo_ferias": 10},
    "4": {"nome": "Pedro Lima", "depto": "Engineering", "saldo_ferias": 5},
    "5": {"nome": "Carla Souza", "depto": "HR", "saldo_ferias": 25},
}

# ============================================================
# Tools
# ============================================================


@server.tool()
def aprovar_ferias(colaborador_id: str, data_inicio: str, data_fim: str) -> dict:
    """Aprova solicitação de férias de um colaborador."""
    if colaborador_id not in COLABORADORES:
        return {"status": "erro", "mensagem": f"Colaborador {colaborador_id} não encontrado"}
    colaborador = COLABORADORES[colaborador_id]
    return {
        "status": "aprovado",
        "protocolo": f"MCP-2025-RH-{colaborador_id.zfill(4)}",
        "colaborador": colaborador["nome"],
    }


@server.tool()
def transferir_departamento(colaborador_id: str, novo_departamento: str) -> dict:
    """Transfere um colaborador para outro departamento.

    Atualiza o departamento do colaborador no sistema de RH.
    Use quando o usuário pedir para mover ou transferir um colaborador
    para um novo departamento ou equipe.
    """
    if colaborador_id not in COLABORADORES:
        return {"status": "erro", "mensagem": f"Colaborador {colaborador_id} não encontrado"}

    colaborador = COLABORADORES[colaborador_id]
    depto_anterior = colaborador["depto"]
    colaborador["depto"] = novo_departamento

    return {
        "status": "transferido",
        "colaborador": colaborador["nome"],
        "departamento_anterior": depto_anterior,
        "departamento_novo": novo_departamento,
        "efetivado_em": datetime.now().isoformat(),
    }


# ============================================================
# Resources
# ============================================================


@server.resource("rh://colaboradores/{colaborador_id}/saldo-ferias")
def saldo_ferias(colaborador_id: str) -> str:
    """Retorna o saldo de férias disponível do colaborador."""
    if colaborador_id not in COLABORADORES:
        return json.dumps({"erro": f"Colaborador {colaborador_id} não encontrado"})
    dados = COLABORADORES[colaborador_id]
    return json.dumps({"colaborador": dados["nome"], "saldo_dias": dados["saldo_ferias"]})


@server.resource("rh://departamentos/{depto_id}/headcount")
def headcount_departamento(depto_id: str) -> str:
    """Retorna o headcount e lista de colaboradores de um departamento.

    O depto_id deve corresponder ao nome do departamento
    (ex: Engineering, Product, Design, HR).
    """
    membros = [
        {"id": cid, "nome": c["nome"]}
        for cid, c in COLABORADORES.items()
        if c["depto"].lower() == depto_id.lower()
    ]

    return json.dumps({
        "departamento": depto_id,
        "headcount": len(membros),
        "colaboradores": membros,
    })


# ============================================================
# Prompts
# ============================================================


@server.prompt()
def responder_colaborador(colaborador_id: str, assunto: str) -> str:
    """Gera template de resposta formal para colaborador."""
    if colaborador_id not in COLABORADORES:
        return f"Colaborador {colaborador_id} não encontrado."
    dados = COLABORADORES[colaborador_id]
    return f"""Gere uma resposta formal para {dados["nome"]} sobre {assunto},
incluindo prazos e próximos passos. Tom: profissional e empático."""


@server.prompt()
def gerar_relatorio_mensal(departamento: str, mes: str) -> str:
    """Gera template para relatório mensal de um departamento.

    Cria instrução estruturada para o LLM montar um relatório
    gerencial com métricas, destaques e pontos de atenção.
    """
    # Busca dados do departamento
    membros = [c["nome"] for c in COLABORADORES.values() if c["depto"].lower() == departamento.lower()]

    return f"""Gere um relatório mensal gerencial para o departamento {departamento},
referente ao mês de {mes}.

Dados disponíveis:
- Headcount atual: {len(membros)} colaboradores
- Membros: {', '.join(membros) if membros else 'Nenhum encontrado'}

O relatório deve incluir:
1. Resumo executivo (2-3 linhas)
2. Headcount e movimentações
3. Solicitações processadas no período
4. Métricas de atendimento (SLA de aprovações)
5. Destaques positivos
6. Pontos de atenção e riscos
7. Plano de ação para o próximo mês

Formato: documento gerencial, objetivo e direto.
Tom: profissional, orientado a dados."""


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    server.run()

"""
Slide 25 — Desafio: expanda o copiloto de RH
MCP Course - LB2 - Cap 2.4

Exercício para o aluno implementar antes do LB3:
1. Nova Tool: transferir_departamento
2. Novo Resource: headcount por departamento
3. Novo Prompt: gerar relatório mensal

Este arquivo contém o esqueleto com TODOs para o aluno completar.
A solução está em desafio_solucao.py.
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
# Tools existentes (do server completo)
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


# ============================================================
# TODO 1: Nova Tool — transferir_departamento
# ============================================================
# Implemente uma tool que transfere um colaborador para outro departamento.
# Parâmetros: colaborador_id (str), novo_departamento (str)
# A tool deve:
#   - Validar se o colaborador existe
#   - Atualizar o departamento no dict
#   - Retornar confirmação com depto anterior e novo
#
# Dica: pense na docstring — como o LLM vai saber quando usar essa tool?
#
# @server.tool()
# def transferir_departamento(...) -> dict:
#     """..."""
#     pass


# ============================================================
# Resources existentes
# ============================================================


@server.resource("rh://colaboradores/{colaborador_id}/saldo-ferias")
def saldo_ferias(colaborador_id: str) -> str:
    """Retorna o saldo de férias disponível do colaborador."""
    if colaborador_id not in COLABORADORES:
        return json.dumps({"erro": f"Colaborador {colaborador_id} não encontrado"})
    dados = COLABORADORES[colaborador_id]
    return json.dumps({"colaborador": dados["nome"], "saldo_dias": dados["saldo_ferias"]})


# ============================================================
# TODO 2: Novo Resource — headcount por departamento
# ============================================================
# Implemente um resource com URI: rh://departamentos/{depto_id}/headcount
# Deve retornar:
#   - Nome do departamento
#   - Quantidade de colaboradores
#   - Lista de nomes
#
# Dica: itere sobre COLABORADORES filtrando por depto.
#
# @server.resource("rh://departamentos/{depto_id}/headcount")
# def headcount_departamento(...) -> str:
#     """..."""
#     pass


# ============================================================
# Prompts existentes
# ============================================================


@server.prompt()
def responder_colaborador(colaborador_id: str, assunto: str) -> str:
    """Gera template de resposta formal para colaborador."""
    if colaborador_id not in COLABORADORES:
        return f"Colaborador {colaborador_id} não encontrado."
    dados = COLABORADORES[colaborador_id]
    return f"""Gere uma resposta formal para {dados["nome"]} sobre {assunto},
incluindo prazos e próximos passos. Tom: profissional e empático."""


# ============================================================
# TODO 3: Novo Prompt — gerar relatório mensal
# ============================================================
# Implemente um prompt que gera template para relatório mensal de departamento.
# Parâmetros: departamento (str), mes (str)
# O template deve instruir o LLM a gerar:
#   - Resumo de headcount
#   - Solicitações do período
#   - Métricas e destaques
#   - Pontos de atenção
#
# @server.prompt()
# def gerar_relatorio_mensal(...) -> str:
#     """..."""
#     pass


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    server.run()

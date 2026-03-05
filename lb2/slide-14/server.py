"""
Slide 14 — Na prática: uma linha muda o transport
MCP Course - LB2 - Cap 2.3

Demonstra que o mesmo server roda em stdio ou HTTP
mudando apenas o argumento de server.run().

Para testar:
  stdio:   python server.py
  HTTP:    python server.py --http
"""

import json
import sys

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")

# Mock data (simplificado)
COLABORADORES = {
    "1": {"nome": "Maria Silva", "depto": "Engineering", "saldo_ferias": 15, "vencimento": "2026-12-31"},
    "2": {"nome": "João Santos", "depto": "Product", "saldo_ferias": 20, "vencimento": "2026-06-30"},
}


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
        "periodo": f"{data_inicio} a {data_fim}",
    }


@server.resource("rh://colaboradores/{colaborador_id}/saldo-ferias")
def saldo_ferias(colaborador_id: str) -> str:
    """Retorna o saldo de férias disponível do colaborador."""
    if colaborador_id not in COLABORADORES:
        return json.dumps({"erro": f"Colaborador {colaborador_id} não encontrado"})
    dados = COLABORADORES[colaborador_id]
    return json.dumps({"colaborador": dados["nome"], "saldo_dias": dados["saldo_ferias"]})


if __name__ == "__main__":
    # ============================================================
    # OPÇÃO 1: stdio (padrão — dev local, Claude Desktop, Inspector)
    # ============================================================
    # server.run()
    # ou explicitamente:
    # server.run(transport="stdio")

    # ============================================================
    # OPÇÃO 2: Streamable HTTP (produção, múltiplos clients)
    # ============================================================
    # server.run(transport="streamable-http", host="0.0.0.0", port=8000)

    # ============================================================
    # Detecta argumento de linha de comando pra facilitar a demo
    # ============================================================
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        print("Iniciando em modo HTTP (streamable-http)...", file=sys.stderr)
        server.run(transport="streamable-http")
    else:
        server.run()  # stdio (padrão)
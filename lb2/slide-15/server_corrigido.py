"""
Slide 15 — Versão corrigida: usar sys.stderr para debug
MCP Course - LB2 - Cap 2.3

Correção: trocar print() por print(..., file=sys.stderr).
O stderr é separado do stdout e não interfere no JSON-RPC.
"""

import sys

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")

# ✅ CORRETO: stderr não interfere no protocolo
print("debug: server iniciando...", file=sys.stderr)


@server.tool()
def ping() -> str:
    """Verifica se o server está ativo"""
    print("debug: ping chamado", file=sys.stderr)  # ✅ OK
    return "pong"


if __name__ == "__main__":
    server.run()

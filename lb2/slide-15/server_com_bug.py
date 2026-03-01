"""
Slide 15 — Erros comuns: print() quebra o protocolo
MCP Course - LB2 - Cap 2.3

DEMO AO VIVO:
1. Rodar este arquivo: python server_com_bug.py
2. Abrir o Inspector: npx @modelcontextprotocol/inspector
3. Inspector FALHA — o print() contaminou o stdout
4. Corrigir: trocar print() por print(..., file=sys.stderr)
5. Rodar server_corrigido.py — funciona!
"""

# ============================================================
# VERSÃO COM BUG — print() no stdout quebra o JSON-RPC
# ============================================================

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")

# ⚠️ ESSE PRINT QUEBRA TUDO!
# stdout é o canal do JSON-RPC no transport stdio.
# Qualquer coisa impressa aqui vira lixo no protocolo.
print("debug: server iniciando...")  # ← BUG!


@server.tool()
def ping() -> str:
    """Verifica se o server está ativo"""
    print("debug: ping chamado")  # ← BUG!
    return "pong"


if __name__ == "__main__":
    server.run()

"""
Slide 15 — Erros comuns: retorno inválido quebra o protocolo
MCP Course - LB2 - Cap 2.3

DEMO AO VIVO:
1. Rodar este arquivo: python server_com_bug.py
2. Abrir o Inspector: npx @modelcontextprotocol/inspector
3. Executar a tool ping → ERRO
4. Corrigir: ver server_corrigido.py
"""

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")


@server.tool()
def ping() -> str:
    """Verifica se o server está ativo"""
    # ⚠️ BUG: retorna um tipo que o protocolo não consegue serializar
    # MCP espera str, dict, ou lista — não um objeto arbitrário
    class Resultado:
        status = "ok"
    return Resultado()  # ← BUG! Objeto não-serializável


if __name__ == "__main__":
    server.run()
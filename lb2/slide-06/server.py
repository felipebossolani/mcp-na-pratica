"""
Slide 6 — Demo: server rodando no Inspector
MCP Course - LB2 - Cap 2.1

Mesmo server mínimo do Slide 5.
Usado para demonstrar ao vivo:
  1. python server.py
  2. npx @modelcontextprotocol/inspector
  3. Testar tool ping no Inspector
"""

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")


@server.tool()
def ping() -> str:
    """Verifica se o server está ativo"""
    return "pong"


if __name__ == "__main__":
    server.run()

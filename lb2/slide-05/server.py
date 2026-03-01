"""
Slide 5 — Server mínimo: 10 linhas de código
MCP Course - LB2 - Cap 2.1

Server MCP mínimo funcional usando FastMCP.
Demonstra: decorador @server.tool(), docstring como descrição, type hints.
"""

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")


@server.tool()
def ping() -> str:
    """Verifica se o server está ativo"""
    return "pong"


if __name__ == "__main__":
    server.run()

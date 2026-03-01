"""
Slide 8 — Tools na prática: @server.tool()
MCP Course - LB2 - Cap 2.2

Demonstra implementação de Tools MCP:
- Decorador @server.tool()
- Type hints geram JSON Schema automaticamente
- Docstring vira descrição da tool pro LLM
- Retorno estruturado (dict)
"""

from mcp.server.fastmcp import FastMCP

server = FastMCP("rh-copilot")

# Mock data
COLABORADORES = {
    "1": {"nome": "Maria Silva", "depto": "Engineering", "saldo_ferias": 15, "vencimento": "2026-12-31"},
    "2": {"nome": "João Santos", "depto": "Product", "saldo_ferias": 20, "vencimento": "2026-06-30"},
    "3": {"nome": "Ana Costa", "depto": "Design", "saldo_ferias": 10, "vencimento": "2026-12-31"},
    "4": {"nome": "Pedro Lima", "depto": "Engineering", "saldo_ferias": 5, "vencimento": "2026-03-31"},
    "5": {"nome": "Carla Souza", "depto": "HR", "saldo_ferias": 25, "vencimento": "2026-12-31"},
}


@server.tool()
def aprovar_ferias(colaborador_id: str, data_inicio: str, data_fim: str) -> dict:
    """Aprova solicitação de férias de um colaborador.

    Recebe o ID do colaborador e o período desejado.
    Valida se o colaborador existe e retorna confirmação com protocolo.
    """
    if colaborador_id not in COLABORADORES:
        return {"status": "erro", "mensagem": f"Colaborador {colaborador_id} não encontrado"}

    colaborador = COLABORADORES[colaborador_id]
    return {
        "status": "aprovado",
        "protocolo": f"MCP-2025-RH-{colaborador_id.zfill(4)}",
        "colaborador": colaborador["nome"],
        "periodo": f"{data_inicio} a {data_fim}",
        "notificacao_enviada": True,
    }


if __name__ == "__main__":
    server.run()

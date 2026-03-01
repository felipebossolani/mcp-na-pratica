"""
Slide 9 — Resources na prática: @server.resource()
MCP Course - LB2 - Cap 2.2

Demonstra implementação de Resources MCP:
- Decorador @server.resource() com URI template
- Leitura passiva, sem efeito colateral
- Application-controlled (host decide quando injetar no contexto)
- Diferença de Tool: Resource NÃO muda estado
"""

import json

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


if __name__ == "__main__":
    server.run()

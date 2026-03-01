"""
Slide 10 — Prompts na prática: @server.prompt()
MCP Course - LB2 - Cap 2.2

Demonstra implementação de Prompts MCP:
- Decorador @server.prompt()
- Template parametrizado que o usuário seleciona
- User-controlled (usuário escolhe quando ativar)
- Diferença de Tool: NÃO executa ação, prepara instrução pro LLM
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


@server.prompt()
def responder_colaborador(colaborador_id: str, assunto: str) -> str:
    """Gera template de resposta formal para colaborador.

    Cria uma instrução estruturada para o LLM gerar uma resposta
    profissional e empática sobre o assunto solicitado.
    """
    if colaborador_id not in COLABORADORES:
        return f"Colaborador {colaborador_id} não encontrado. Verifique o ID."

    dados = COLABORADORES[colaborador_id]
    return f"""Gere uma resposta formal para {dados["nome"]} ({dados["depto"]})
sobre {assunto}, incluindo:
- Prazos aplicáveis
- Próximos passos claros
- Referência à política da empresa quando relevante

Tom: profissional e empático.
Formato: email corporativo."""


@server.prompt()
def aprovar_solicitacao(colaborador_id: str, tipo_solicitacao: str) -> str:
    """Gera template de comunicação de aprovação de solicitação.

    Cria uma instrução para o LLM montar a comunicação formal
    de aprovação para o colaborador.
    """
    if colaborador_id not in COLABORADORES:
        return f"Colaborador {colaborador_id} não encontrado. Verifique o ID."

    dados = COLABORADORES[colaborador_id]
    return f"""Gere uma comunicação formal de aprovação para {dados["nome"]} ({dados["depto"]})
referente à solicitação de {tipo_solicitacao}.

Inclua:
- Confirmação da aprovação
- Número de protocolo (formato: MCP-2025-RH-XXXX)
- Datas relevantes
- Orientações sobre próximos passos
- Contato do RH para dúvidas

Tom: profissional, positivo e acolhedor.
Formato: email corporativo."""


if __name__ == "__main__":
    server.run()

"""
demo_auth.py — Demonstração dos 3 cenários de auth
MCP Course - LB3 - Slide 20

Roda 3 testes que mostram o comportamento do auth:
1. Sem token → 401 Unauthorized
2. Token válido sem escopo → 403 Forbidden
3. Token válido com escopo → 200 OK

Uso: python demo_auth.py
"""

from auth import validate_token, gerar_token_teste

SEPARADOR = "=" * 60


def cenario_1_sem_token():
    """Teste: requisição sem token."""
    print(f"\n{SEPARADOR}")
    print("CENÁRIO 1: Sem token")
    print(SEPARADOR)
    print("→ Simulando requisição sem header Authorization...")

    try:
        validate_token(None)
        print("✅ Aceito (INESPERADO!)")
    except PermissionError as e:
        print(f"🚨 401 Unauthorized: {e}")
        print("→ Comportamento correto: sem token, sem acesso.")


def cenario_2_token_sem_escopo():
    """Teste: token válido mas sem escopo necessário."""
    print(f"\n{SEPARADOR}")
    print("CENÁRIO 2: Token válido, escopo insuficiente")
    print(SEPARADOR)

    # Gera token com escopo limitado (só leitura de resources)
    token = gerar_token_teste(
        sub="agente-basico",
        scopes=["resources:read"],
    )
    print(f"→ Token gerado para 'agente-basico'")
    print(f"→ Escopos no token: ['resources:read']")
    print(f"→ Tentando executar tool que exige 'tools:aprovar_ferias'...")

    claims = validate_token(f"Bearer {token}")
    user_scopes = claims.get("scopes", [])
    required_scope = "tools:aprovar_ferias"

    if required_scope in user_scopes or "tools:*" in user_scopes:
        print("✅ Autorizado (INESPERADO!)")
    else:
        print(f"🚨 403 Forbidden: Escopo insuficiente.")
        print(f"   Necessário: {required_scope}")
        print(f"   Disponíveis: {user_scopes}")
        print("→ Comportamento correto: token válido, mas sem permissão pra essa tool.")


def cenario_3_token_com_escopo():
    """Teste: token válido com escopo correto."""
    print(f"\n{SEPARADOR}")
    print("CENÁRIO 3: Token válido com escopo correto")
    print(SEPARADOR)

    # Gera token com escopo completo
    token = gerar_token_teste(
        sub="admin-rh",
        scopes=["tools:aprovar_ferias", "tools:criar_solicitacao", "resources:read", "prompts:read"],
    )
    print(f"→ Token gerado para 'admin-rh'")
    print(f"→ Escopos no token: ['tools:aprovar_ferias', 'tools:criar_solicitacao', 'resources:read', 'prompts:read']")
    print(f"→ Tentando executar tool 'aprovar_ferias'...")

    claims = validate_token(f"Bearer {token}")
    user_scopes = claims.get("scopes", [])
    required_scope = "tools:aprovar_ferias"

    if required_scope in user_scopes or "tools:*" in user_scopes:
        print(f"✅ 200 OK: Autorizado!")
        print(f"   Usuário: {claims['sub']}")
        print(f"   Escopo: {required_scope} ∈ {user_scopes}")

        # Simula execução da tool
        resultado = {
            "status": "aprovado",
            "protocolo": "MCP-2025-RH-0848",
            "colaborador": "Maria Silva",
            "periodo": "2026-03-01 a 2026-03-15",
            "notificacao_enviada": True,
        }
        print(f"   Resultado: {resultado}")
        print("→ Comportamento correto: autenticado + autorizado = execução permitida.")
    else:
        print(f"🚨 403 Forbidden (INESPERADO!)")


def cenario_bonus_wildcard():
    """Teste: token com escopo wildcard."""
    print(f"\n{SEPARADOR}")
    print("BÔNUS: Token com escopo wildcard (tools:*)")
    print(SEPARADOR)

    token = gerar_token_teste(
        sub="super-admin",
        scopes=["tools:*", "resources:*", "prompts:*"],
    )
    print(f"→ Token gerado para 'super-admin'")
    print(f"→ Escopos: ['tools:*', 'resources:*', 'prompts:*']")

    claims = validate_token(f"Bearer {token}")
    user_scopes = claims.get("scopes", [])

    tools = ["aprovar_ferias", "criar_solicitacao", "enviar_resposta", "transferir_departamento"]
    for tool in tools:
        scope = f"tools:{tool}"
        autorizado = scope in user_scopes or "tools:*" in user_scopes
        status = "✅" if autorizado else "🚨"
        print(f"   {status} {tool}: {'autorizado' if autorizado else 'negado'}")

    print("→ Wildcard 'tools:*' autoriza qualquer tool. Use com cuidado.")


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     DEMO: 3 Cenários de Auth no MCP Server             ║")
    print("║     Copiloto de RH — LB3                               ║")
    print("╚══════════════════════════════════════════════════════════╝")

    cenario_1_sem_token()
    cenario_2_token_sem_escopo()
    cenario_3_token_com_escopo()
    cenario_bonus_wildcard()

    print(f"\n{SEPARADOR}")
    print("Resumo:")
    print("  Sem token         → 401 Unauthorized")
    print("  Token sem escopo  → 403 Forbidden")
    print("  Token com escopo  → 200 OK + execução")
    print("  Wildcard (tools:*)→ Acesso total a tools")
    print(SEPARADOR)

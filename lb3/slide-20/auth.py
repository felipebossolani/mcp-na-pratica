"""
auth.py — Módulo de autenticação e autorização para MCP Server
MCP Course - LB3 - Slide 20

Implementação didática de validação JWT e controle de escopos.
Em produção, troque a SECRET_KEY pela public key do seu IdP
(Auth0, Okta, Azure AD, Keycloak).

Dependências: pip install PyJWT
"""

import functools
import jwt

# ============================================================
# CONFIGURAÇÃO
# ============================================================

# Em produção: public key do IdP (RS256)
# Aqui usamos HS256 com secret para fins didáticos
SECRET_KEY = "mcp-curso-tera-secret-key-troque-em-producao"
ALGORITHM = "HS256"
ISSUER = "https://idp.empresa.com"


# ============================================================
# VALIDAÇÃO DE TOKEN
# ============================================================

def validate_token(token: str | None) -> dict:
    """Valida um JWT e retorna os claims.

    Verifica:
    - Presença do token
    - Assinatura (SECRET_KEY / public key)
    - Expiração (exp)
    - Emissor (iss)

    Retorna dict com claims: sub, scopes, exp, iss
    Levanta exceção se inválido.
    """
    if not token:
        raise PermissionError("Token não fornecido. Envie o header Authorization: Bearer <token>")

    # Remove prefixo "Bearer " se presente
    if token.startswith("Bearer "):
        token = token[7:]

    try:
        claims = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            options={"require": ["exp", "iss", "sub", "scopes"]},
        )
        return claims

    except jwt.ExpiredSignatureError:
        raise PermissionError("Token expirado. Solicite um novo token ao IdP.")
    except jwt.InvalidIssuerError:
        raise PermissionError(f"Emissor inválido. Esperado: {ISSUER}")
    except jwt.InvalidTokenError as e:
        raise PermissionError(f"Token inválido: {e}")


# ============================================================
# CONTROLE DE ESCOPOS
# ============================================================

def require_scope(scope: str):
    """Decorator que exige um escopo específico no token.

    Uso:
        @require_scope("tools:aprovar_ferias")
        def aprovar_ferias(...):
            ...

    O escopo é verificado contra a lista de escopos no token.
    Suporta wildcard: "tools:*" autoriza qualquer tool.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Busca claims no contexto (injetados pelo middleware)
            # Em implementação real, usar contextvars ou request.state
            user_scopes = kwargs.get("_user_scopes", [])

            # Verifica escopo exato ou wildcard
            scope_prefix = scope.split(":")[0] + ":*"
            if scope not in user_scopes and scope_prefix not in user_scopes:
                raise PermissionError(
                    f"Escopo insuficiente. Necessário: {scope}. "
                    f"Disponíveis: {', '.join(user_scopes)}"
                )

            # Remove _user_scopes antes de chamar a função original
            kwargs.pop("_user_scopes", None)
            return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================
# UTILITÁRIO: GERAR TOKEN DE TESTE
# ============================================================

def gerar_token_teste(
    sub: str = "agente-rh",
    scopes: list[str] | None = None,
    expira_em_min: int = 60,
) -> str:
    """Gera um JWT de teste para desenvolvimento.

    Uso:
        token = gerar_token_teste(
            sub="agente-rh",
            scopes=["tools:aprovar_ferias", "resources:read"]
        )

    NÃO use em produção — use tokens emitidos pelo IdP.
    """
    from datetime import datetime, timedelta, timezone

    if scopes is None:
        scopes = ["tools:*", "resources:*", "prompts:*"]

    payload = {
        "sub": sub,
        "scopes": scopes,
        "iss": ISSUER,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expira_em_min),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
# TESTE RÁPIDO
# ============================================================

if __name__ == "__main__":
    print("=== Gerando tokens de teste ===\n")

    # Token com acesso total
    token_admin = gerar_token_teste(sub="admin-rh", scopes=["tools:*", "resources:*", "prompts:*"])
    print(f"Token admin (acesso total):\n{token_admin}\n")

    # Token com acesso restrito
    token_restrito = gerar_token_teste(sub="agente-basico", scopes=["tools:aprovar_ferias", "resources:read"])
    print(f"Token restrito (só aprovar_ferias + resources):\n{token_restrito}\n")

    # Validar
    print("=== Validando token admin ===")
    claims = validate_token(f"Bearer {token_admin}")
    print(f"Sub: {claims['sub']}")
    print(f"Scopes: {claims['scopes']}")
    print(f"Válido!\n")

    # Testar token inválido
    print("=== Testando token inválido ===")
    try:
        validate_token("token-invalido-qualquer")
    except PermissionError as e:
        print(f"Erro (esperado): {e}\n")

    # Testar sem token
    print("=== Testando sem token ===")
    try:
        validate_token(None)
    except PermissionError as e:
        print(f"Erro (esperado): {e}")

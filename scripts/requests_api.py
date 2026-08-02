import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = "https://discord.com/api/v10"
TOKEN_AUTH = os.getenv("TOKEN_AUTH") 
GUILD_ID = str(os.getenv("GUILD_ID"))


def discord_get(path: str, token: str, params: dict[str, str] | None = None) -> dict | list:
    response = requests.get(
        f"{API_ENDPOINT}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=30,
    )
    if not response.ok:
        raise RuntimeError(
            f"Discord request failed ({response.status_code}): {response.text}"
        )
    return response.json()


def get_authorization_info(token: str) -> bool:
    permissions = discord_get("/oauth2/@me", token)
    print(f"Scopes autorizados: {', '.join(permissions.get('scopes', [])) if permissions.get('scopes') else 'nenhum'}")
    print()
    
    if "guilds" in permissions.get("scopes",[]):
        return True

    return False


def get_current_user_guilds(token: str) -> None:
    guilds = discord_get(
        "/users/@me/guilds",
        token,
        params={"with_counts": "true"},
    )
    if not isinstance(guilds, list):
        raise RuntimeError("Resposta inesperada ao listar guildas do usuario.")

    print("Servidores Encontrados:")
    pprint(guilds)


def get_guild_by_id(token:str) -> None:
    try:
        guild = discord_get(f"/guilds/{GUILD_ID}/preview", token, params={"with_counts": "true"})
    except RuntimeError as exc:
        if "403" in str(exc):
            return None
        raise

    print("Informações da Guilda:")
    pprint(guild)

def get_current_user_guild_member(token: str, guild_id: str) -> None:
    try:
        member = discord_get(f"/users/@me/guilds/{guild_id}/member", token)
    except RuntimeError as exc:
        if "403" in str(exc):
            return None
        raise
    if not isinstance(member, dict):
        raise RuntimeError("Resposta inesperada ao consultar o membro atual na guilda.")



if __name__ == "__main__":
    if not TOKEN_AUTH:
        raise SystemExit("Defina TOKEN_AUTH ou DISCORD_ACCESS_TOKEN com o bearer token OAuth2.")

    auth_info = get_authorization_info(TOKEN_AUTH)

    if not auth_info:
        raise SystemExit(
            "Esse token nao tem o scope 'guilds'. Gere um token OAuth2 com pelo menos 'identify guilds'."
        )

    ## get_current_user_guilds(TOKEN_AUTH)
    get_guild_by_id(TOKEN_AUTH)
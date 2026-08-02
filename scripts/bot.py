import json
import os
from pathlib import Path
from typing import Any

import discord
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0") or 0) or None
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0") or 0) or None

OUTPUT_PATH = Path("data/messages.jsonl")
OUTPUT_PATH.parent.mkdir(exist_ok=True)

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)
history_synced = False


def should_capture(message: discord.Message) -> bool:
    if message.author == client.user:
        return False

    if GUILD_ID and (message.guild is None or message.guild.id != GUILD_ID):
        return False

    return True


def serialize_message(message: discord.Message) -> dict[str, Any]:
    return {
        "id": message.id,
        "created_at": message.created_at.isoformat(),
        "edited_at": message.edited_at.isoformat() if message.edited_at else None,
        "guild_id": message.guild.id if message.guild else None,
        "guild_name": message.guild.name if message.guild else None,
        "channel_id": message.channel.id,
        "channel_name": getattr(message.channel, "name", str(message.channel)),
        "author_id": message.author.id,
        "author_server_name": str(message.author.name),
        "author_global_name": str(message.author.global_name),
        "bot": message.author.bot,
        "content": message.content,
        "mentions?": message.mentions,
        "mentioned_everyone?": message.mention_everyone,
        "attachments": [attachment.url for attachment in message.attachments],
        "type": message.type,
    }


def save_message(message: discord.Message, source: str) -> None:
    message_data = serialize_message(message)

    with OUTPUT_PATH.open("a", encoding="utf-8") as file:
        json.dump(message_data, file, ensure_ascii=False)
        file.write("\n")

    preview = message.content.strip() or "<mensagem sem texto>"
    preview = preview.replace("\n", " ")
    pprint(message)


@client.event
async def on_ready() -> None:
    print(f"Bot conectado como {client.user}.")

    if GUILD_ID:
        guild = client.get_guild(GUILD_ID)
        if guild is None:
            print("O bot conectou, mas nao encontrou o servidor configurado em cache.")
        else:
            print(f"Servidor alvo: {guild.name} ({guild.id})")


@client.event
async def on_message(message: discord.Message) -> None:
    if not should_capture(message):
        return

    save_message(message, source="live")


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "Defina DISCORD_BOT_TOKEN no arquivo .env antes de executar o bot."
        )

    client.run(TOKEN)
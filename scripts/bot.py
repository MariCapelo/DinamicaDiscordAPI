import discord

import json
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from pprint import pprint

# Capturando variaveis de ambiente do arquivo .env 
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0") or 0) or None
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0") or 0) or None

OUTPUT_PATH = Path("data/messages.jsonl")
OUTPUT_PATH.parent.mkdir(exist_ok=True)

# Configurando o bot do Discord com as intenções necessárias
# Isso é importante para que o bot possa receber eventos de mensagens e interagir com os servidores.
intents = discord.Intents.all()

# Criando uma instância do cliente do Discord com as intenções configuradas
client = discord.Client(intents=intents)

# Variável global para controlar o estado de mineração
minerar = False 

async def get_historic(message: discord.Message, num:int | None = None) -> list[discord.Message]:
    message_list = []
    count_messages = 0
    async for msg in message.channel.history(limit=num, before=message, oldest_first=False):
        count_messages += 1
        message_list.append(msg)

    await message.channel.send(f"{count_messages} mensagens capturadas.")
    return message_list


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
        "mentions?": True if message.mentions else False,
        "mentioned_everyone?": message.mention_everyone,
        "attachments": [attachment.url for attachment in message.attachments],
        "type": message.type,
    }


def save_message(message: discord.Message, source: str) -> None:
    message_data = serialize_message(message)
    message_data["source"] = source
    
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
    global minerar # Declarando a variável global para controle de mineração
    
    # Condicionais de controle de historico
    if message.content.startswith(".historico"):
        partes = message.content.split()
        if len(partes) == 2 and partes[1].isdigit():
            num = int(partes[1])
            historic_messages = await get_historic(message, num)
            for msg in historic_messages:
                save_message(msg, source="historic")
        elif len(partes) == 1:
            historic_messages = await get_historic(message)
            for msg in historic_messages:
                save_message(msg, source="historic")
    
    # Condicionais de controle de mineração      
    if message.content.startswith(".minerar") and minerar is False:
        await message.channel.send("oVo MiNeraR SEu seRViDoR :D")
        minerar = True
    elif message.content.startswith(".minerar") and minerar is True:
        await message.channel.send("Já to minerando meu chapa :)")
    elif message.content.startswith(".parar") and minerar is True:
        await message.channel.send("Parando aqui goat :P")
        minerar = False
    elif message.content.startswith(".parar") and minerar is False:
        await message.channel.send("To fazendo nada mano :(")
    
    if minerar is True:
        save_message(message, source="live")


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit(
            "Defina DISCORD_BOT_TOKEN no arquivo .env antes de executar o bot."
        )

    client.run(TOKEN)
import discord 

TOKEN_AUTH = "1531096870384959648"
GUILD_ID = "789888698673922078"

class GetChannel(discord.Client):
    def __init__(self, guild_id:int, **kwargs):
        super().__init__(**kwargs)
        self.guild_id = guild_id

    async def on_ready(self) -> None:
        print(f"Conectado como {self.user}.")

        try: 
            guild = await self.fetch_guild(self.guild_id)
            print(f"Servidor alvo: {guild}")
        except discord.NotFound:
            print("Servidor nao encontrado.")
            await self.close()
            return
        except discord.Forbidden:
            print("Sem permissao para acessar o servidor.")
            await self.close()
            return
        except discord.HTTPException as exc:
            print(f"Erro ao consultar a API do Discord: {exc}")
            await self.close()
            return
        
        await self.close()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.guilds = True

    client = GetChannel(guild_id=GUILD_ID, intents=intents)
    client.run(TOKEN_AUTH)
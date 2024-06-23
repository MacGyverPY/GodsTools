import discord
from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import box

class CogScanner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Unique identifier

    @commands.command()
    async def scan(self, ctx):
        """
        Scans for unloaded cogs and displays them.
        """
        unloaded_cogs = []
        loaded_cogs = [cog.lower() for cog in self.bot.cogs]
        
        for repo_name, repo in self.bot.cogs.items():
            for cog_name, cog_class in repo.__cogs__.items():
                if cog_name.lower() not in loaded_cogs:
                    unloaded_cogs.append((repo_name, cog_name))

        if not unloaded_cogs:
            await ctx.send("All cogs are already loaded.")
            return

        embed = discord.Embed(
            title="Unloaded Cogs",
            color=discord.Color.blue()
        )
        
        for repo_name, cog_name in unloaded_cogs:
            embed.add_field(
                name=f"{repo_name} - {cog_name}",
                value=":arrow_double_down: React with this emoji to uninstall",
                inline=False
            )

        message = await ctx.send(embed=embed)
        await message.add_reaction("⏬")  # Reaction to uninstall

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "⏬" and reaction.message.id == message.id

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send("No reaction added in time. Aborting.")
        else:
            repo_name, cog_name = reaction.message.embeds[0].fields[0].name.split(" - ")
            await self.uninstall_cog(ctx, repo_name, cog_name)

    async def uninstall_cog(self, ctx, repo_name, cog_name):
        """
        Uninstalls the selected cog.
        """
        try:
            self.bot.unload_extension(f"{repo_name}.{cog_name}")
            await ctx.send(f"Cog '{cog_name}' from '{repo_name}' unloaded successfully.")
        except Exception as e:
            await ctx.send(f"Failed to unload cog '{cog_name}' from '{repo_name}': {e}")

def setup(bot):
    bot.add_cog(CogScanner(bot))

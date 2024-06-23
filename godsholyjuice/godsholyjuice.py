import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.errors import CogLoadError

class GodsHolyJuice(commands.Cog):
    """Cog to manage and monitor other cogs."""

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command()
    async def check_cogs(self, ctx: commands.Context):
        """Check and manage the cogs."""
        await ctx.send("Scanning for cogs, please wait...")

        loaded_cogs = self.bot.cogs
        unloaded_cogs = [cog for cog in self.bot.extensions if cog not in loaded_cogs]

        report = []

        # Check loaded cogs
        for cog_name, cog in loaded_cogs.items():
            report.append(f"Cog: {cog_name} - Status: Enabled")

        # Check unloaded cogs and attempt to load them
        for cog_name in unloaded_cogs:
            try:
                await self.bot.load_extension(cog_name)
                report.append(f"Cog: {cog_name} - Status: Disabled -> Enabled")
            except CogLoadError as e:
                report.append(f"Cog: {cog_name} - Status: Disabled -> Error: {str(e)}")

        # Send the report
        if report:
            await ctx.send("\n".join(report))
        else:
            await ctx.send("No cogs found or all cogs are enabled.")

    @commands.command()
    async def enable_cog(self, ctx: commands.Context, cog_name: str):
        """Attempt to enable a specific cog."""
        if cog_name in self.bot.cogs:
            await ctx.send(f"Cog: {cog_name} is already enabled.")
        else:
            try:
                await self.bot.load_extension(cog_name)
                await ctx.send(f"Cog: {cog_name} - Status: Enabled")
            except CogLoadError as e:
                await ctx.send(f"Cog: {cog_name} - Error: {str(e)}")
                # Optionally, you can provide possible solutions or log the error for further analysis

def setup(bot):
    bot.add_cog(GodsHolyJuice(bot))

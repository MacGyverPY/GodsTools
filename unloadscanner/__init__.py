from .unloadscanner import CogScanner

def setup(bot):
    bot.add_cog(CogScanner(bot))

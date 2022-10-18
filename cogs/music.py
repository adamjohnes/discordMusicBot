import config
import discord
from URL import URL
from discord.ext import commands
"""category documentations"""

class MusicCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	

async def setup(bot):
	await bot.add_cog(MessagingCog(bot))
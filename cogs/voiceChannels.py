import config
import discord
from discord.ext import commands
"""category documentations"""

class VoiceChannelsCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name = "join-voice", help = "Joins the voice channel for audio playing purposes")
	async def join_voice(self, ctx):
		if not ctx.message.author.voice:
			await ctx.send("{} is not connected to a voice channel.".format(str(ctx.message.author)))
			return
		else:
			channel = ctx.author.voice.channel
		await channel.connect()

	@commands.command(name = "leave-voice", help = "Leaves the voice channel it currently resides in")
	async def leave_voice(self, ctx):
		if not ctx.message.author.voice:
			await ctx.send("{} is not connected to a voice channel.".format(str(ctx.message.author)))
			return
		try:
			await ctx.voice_client.disconnect()
		except AttributeError:
			await ctx.send("You have requested the bot to leave a voice channel it does not currently reside.")

async def setup(bot):
	await bot.add_cog(MessagingCog(bot))
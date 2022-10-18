import config
import discord
import random
from discord.ext import commands
"""category documentations"""

class MessagingCog(commands.Cog):

	lastMessage = ""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name = "hello", help = "Responds with a various form of greetings")
	async def hello(self, ctx):
		global lastMessage
		message = ctx.message		
		if message.author == bot.user: #avoids bots talking with bots infinitely
			return 

		username = str(message.author)
		user_message = str(message.content)
		channel = str(message.channel)

		print(f"{username} said: '{user_message}' ({channel})")
		greetings = ["Hey there!", "Hello!", "¡Hola!", "Ciao!", "Bonjour.", "Greetings, fella!", "Salutations.", "What's up?"]

		response = random.choice(greetings)
		print(response, " - ", lastMessage)
		while (lastMessage == response): #avoid duplicate greetings messages! we like to be unique!
			response = random.choice(greetings)

		lastMessage = response
		await ctx.send(response + " " +  f"<@{message.author.id}>")
		"""
	@bot.event
	async def on_reaction_add(reaction, user):
		await reaction.message.add_reaction(reaction)
	"""
async def setup(bot):
	await bot.add_cog(MessagingCog(bot))
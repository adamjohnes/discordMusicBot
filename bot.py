import discord
from discord.ext import commands
from URL import URL
import config
import random
import urllib.request
import json
import urllib
import os
import asyncio
import youtube_dl

check_is_playing_method = False
repeat = False
lastMessage = ""
voice_clients = {}
yt_dl_opts = {"format": "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {"options": "-vn"}

def run_discord_bot():
	
	TOKEN = "MTAyOTI0OTM5NDIyODM1MDk4Ng.Ge7jSK.UGjXS6sMq5B4urN1mQRZAlF2DDKogMuecfQRnE"
	bot = commands.Bot(intents=discord.Intents.all(), command_prefix = '<')
	@bot.event
	async def on_ready():
		print("Ready!")

	@bot.command(name = "hello", help = "Responds with a various form of greetings")
	async def hello(ctx):
		global lastMessage
		message = ctx.message		
		if message.author == bot.user: #avoids bots talking with bots infinitely
			return 

		username = str(message.author)
		user_message = str(message.content)
		channel = str(message.channel)

		greetings = ["Hey there!", "Hello!", "¡Hola!", "Ciao!", "Bonjour.", "Greetings, fella!", "Salutations.", "What's up?"]

		response = random.choice(greetings)
		while (lastMessage == response): #avoid duplicate greetings messages! we like to be unique!
			response = random.choice(greetings)

		lastMessage = response
		await ctx.send(response + " " +  f"<@{message.author.id}>")
		await ctx.send("For more info on what I can do: use <help")

	@bot.event
	async def on_reaction_add(reaction, user):
		await reaction.message.add_reaction(reaction)

	@bot.command(name = "fifa", help = "Congratulates a good fifa pack opening")
	async def fifa(ctx, player):
		player = player.lower()
		
		players = {
			"ronaldo": "https://imgur.com/t/cristiano_ronaldo/TvJ3tW0",
			"messi": "https://imgur.com/gallery/xGRwP4S",
			"benzema": "https://imgur.com/gallery/J1I2VnD",
			"lewandowski": "https://imgur.com/gallery/bzJLS4N",
			"kdb": "https://imgur.com/t/kevin_de_bruyne/kg45TbX",
			"kevin de bruyne": "https://imgur.com/t/kevin_de_bruyne/kg45TbX",
			"de bruyne": "https://imgur.com/t/kevin_de_bruyne/kg45TbX",
			"mbappe": "https://imgur.com/gallery/7eTYriv",
			"salah": "https://imgur.com/gallery/kcUC2nX",
			"courtois": "https://imgur.com/gallery/46WEN",
			"neuer": "https://imgur.com/gallery/P5oLDGs",
			"van dijk": "https://imgur.com/gallery/3DHcnYu",
			"kane": "https://imgur.com/gallery/iHPmGbQ",
			"neymar": "https://imgur.com/gallery/7P88R2n",
			"son": "https://imgur.com/gallery/sEJefYn",
			"casemiro": "https://imgur.com/gallery/EFI5VTs",
			"oblak": "https://imgur.com/gallery/PFDmCiX",
			"mane": "https://imgur.com/gallery/BPoI7",
			"ederson": "https://imgur.com/gallery/ZDK67Ez",
			"kimmich": "https://imgur.com/gallery/ZWtqMO0",
			"alisson": "https://imgur.com/gallery/lnozSiF",
			"kante": "https://imgur.com/gallery/lTfUGeE",
			"dias": "https://giphy.com/gifs/SL-Benfica-slbgifs-slbgif-ruben-dias-Wwfm9nAQWU2iwOfbAZ",
			"haaland": "https://giphy.com/gifs/no-nope-haaland-H9tRvFsIRuQ7PBI5c3",
			"donnarumma": "https://giphy.com/gifs/psg-inside-donnarumma-gianluigi-gianluigidonnarumma-2ETveDPtpSm5KEW3up",
			"silva": "https://giphy.com/gifs/uefa-21-22-ucl-champions-league-uefa-7Vu4wElcT3OgHB7sJs",
			"cancelo": "https://giphy.com/gifs/manchester-city-man-joao-cancelo-9cfDSYFuy3sumBjVr8",
			"marquinhos": "https://giphy.com/gifs/psg-inside-football-paris-3o6fJ5QKuGY4ldr8PK",
			"navas": "https://giphy.com/gifs/psg-inside-keylor-navas-keylornavas-yucxnZa4J9GHfhm7JK",
			"ter stegen": "https://giphy.com/gifs/CUPRA-Official-ter-stegen-marc-terstegen-VdDYiS5tDBSpljc2AF",
			"kroos": "https://giphy.com/gifs/realmadrid-RekA2nAeNKVdl1b40T",
			"modric": "https://giphy.com/gifs/fifa-the-best-luka-modric-KCY0yALOOQ5gP6l1a5",
			"icon": "https://tenor.com/view/welcome-gate-open-cloudy-heaven-gif-14589502"
		}

		try:
			await ctx.send("LETS FUCKING GO!!! " + players[player] + " " + f"<@&{1029957235318718474}>")
		except KeyError:
			await ctx.send("Name not recognized :sob: -> if it's an icon, use" + ' "icon"!')

	
	@bot.command(name = "join-voice", help = "Joins the voice channel (play also does this)")
	async def join_voice(ctx):
		if not ctx.message.author.voice:
			await ctx.send("{} is not connected to a voice channel.".format(str(ctx.message.author)))
			return
		else:
			channel = ctx.author.voice.channel
		voice_client = await channel.connect()
		voice_clients[voice_client.guild.id] = voice_client
	

	@bot.command(name = "leave-voice", help = "Leaves the voice channel it currently resides in")
	async def leave_voice(ctx):
		if not ctx.message.author.voice:
			await ctx.send("{} is not connected to a voice channel.".format(str(ctx.message.author)))
			return
		if ctx.voice_client.is_playing():
			voice_clients[ctx.guild.id].stop()
		try:
			await ctx.voice_client.disconnect()
		except AttributeError:
			await ctx.send("You have requested the bot to leave a voice channel it does not currently reside.")

	async def isPlayingMusic(ctx):
		global repeat
		check_is_playing_method = True
		while True:
			if voice_clients[ctx.guild.id].is_connected():
				if voice_clients[ctx.guild.id].is_playing():
					#do nothing
					await asyncio.sleep(6)
					pass
				elif voice_clients[ctx.guild.id].is_playing() == False and repeat == True:
					try:
						url = config.songs.current.url
						loop = asyncio.get_event_loop()
						urlData = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
						toPlay = urlData['url']
						player = discord.FFmpegPCMAudio(toPlay, **ffmpeg_options, executable = "bin\\ffmpeg.exe")
						try:
							voice_clients[ctx.guild.id].play(player)
						except discord.errors.ClientException:
							pass

					except Exception as e:
						await ctx.send(e)
				else:
					if len(config.songs.queue) == 0:
						return
					try:
						url = config.songs.queue[0].url
						loop = asyncio.get_event_loop()
						urlData = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
						toPlay = urlData['url']
						player = discord.FFmpegPCMAudio(toPlay, **ffmpeg_options, executable = "bin\\ffmpeg.exe")
						if len(config.songs.queue) == 0:
							await ctx.send("The queue is now empty!")

						try:
							voice_clients[ctx.guild.id].play(player)
							config.songs.removeFromQueue()
						except discord.errors.ClientException:
							pass

					except Exception as e:
						await ctx.send(e)
			else:
				config.songs.clearQueue()
				check_is_playing_method = False
				repeat = False
				return


	@bot.command(name = "play", help = "Plays audio from youtube URLs (no spotify yet😭) & adds to list")
	async def play_song(ctx, request):
		global repeat
		if not ctx.message.author.voice:
			await ctx.send("{} is not connected to a voice channel.".format(str(ctx.message.author)))
			return
		else:
			channel = ctx.author.voice.channel

		try:
			voice_client = await channel.connect()
			voice_clients[voice_client.guild.id] = voice_client
		except discord.errors.ClientException:
			pass

		if request != "next":
			vidID, title = str(), str()
			url = request
			if "watch?" in request:
				vidID = request[request.index("="):]
				vidID = vidID[1::]
			elif "tu.be" in request:
				vidID = request[request.index("."):]
				vidID = vidID[4::]
			params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % vidID}
			request = "https://www.youtube.com/oembed"
			query_str = urllib.parse.urlencode(params)
			request = request + "?" + query_str

			try:
				with urllib.request.urlopen(request) as response:
				    response_text = response.read()
				    data = json.loads(response_text.decode())
				    title = data['title']
			except urllib.error.HTTPError:
				await ctx.send("Please use a youtube URL. (more play options possibly coming in the future)")
			song = URL(title, url)
			config.songs.addToQueue(song)

			if voice_clients[ctx.guild.id].is_playing():
				return
			loop = asyncio.get_event_loop()
			urlData = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
			toPlay = urlData['url']
			player = discord.FFmpegPCMAudio(toPlay, **ffmpeg_options, executable = "bin\\ffmpeg.exe")
			if len(config.songs.queue) == 0:
				await ctx.send("The queue is now empty!")

			try:
				voice_clients[ctx.guild.id].play(player)
				config.songs.current = config.songs.queue[0]
				config.songs.removeFromQueue()
				await isPlayingMusic(ctx)
			except discord.errors.ClientException:
				pass
		else:
			if len(config.songs.queue) == 0:
				await ctx.send("The queue is empty!")
				return
			else:
				if (check_is_playing_method == False):
					await isPlayingMusic(ctx)
				url = config.songs.queue[0].url
				loop = asyncio.get_event_loop()
				urlData = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
				toPlay = urlData['url']
				player = discord.FFmpegPCMAudio(toPlay, **ffmpeg_options, executable = "bin\\ffmpeg.exe")
				if len(config.songs.queue) == 0:
					await ctx.send("The queue is now empty!")
				if voice_clients[ctx.guild.id].is_playing() == False:
					try:
						voice_clients[ctx.guild.id].play(player)
						config.songs.current = config.songs.queue[0]
						config.songs.removeFromQueue()
					except discord.errors.ClientException:
						add_song(ctx, url)
						await ctx.send("Added " + song + " to the queue.")

	@bot.command(name = "pause", help = "Pauses the song that is currently playing")
	async def pause_song(ctx):
		try:
			voice_clients[ctx.guild.id].pause()
		except Exception as e:
			await ctx.send(e)

	@bot.command(name = "resume", help = "Resumes the song that is currently paused")
	async def resume_song(ctx):
		try:
			voice_clients[ctx.guild.id].resume()
		except Exception as e:
			await ctx.send(e)

	@bot.command(name = "stop", help = "Stops any music and disconnects")
	async def stop_song(ctx):
		try:
			voice_clients[ctx.guild.id].stop()
			await voice_clients[ctx.guild.id].disconnect()
		except Exception as e:
			await ctx.send(e)

	@bot.command(name = "skip", help = "Skips current song and plays next song in queue")
	async def skip_song(ctx):
		global repeat
		try:
			repeat = False
			voice_clients[ctx.guild.id].stop()
			if len(config.songs.queue) == 0:
				await ctx.send("The queue is now empty!")
				return
			url = config.songs.queue[0].url
			loop = asyncio.get_event_loop()
			urlData = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = False))
			toPlay = urlData['url']
			player = discord.FFmpegPCMAudio(toPlay, **ffmpeg_options, executable = "bin\\ffmpeg.exe")

			try:
				voice_clients[ctx.guild.id].play(player)
				config.songs.current = config.songs.queue[0]
				config.songs.removeFromQueue()
			except discord.errors.ClientException:
				pass

		except Exception as e:
			await ctx.send(e)

	@bot.command(name = "repeat", help = "Repeats the current song until skipped or stopped")
	async def loop_song(ctx):
		global repeat
		if voice_clients[ctx.guild.id].is_connected == False:
			await ctx.send("Connect the bot to the channel first.")
		if voice_clients[ctx.guild.id].is_playing == False:
			await ctx.send("A song must be playing to repeat it, right?")
		else:
			await ctx.send("Setting " + config.songs.current.songTitle + " on repeat. Use 'skip' or 'stop' to move to the next song in the queue.")
			repeat = True
	
	@bot.command(name = "current", help = "Displays the name of the current playing song")
	async def current_song(ctx):
		await ctx.send(config.songs.current.songTitle)

	@bot.command(name = "list", help = "Displays a list of the songs in queue")
	async def list_songs(ctx):
		if len(config.songs.queue) == 0:
			await ctx.send("The queue is empty!")
			return
		else:
			await ctx.send(config.songs)

	@bot.command(name = "add", help = "Adds a song to the queue but does not play it")
	async def add_song(ctx, request):
		url = request
		vidID, title = str(), str()
		if "watch" in request:
			vidID = request[request.index("="):]
			vidID = vidID[1::]
		elif "tu.be" in request:
			vidID = request[request.index("."):]
			vidID = vidID[4::]
		params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % vidID}
		request = "https://www.youtube.com/oembed"
		query_str = urllib.parse.urlencode(params)
		request = request + "?" + query_str

		with urllib.request.urlopen(request) as response:
		    response_text = response.read()
		    data = json.loads(response_text.decode())
		    title = data['title']
		song = URL(title, url)
		config.songs.addToQueue(song)

	@bot.command(name = "remove", help = "Removes the song at the front of the queue")
	async def remove_song(ctx):
		try:
			config.songs.removeFromQueue()
		except IndexError:
			await ctx.send("There are no songs to remove from the queue.")

	bot.run(TOKEN)
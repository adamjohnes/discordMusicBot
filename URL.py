class URL:
	songTitle = "default"
	url = "default"

	def __init__(self):
		pass

	def __init__(self, songTitle, url):
		self.songTitle = songTitle
		self.url = url

	def __str__(self):
		return "Song: " + self.songTitle + "\n" + self.url
import URL

class songQueue:
	queue = []
	current = None

	def __init__(self):
		pass

	def __str__(self):
		message = "List of Songs:\n"
		for song in self.queue:
			message += song.songTitle + "\n"
		return message[0:-1]

	def addToQueue(self, song):
		self.queue.append(song)

	def removeFromQueue(self):
		del self.queue[0]

	def removeFromQueueByTitle(self, title):
		for song in self.queue:
			if song.songTitle == title:
				del self.queue[song]

	def removeFromQueueByPosition(self, position):
		del self.queue[position - 1]

	def removeFromQueueLast(self):
		del self.queue[-1]

	def clearQueue(self):
		self.queue.clear()

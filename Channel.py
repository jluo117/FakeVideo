from bs4 import BeautifulSoup as bs
import bisect
class Channel():
	def __init__(self, soupData):
		channel_tag = soupData.find("div", attrs={"class": "yt-user-info"}).find("a")
		#print(soupData.find("span", attrs={"class": "yt-subscriber-count"}))
		self.Channel_Url = f"https://www.youtube.com{channel_tag['href']}"
		self.Channel_Name = channel_tag.text
		self.UpVote = 0
		self.TotalVote = 0
		subData = soupData.find("span", attrs={"class": "yt-subscriber-count"})
		if subData != None:
			self.Sub = soupData.find("span", attrs={"class": "yt-subscriber-count"}).text.strip()
		else:
			self.Sub = "Error"
		self.Freq = {}
	
	def up_vote(self):
		self.UpVote += 1
		self.TotalVote += 1
		
	
	def down_vote(self):
		self.TotalVote += 1
		
	def get_sub(self):
		return self.Sub
	def update_common(self,wordList):
		for word in wordList:
			if word in self.Freq:
				self.Freq[word] += wordList[word]
			else:
				self.Freq[word] = wordList[word]
	def get_rating(self):

		if self.TotalVote == 0:
		
			return 5
		print("UpVote")
		print(self.UpVote)
		print(self.TotalVote)
		return (self.UpVote / self.TotalVote) * 5
	def get_k_freqWords(self,K):
		mostCommon = []
		for word in self.Freq:
			wordFreq = -(self.Freq[word])
			bisect.insort(mostCommon,(wordFreq,word))
			if len(mostCommon) > K:
				mostCommon.pop()
		result = []
		for dataSet in mostCommon:
			dataNode = (dataSet[1],-dataSet[0])
			result.append(dataNode)
		return result

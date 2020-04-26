from bs4 import BeautifulSoup as bs
import bisect
class Channel():
	def __init__(self,soupData):
		channel_tag = soupData.find("div", attrs={"class": "yt-user-info"}).find("a")
		self.Channel_Url = f"https://www.youtube.com{channel_tag['href']}"
		self.Channel_Name = channel_tag.text
		self.Rating = 0
		self.Sub = soupData.find("span", attrs={"class": "yt-subscriber-count"}).text.strip()
		self.Freq = {}
	
	def up_vote(self):
		self.Rating += 1
		return self.Rating
	
	def down_vote(self):
		self.Rating -= 1
		return self.Rating
	def get_sub(self):
		return self.Sub
	def update_common(self,wordList):
		for word in wordList:
			if word in self.Freq:
				self.Freq[word] += wordList[word]
			else:
				self.Freq[word] = wordList[word]
	def get_rating(self):
		return self.Rating
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

from bs4 import BeautifulSoup as bs
import bisect
import math  
class Channel():
	def __init__(self):
		self.Channel_Url = None
		self.Channel_Name = None
		self.UpVote = 0
		self.TotalVote = 0
		self.Sub = ""
		self.Freq = {}
	 
	def soup_insert(self, soupData):
		channel_tag = soupData.find("div", attrs={"class": "yt-user-info"}).find("a")
		#print(soupData.find("span", attrs={"class": "yt-subscriber-count"}))
		self.Channel_Url = f"https://www.youtube.com{channel_tag['href']}"
		self.Channel_Name = channel_tag.text
	
		subData = soupData.find("span", attrs={"class": "yt-subscriber-count"})
		if subData != None:
			self.Sub = soupData.find("span", attrs={"class": "yt-subscriber-count"}).text.strip()
		else:
			self.Sub = "Not Found"
		data = {
		u'Channel_Url' : self.Channel_Url,
		u'Channel_Name': self.Channel_Name,
		u'Sub': self.Sub,
		u'Freq': self.Freq,
		u'UpVote': self.UpVote,
		u'TotalVote': self.TotalVote
		}
		return data

	def get_from_database(self,dataBase):
		self.Channel_Url = dataBase['Channel_Url']
		self.Channel_Name = dataBase['Channel_Name']
		self.UpVote = dataBase['UpVote']
		self.TotalVote = dataBase['TotalVote']
		self.Sub = dataBase['Sub']
		self.Freq = dataBase['Freq']
	
	def up_vote(self):
		self.UpVote += 1
		self.TotalVote += 1
		return self.UpVote , self.TotalVote
	
	def down_vote(self):
		self.TotalVote += 1
		return self.TotalVote
	def get_sub(self):
		return self.Sub
	def update_common(self,wordList):
		for word in wordList:
			if word in self.Freq:
				self.Freq[word] += wordList[word]
			else:
				self.Freq[word] = wordList[word]
		return self.Freq
	def get_rating(self):

		if self.TotalVote == 0:
		
			return 5
		print("UpVote")
		print(self.UpVote)
		print(self.TotalVote)
		return math.floor((self.UpVote / self.TotalVote) * 5)
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

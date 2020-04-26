from youtube_transcript_api import YouTubeTranscriptApi
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import reteriveChannel as rc
import requests
from Channel import Channel
from bs4 import BeautifulSoup as bs

import editdistance 
def correctData(Organzation,Proper):
	massiveBucket = {}
	for word in Organzation:
		if word not in massiveBucket:
			massiveBucket[word] = Organzation[word]
		
	for word in Proper:
		if word not in massiveBucket:
			massiveBucket[word] = Proper[word]
		
	for word in massiveBucket:
		if massiveBucket[word] <= 1:
			for toCompare in massiveBucket:
				if editdistance.eval(word,toCompare) == 1:
					massiveBucket[toCompare] += 1
					massiveBucket[word] = 0
					break
	return massiveBucket
def NLPProcessor(text):
	OrganizationBucket = {}
	ProperBucket = {}
	client = language.LanguageServiceClient()
	document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)
	encoding_type = enums.EncodingType.UTF8

	response = client.analyze_entities(document, encoding_type=encoding_type)
	for entity in response.entities:
		for mention in entity.mentions:
			if enums.Entity.Type(entity.type).name == "ORGANIZATION":
				if mention.text.content in OrganizationBucket:
					OrganizationBucket[mention.text.content] += 1
				else:
					OrganizationBucket[mention.text.content] = 1
			if enums.EntityMention.Type(mention.type).name == "PROPER":
				if mention.text.content in ProperBucket:
					ProperBucket[mention.text.content] += 1
				else:
					ProperBucket[mention.text.content] = 1
	return OrganizationBucket , ProperBucket
class VideoDetect():

	def __init__(self):
		self.ChannelUrls = {}
		self.DataSet = {}
		self.lastChannel = None
	def detect_video(self , url):
		res = None
		try:
			res = YouTubeTranscriptApi.get_transcript(url)
		except:
			return "No Subtitles Found"
		videoText = ""
		time = 0
		for output in res:
			videoText += (output['text']) + " "
			time += output['duration']
		print(time/60)
		OrgValue , ProperValue= NLPProcessor(videoText)
		self.OrgValue = OrgValue
		maxValue = (0,"")
		massiveBucket = correctData(OrgValue,ProperValue)
		for entitiies in OrgValue:
			if massiveBucket[entitiies] == 0:
				continue
			maxValue = max(maxValue,(massiveBucket[entitiies],entitiies))
		
		
		print(maxValue[0])
		channelName , ChannelUrl,soup = rc.get_video_info(url)
		if channelName == None:
			self.lastChannel = "ERROR"
			if maxValue[0] >= time/90:
				
				return "This video is an advertisement for " + maxValue[1]
			else:
				return "This video is not an advertisement"
		self.lastChannel = channelName
		if channelName not in self.DataSet:
			newChannel = Channel(soup)
			self.DataSet[channelName] = newChannel
			self.ChannelUrls[ChannelUrl] = channelName
		self.DataSet[channelName].update_common(massiveBucket)
		rating = self.DataSet[channelName].get_rating()
		if maxValue[0] >= time/90 + rating * 5:
			self.DataSet[channelName].up_vote()
			return "This video is an advertisement for " + maxValue[1]
		self.DataSet[channelName].down_vote()
		return "This video is not an advertisement"
	def get_last_info(self):
		if self.lastChannel == "ERROR" or self.lastChannel == None:
			return "ERROR with either last channel or no data is found"
		returnVal = "Channel Name: " + self.lastChannel + '\n'
		returnVal += "Channel Sub: " + self.DataSet[self.lastChannel].get_sub() + ' \n'
		returnVal += "Channel Rating: " + str(self.DataSet[self.lastChannel].get_rating()) + ' \n'
		return returnVal
	def get_channel_info(self, channel):
		if channel not in self.DataSet:
			return "Error"
		returnVal = "Channel Name: " + channel + '\n'
		returnVal += "Channel Sub: " + self.DataSet[channel].get_sub() + ' \n'
		returnVal += "Channel Rating: " + str(self.DataSet[channel].get_rating()) + ' \n'
		return returnVal
	def get_popularVal(self,channel = None,K = 3):
		if channel == None:
			channel = self.lastChannel
		if channel not in self.DataSet:
			return "Invalid Channel"
		KFreq = self.DataSet[channel].get_k_freqWords(K)
		returnVal = {}
		for word in KFreq:
			returnVal[word[0]] = str(word[1])
		return returnVal
	def get_channel_name(self,url):
		if url not in self.ChannelUrls:
			return None
		else:
			return self.ChannelUrls[url]
		




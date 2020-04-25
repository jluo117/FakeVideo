from youtube_transcript_api import YouTubeTranscriptApi
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import reteriveChannel as rc
import requests
from bs4 import BeautifulSoup as bs


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
		self.DataSet = {}
	def detect_video(self , url):
		res = YouTubeTranscriptApi.get_transcript(url)
		videoText = ""
		time = 0
		for output in res:
			videoText += (output['text']) + " "
			time += output['duration']
		print(time/60)
		OrgValue , ProperValue= NLPProcessor(videoText)
		maxValue = (0,"")
		for entitiies in OrgValue:
			maxValue = max(maxValue,(OrgValue[entitiies],entitiies))
		for entitiies in ProperValue:
			maxValue = max(maxValue,(ProperValue[entitiies],entitiies))
		print(OrgValue)
		print(ProperValue)
		print(maxValue[0])
		channelName = rc.get_video_info(url)
		if channelName == None:
			if maxValue[0] >= time/90:
				
				return "This video is an advertisement for " + maxValue[1]
			else:
				return "This video is not an advertisement"
		score = 0
		if channelName in self.DataSet:
			score = self.DataSet[channelName]
		else:
			self.DataSet[channelName] = 0
		if maxValue[0] >= time/90 + score * 5:
			self.DataSet[channelName] += 1
			return "This video is an advertisement for " + maxValue[1]
		self.DataSet[channelName] -= 1
		return "This video is not an advertisement"



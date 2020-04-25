from youtube_transcript_api import YouTubeTranscriptApi
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
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
		self.DataSet = None
	def detect_video(self , url):
		res = YouTubeTranscriptApi.get_transcript(url)
		videoText = ""
		for output in res:
			videoText += (output['text'])
		OrgValue , ProperValue= NLPProcessor(videoText)
		maxValue = (0,"")
		for entitiies in OrgValue:
			maxValue = max(maxValue,(OrgValue[entitiies],entitiies))
		for entitiies in ProperValue:
			maxValue = max(maxValue,(ProperValue[entitiies],entitiies))
		
		if maxValue[0] > 2:
			return "This is an AD for " + maxValue[1]
		return "This is Not an AD"



from youtube_transcript_api import YouTubeTranscriptApi
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
def getToken(text):
	WordBucket = {}
	client = language.LanguageServiceClient()
	document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)
	encoding_type = enums.EncodingType.UTF8
	response = client.analyze_entities(document, encoding_type=encoding_type)
	for entity in response.entities:
		for mention in entity.mentions:
			if enums.Entity.Type(entity.type).name != "TYPE_UNKNOWN" or enums.Entity.Type(entity.type).name != "NUMBER":
				if mention.text.content in WordBucket:
					WordBucket[mention.text.content] += 1
				else:
					WordBucket[mention.text.content] = 1
	return WordBucket

def compareVideo(VideoOne,VideoTwo):
	VideoOneTxt = ""
	VideoTwoTxt = ""
	try:
		resOne = YouTubeTranscriptApi.get_transcript(VideoOne)
		resTwo = YouTubeTranscriptApi.get_transcript(VideoTwo)
	except:
		return "Having issue parsing Subtiles"
	for output in resOne:
		VideoOneTxt += output['text'] + " "
	for output in resTwo:
		VideoTwoTxt += output['text'] + " "
	VideoOneBucket = getToken(VideoOneTxt)
	VideoTwoBucket = getToken(VideoTwoTxt)
	score = 0
	Common = {}
	for word in VideoOneBucket:
		if word in VideoTwoBucket:
			score += min(VideoOneBucket[word],VideoTwoBucket[word])
			Common[word] = min(VideoOneBucket[word],VideoTwoBucket[word])
	return str(score) , Common

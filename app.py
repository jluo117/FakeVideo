from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi
app = Flask(__name__)


def extract_id_from_url(link):
    return str(link.split('=', 1)[1])[:11]


@app.route('/')
def home():
    id = extract_id_from_url('https://www.youtube.com/watch?v=nmqDrG09CQQ')
    print(id, YouTubeTranscriptApi.get_transcript(id))
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

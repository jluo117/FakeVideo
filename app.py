from flask import Flask, render_template, redirect, request
from youtube_transcript_api import YouTubeTranscriptApi
app = Flask(__name__)


def extract_id_from_url(link):
    return str(link.split('=', 1)[1])[:11]


@app.route('/about')
def about():
    return render_template('about.html', page_name='about')


@app.route('/')
def home():
    id = extract_id_from_url('https://www.youtube.com/watch?v=nmqDrG09CQQ')
    print(id, YouTubeTranscriptApi.get_transcript(id))
    return render_template('index.html', page_name='home')


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        id = extract_id_from_url(str(request.form.get('videoURL')))
        lyrics = YouTubeTranscriptApi.get_transcript(id)
        return render_template('detect.html', lyrics=lyrics)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

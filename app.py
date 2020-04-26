from flask import Flask, render_template, redirect, request
from VideoDetect import VideoDetect
from youtube_transcript_api import YouTubeTranscriptApi
app = Flask(__name__)


def extract_id_from_url(link):
    return str(link.split('=', 1)[1])[:11]


@app.route('/about')
def about():
    return render_template('about.html', page_name='about')


@app.route('/')
def home():
    return render_template('index.html', page_name='home')


@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        url = str(request.form.get('videoURL'))
        id = extract_id_from_url(url)
        detect = VideoDetect()
        res = detect.detect_video(id)
        word_freq = detect.get_popularVal()
        return render_template('detect.html', response=res, nlp=detect.ChannelUrls, video_url=url, freq=word_freq, video_id=id)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

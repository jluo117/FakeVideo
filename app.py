from flask import Flask, render_template, redirect, request
from VideoDetect import VideoDetect
from youtube_transcript_api import YouTubeTranscriptApi
from reteriveChannel import *
from Compare import *
app = Flask(__name__)
Video_Detector = VideoDetect()

def extract_id_from_url(link):
    return str(link.split('=', 1)[1])[:11]


@app.route('/compare', methods=['GET','POST'])
def compare():
    if request.method == 'POST':
        vid1 = extract_id_from_url(str(request.form.get('video1')))
        vid2 = extract_id_from_url(str(request.form.get('video2')))
        print(vid1, vid2)
        rating, similarities = compareVideo(vid1, vid2)

        return render_template('compare.html', page_name='compare videos', rating=rating, similarities=similarities)
    return render_template('compare.html', page_name='compare videos')


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
        res = Video_Detector.detect_video(id)
        word_freq = Video_Detector.get_popularVal()
        return render_template('detect.html', response=res, video_url=url, freq=word_freq, channel_info=Video_Detector.get_last_info(), page_name='video details')
    return redirect('/')


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, send_file
import os
import yt_dlp

app = Flask(__name__)
@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    if "instagram.com" not in url:
        return "Only Instagram links are supported!", 400

    output_path = "downloads/"
    os.makedirs(output_path, exist_ok=True)
    options = {
        'outtmpl': f'{output_path}%(title)s.%(ext)s',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    format = request.json.get('format', 'mp4')  # Default to mp4 if no format is provided
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        yt = YouTube(url)
        if format == 'mp3':
            stream = yt.streams.filter(only_audio=True).first()
            file_path = stream.download(filename='audio.mp3')
        else:
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            file_path = stream.download()
        return jsonify({'message': 'Downloaded successfully', 'file_path': file_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

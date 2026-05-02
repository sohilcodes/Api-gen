from flask import Flask, request, jsonify
import yt_dlp
import re

app = Flask(__name__)

def clean_url(url):
    match = re.search(r"(https://www\.instagram\.com/reel/[^/?]+)", url)
    return match.group(1) if match else url

@app.route('/')
def home():
    return "API Running 🚀"

@app.route('/api', methods=['GET'])
def download():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "No URL"}), 400

    try:
        url = clean_url(url)

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'quiet': True,
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return jsonify({
            "status": "success",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "video_url": info.get("url")
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run()

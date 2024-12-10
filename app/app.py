from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        # Kullanıcıdan gelen URL
        video_url = request.form['url']
        
        # İndirilen dosyanın çıkış yolu
        output_path = "downloads"
        if not os.path.exists(output_path):
            os.makedirs(output_path)  # Klasör yoksa oluştur

        # YT-DLP ayarları
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Dosya adı ve yolu
            'format': 'best',  # En iyi kalite
        }

        # Video indirme işlemi
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)  # Video bilgilerini al ve indir
            file_name = ydl.prepare_filename(info)  # İndirilen dosya adı

        # Dosyayı kullanıcıya gönder
        return send_file(file_name, as_attachment=True)

    except Exception as e:
        return f"Bir hata oluştu: {e}"

if __name__ == '__main__':
    app.run(debug=True)

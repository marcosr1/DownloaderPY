import yt_dlp
import ffmpeg_downloader as ffdl

caminho_ffmpeg = ffdl.ffmpeg_path

def baixar_mp3(url, qualidade, pastaD="./downloads/mp3", callback_progresso=None, checar_cancelamento=None):
    def hook_interno(d): 
        if checar_cancelamento:
            checar_cancelamento(d)

        if d['status'] == 'downloading' and callback_progresso:
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            baixado = d.get('downloaded_bytes', 0)
            if total > 0:
                porcentagem = baixado / total
                callback_progresso(porcentagem)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{pastaD}/%(title)s.%(ext)s',
        'ffmpeg_location': caminho_ffmpeg,
        'postprocessors': [{ 'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': qualidade,
        }],
        'max_downloads': 1,
        'noplaylist': True,
        'progress_hooks': [hook_interno],
    }

    try:
        print("Analisando o link e baixando o áudio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download e conversão para MP3 concluídos!")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o áudio: {e}")

def baixar_mp4(url, qualidade, pastaD="./downloads/mp4", callback_progresso=None, checar_cancelamento=None):
    def hook_interno(d): 
        if checar_cancelamento:
            checar_cancelamento(d)

        if d['status'] == 'downloading' and callback_progresso:
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            baixado = d.get('downloaded_bytes', 0)
            if total > 0:
                porcentagem = baixado / total
                callback_progresso(porcentagem)

    ydl_opts = {
        'format': f'bestvideo[height<={qualidade}][ext=mp4]+bestaudio[ext=m4a]/best[height<={qualidade}][ext=mp4]/best',
        'outtmpl': f'{pastaD}/%(title)s.%(ext)s',
        'ffmpeg_location': caminho_ffmpeg,
        'merge_output_format': 'mp4',
        'max_downloads': 1,
        'noplaylist': True,
        'progress_hooks': [hook_interno],
    }

    try:
        print("Analisando o link e baixando o vídeo...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download do vídeo concluído!")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o vídeo: {e}") 

if __name__ == "__main__":
    while True:
        link_do_video = input("Cole o link do vídeo aqui para extrair o MP3: ")
        mp3ou_mp4 = input("Digite '1' para baixar apenas o áudio ou '2' para baixar o vídeo: ").strip().lower()

        if mp3ou_mp4 == "1":
            q = input("Digite a qualidade desejada para o áudio (ex: 128, 192, 256, 320): ").strip()
            baixar_mp3(link_do_video, qualidade=q)
        elif mp3ou_mp4 == "2":
            q = input("Digite a qualidade desejada para o vídeo (ex: 144p, 240p, 360p, 480p, 720p, 1080p): ").strip()
            baixar_mp4(link_do_video, qualidade=q)
        else:
            print("Opção inválida. Por favor, digite '1' ou '2'.")
    
import yt_dlp
import ffmpeg_downloader as ffdl

caminho_ffmpeg = ffdl.ffmpeg_path

def baixar_mp3(url, pastaD="./downloads/mp3", qualidade="'320"):
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
    }

    try:
        print("Analisando o link e baixando o áudio...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download e conversão para MP3 concluídos!")
    except Exception as e:
        print(f"Ocorreu um erro ao baixar o áudio: {e}")

def baixar_mp4(url, pastaD="./downloads/mp4"):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=m4a]',
        'outtmpl': f'{pastaD}/%(title)s.%(ext)s',
        'ffmpeg_location': caminho_ffmpeg,
        'merge_output_format': 'mp4',
        'max_downloads': 1,
        'noplaylist': True,
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
            baixar_mp3(link_do_video)
        elif mp3ou_mp4 == "2":
            baixar_mp4(link_do_video)
        else:
            print("Opção inválida. Por favor, digite '1' ou '2'.")
    
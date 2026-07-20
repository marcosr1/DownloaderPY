import threading
import customtkinter as ctk
import yt_dlp
import io
import urllib.request
import requests
from PIL import Image
import ffmpeg_downloader as ffdl

from main import baixar_mp3, baixar_mp4
caminho_ffmpeg = ffdl.ffmpeg_path

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class baixador(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Baixador de Vídeos e Áudios")
        self.geometry("720x580")

        self.configure(fg_color="#121212")

        self.label = ctk.CTkLabel(self, text="Cole o link do vídeo:", font=ctk.CTkFont("Segoe UI", 24, "bold"))
        self.label.pack(pady=10)

        self.url_input = ctk.CTkEntry(self, width=400, placeholder_text="Cole o link aqui", fg_color="#1A1A1A", bg_color="#121212", border_width=1, corner_radius=8)
        self.url_input.pack(pady=(10, 0))
        self.url_input.bind("<KeyRelease>", self.ao_alterar_link)

        self.delay_busca = None

        self.formato_var = ctk.StringVar(value="MP3")
        self.selecao_formato = ctk.CTkSegmentedButton(self, values=["MP3", "MP4"], variable=self.formato_var, width=200, command=self.alterarOpcoes, border_width=1, selected_color="#ff0000", selected_hover_color="#640010", fg_color="#1A1A1A", corner_radius=8)
        self.selecao_formato.pack(pady=15)

        self.combobox_qualidade = ctk.CTkComboBox(self, values=["320 kbps", "256 kbps", "192 kbps", "128 kbps"], border_width=1, fg_color="#1A1A1A", corner_radius=8)
        self.combobox_qualidade.pack(pady=10)

        self.btn_baixar = ctk.CTkButton(self, text="BAIXAR", font=("Segoe UI", 14, "bold"), command=self.baixar, fg_color="#ff0000", hover_color="#640010", text_color="#FFFFFF", width=150, height=40, corner_radius=8)
        self.btn_baixar.pack(pady=10)

        self.cancelar_download = False 
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", font=("Segoe UI", 12, "bold"), command=self.clicar_cancelar, width=100, height=25, corner_radius=8, fg_color="#ff0000", hover_color="#640010", state="disabled") 
        self.btn_cancelar.pack(pady=10)

        self.label_capa = ctk.CTkLabel(self, text="")
        self.label_capa.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Aguardando link...", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)

        self.progresso = ctk.CTkProgressBar(self, width=400, height=10, corner_radius=4, fg_color="#1A1A1A", progress_color="#ff0000")
        self.progresso.set(0)

        self.frame_rodape = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_rodape.pack(side="bottom", pady=(20, 0))
        estilo_icone = {"font": ("Segoe UI", 16), "text_color": "#888888", "cursor": "hand2"}

        self.lbl_yt = ctk.CTkLabel(self.frame_rodape, text="Download direto das principais plataformas", **estilo_icone)
        self.lbl_yt.pack(side="left", padx=15)
        

    def alterarOpcoes(self, formato):
        if formato == "MP3":
            self.combobox_qualidade.configure(values=["320 kbps", "256 kbps", "192 kbps", "128 kbps"])
            self.combobox_qualidade.set("320 kbps")
        elif formato == "MP4":
            self.combobox_qualidade.configure(values=["1080p", "720p", "480p", "360p", "240p", "144p"])
            self.combobox_qualidade.set("1080p")

    def baixar(self):
        thread = threading.Thread(target=self.download, daemon=True)
        thread.start()

    def clicar_cancelar(self):
        self.cancelar_download = True
        self.status_label.configure(text="Cancelando download...", text_color="#EF4444")
        self.btn_cancelar.configure(state="disabled")

    def exibir_capa(self, url_imagem):
        try:
            resposta = requests.get(url_imagem, timeout=5)
            dados_imagem = io.BytesIO(resposta.content)
            img_pil = Image.open(dados_imagem)
            img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(280, 157))
            self.label_capa.configure(image=img_ctk, text="")
            
        except Exception as e:
            print(f"Não foi possível carregar a capa: {e}")

    def ao_alterar_link(self, *args):
        if hasattr(self, 'delay_busca') and self.delay_busca:
            self.after_cancel(self.delay_busca)

        def buscar():
            url = self.url_input.get().strip()
            if not url:
                self.label_capa.configure(image=None, text="")
                return
            
            if "youtu" in url:
                def _thread():
                    try:
                        video_id = None
                        if "v=" in url:
                            video_id = url.split("v=")[1].split("&")[0]
                        elif "youtu.be/" in url:
                            video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]
                        if video_id:
                            url_da_capa = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
                            self.exibir_capa(url_da_capa)
                        else:
                            self.after(0, lambda: self.label_capa.configure(text="Capa não encontrada"))
                            
                    except Exception as erro:
                        print(f"Erro ao gerar a capa: {erro}")
                        self.after(0, lambda: self.label_capa.configure(text="Erro ao carregar capa"))

                threading.Thread(target=_thread, daemon=True).start()

        self.delay_busca = self.after(500, buscar)

    def download(self):
        url = self.url_input.get()
        formato = self.formato_var.get()
        qualidade = self.combobox_qualidade.get().split()[0]

        if not url:
            self.status_label.configure(text="Por favor, insira um link válido.")
            return
        
        self.cancelar_download = False
        self.btn_baixar.configure(state="disabled")
        self.btn_cancelar.configure(state="normal")
        self.status_label.configure(text="Iniciando download...") 
        self.progresso.pack(pady=5)
        self.progresso.set(0)

        def cancelamento(d):
            if self.cancelar_download:
                raise yt_dlp.utils.DownloadError("Download cancelado pelo usuário.")
            if d['status'] == 'downloading':
                pass

        try:
            self.status_label.configure(text=f"Baixando... {formato}, {qualidade}")
            if formato == "MP3":
                print (f"Baixando áudio de {url} com qualidade {qualidade}...")
                baixar_mp3(url, qualidade=qualidade, callback_progresso=self.progresso.set, checar_cancelamento=cancelamento)
            elif formato == "MP4":
                print (f"Baixando vídeo de {url} com qualidade {qualidade}...")
                baixar_mp4(url, qualidade=qualidade, callback_progresso=self.progresso.set, checar_cancelamento=cancelamento)

            if self.cancelar_download:
                self.status_label.configure(text="Download cancelado pelo usuário.", text_color="#EF4444")
            else:
                self.status_label.configure(text="Download concluído com sucesso!", text_color="#10B981")
                self.progresso.set(1) 
                self.url_input.delete(0, ctk.END)
            

        except yt_dlp.utils.DownloadError as e:
            if "cancelado" in str(e).lower():
                self.status_label.configure(text="Download cancelado pelo usuário.", text_color="#EF4444")
            else:
                self.status_label.configure(text=f"Ocorreu um erro: {e}", text_color="#EF4444")
                
        finally: 
            self.progresso.stop()
            self.progresso.pack_forget()
            self.btn_baixar.configure(state="normal")
            self.btn_cancelar.configure(state="disabled")

if __name__ == "__main__":
    app = baixador()
    app.mainloop()
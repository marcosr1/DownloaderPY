import threading
import customtkinter as ctk
import yt_dlp
from io import BytesIO
import urllib.request
from PIL import Image
import requests

from main import baixar_mp3, baixar_mp4

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class baixador(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Baixador de Vídeos e Áudios")
        self.geometry("720x380")

        self.configure(fg_color="#121212")

        self.label = ctk.CTkLabel(self, text="Cole o link do vídeo:", font=ctk.CTkFont("Segoe UI", 24, "bold"))
        self.label.pack(pady=10)

        self.url_input = ctk.CTkEntry(self, width=400, placeholder_text="Cole o link do YouTube aqui...", border_width=1, placeholder_text_color="#555555", fg_color="#1A1A1A", corner_radius=8)
        self.url_input.pack(pady=10)

        self.formato_var = ctk.StringVar(value="MP3")
        self.selecao_formato = ctk.CTkSegmentedButton(self, values=["MP3", "MP4"], variable=self.formato_var, width=200, command=self.alterarOpcoes, border_width=1, selected_color="#ff0000", fg_color="#1A1A1A", corner_radius=8)
        self.selecao_formato.pack(pady=15)

        self.combobox_qualidade = ctk.CTkComboBox(self, values=["320 kbps", "256 kbps", "192 kbps", "128 kbps"], border_width=1, fg_color="#1A1A1A", corner_radius=8)
        self.combobox_qualidade.pack(pady=10)

        self.btn_baixar = ctk.CTkButton(self, text="BAIXAR", font=("Segoe UI", 14, "bold"), command=self.baixar, fg_color="#ff0000", hover_color="#cc0000", text_color="#FFFFFF", width=150, height=40, corner_radius=8)
        self.btn_baixar.pack(pady=10)

        self.cancelar_download = False 
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", font=("Segoe UI", 12, "bold"),width=100, height=25, corner_radius=8, fg_color="#ff0000", hover_color="#B91C1C", state="disabled") 
        self.btn_cancelar.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Aguardando link...", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)

        self.progresso = ctk.CTkProgressBar(self, width=400, height=10, corner_radius=4, fg_color="#1A1A1A", progress_color="#ff0000")
        self.progresso.set(0)

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
                baixar_mp3(url, qualidade=qualidade, callback_progresso=self.progresso.set,)
            elif formato == "MP4":
                print (f"Baixando vídeo de {url} com qualidade {qualidade}...")
                baixar_mp4(url, qualidade=qualidade, callback_progresso=self.progresso.set,)

            self.progresso.set(1)
            self.status_label.configure(text=f"Download de {formato} concluído!")
            self.url_input.delete(0, ctk.END)

        except Exception as e: 
            if "Numero maximo de Arquivos" in str(e):
                self.status_label.configure(text="Download concluído com sucesso!", text_color="green")
                self.url_input.delete(0, 'end')
            else:
                self.status_label.configure(text=f"Erro: {str(e)[:50]}...", text_color="red")
                
        finally: 
            self.progresso.stop()
            self.progresso.pack_forget()
            self.btn_baixar.configure(state="normal")
            self.btn_cancelar.configure(state="disabled")

if __name__ == "__main__":
    app = baixador()
    app.mainloop()
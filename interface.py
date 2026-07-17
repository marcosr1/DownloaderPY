import threading
import customtkinter as ctk
import yt_dlp
from io import BytesIO
import urllib.request
from PIL import Image
import requests

from main import baixar_mp3, baixar_mp4, info_video

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class baixador(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Baixador de Vídeos e Áudios")
        self.geometry("920x640")

        self.label = ctk.CTkLabel(self, text="Cole o link do vídeo:")
        self.label.pack(pady=10)

        self.url_input = ctk.CTkEntry(self, width=400)
        self.url_input.pack(pady=10)

        self.formato_var = ctk.StringVar(value="MP3")
        self.selecao_formato = ctk.CTkSegmentedButton(self, values=["MP3", "MP4"], variable=self.formato_var, width=200)
        self.selecao_formato.pack(pady=15)

        self.btn_baixar = ctk.CTkButton(self, text="Baixar", command=self.baixar)
        self.btn_baixar.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Aguardando link...", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)

    def baixar(self):
        thread = threading.Thread(target=self.download, daemon=True)
        thread.start()

    def download(self):
        url = self.url_input.get()
        formato = self.formato_var.get()

        if not url:
            self.status_label.configure(text="Por favor, insira um link válido.")
            return
        
        self.btn_baixar.configure(state="disabled")
        self.status_label.configure(text="Iniciando download...")
        self.progresso.pack(pady=5)
        self.progresso.start()

        try:
            self.status_label.configure(text=f"Baixando... {formato}")
            if formato == "MP3":
                baixar_mp3(url)
            elif formato == "MP4":
                baixar_mp4(url)
            
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

if __name__ == "__main__":
    app = baixador()
    app.mainloop()
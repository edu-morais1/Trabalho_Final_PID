import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

class PainelImagem(tk.Frame):
    def __init__(self, parent, titulo="Imagem", largura=400, altura=400):
        super().__init__(parent)
        self.largura = largura
        self.altura = altura
        self.label_titulo = tk.Label(self, text=titulo, font=('Arial', 12, 'bold'))
        self.label_titulo.pack(pady=5)
        self.canvas = tk.Canvas(self, width=largura, height=altura, bg='gray', relief=tk.SUNKEN, borderwidth=2)
        self.canvas.pack()
        self.label_info = tk.Label(self, text="Nenhuma imagem", font=('Arial', 9), fg='gray')
        self.label_info.pack(pady=2)
        self.photo_image = None

    def exibir_imagem(self, imagem_array, info=""):
        if imagem_array is None: return
        if imagem_array.max() > 255 or imagem_array.min() < 0:
            imagem_array = np.clip(imagem_array, 0, 255)
        imagem_array = imagem_array.astype(np.uint8)
        h, w = imagem_array.shape
        prop = min(self.largura/w, self.altura/h)
        img_pil = Image.fromarray(imagem_array)
        if prop < 1:
            img_pil = img_pil.resize((int(w*prop), int(h*prop)), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(img_pil)
        self.canvas.delete("all")
        self.canvas.create_image(self.largura//2, self.altura//2, anchor=tk.CENTER, image=self.photo_image)
        self.label_info.config(text=info if info else f"{h}x{w}")

    def limpar(self):
        self.canvas.delete("all")
        self.photo_image = None
        self.label_info.config(text="Nenhuma imagem")

class JanelaProgresso(tk.Toplevel):
    def __init__(self, parent, titulo="Processando..."):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("300x100")
        self.transient(parent)
        self.grab_set()
        tk.Label(self, text="Processando...").pack(pady=10)
        self.pb = ttk.Progressbar(self, mode='indeterminate', length=250)
        self.pb.pack(pady=10)
        self.pb.start()
    def fechar(self): self.destroy()

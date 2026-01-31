"""
Componentes reutilizáveis da interface

Autor: [Seu Nome]
Data: Janeiro/2026
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np


class PainelImagem(tk.Frame):
    """
    Painel para exibir uma imagem com título
    """
    
    def __init__(self, parent, titulo="Imagem", largura=400, altura=400):
        super().__init__(parent)
        
        self.largura = largura
        self.altura = altura
        
        # Título
        self.label_titulo = tk.Label(
            self, 
            text=titulo, 
            font=('Arial', 12, 'bold')
        )
        self.label_titulo.pack(pady=5)
        
        # Canvas para imagem
        self.canvas = tk.Canvas(
            self, 
            width=largura, 
            height=altura, 
            bg='gray',
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.canvas.pack()
        
        # Label de informações
        self.label_info = tk.Label(
            self, 
            text="Nenhuma imagem",
            font=('Arial', 9),
            fg='gray'
        )
        self.label_info.pack(pady=2)
        
        self.imagem_atual = None
        self.photo_image = None
    
    def exibir_imagem(self, imagem_array, info=""):
        """
        Exibe uma imagem no painel
        
        Args:
            imagem_array (numpy.ndarray): Imagem a exibir
            info (str): Informações adicionais
        """
        if imagem_array is None:
            return
        
        self.imagem_atual = imagem_array
        
        # Normalizar se necessário
        if imagem_array.max() > 255 or imagem_array.min() < 0:
            imagem_array = np.clip(imagem_array, 0, 255)
        
        imagem_array = imagem_array.astype(np.uint8)
        
        # Redimensionar mantendo proporção
        altura, largura = imagem_array.shape
        proporcao = min(self.largura/largura, self.altura/altura)
        
        if proporcao < 1:
            nova_largura = int(largura * proporcao)
            nova_altura = int(altura * proporcao)
            
            img_pil = Image.fromarray(imagem_array)
            img_pil = img_pil.resize((nova_largura, nova_altura), Image.LANCZOS)
            imagem_array = np.array(img_pil)
        
        # Converter para PhotoImage
        img_pil = Image.fromarray(imagem_array)
        self.photo_image = ImageTk.PhotoImage(img_pil)
        
        # Limpar canvas
        self.canvas.delete("all")
        
        # Centralizar imagem
        x = (self.largura - img_pil.width) // 2
        y = (self.altura - img_pil.height) // 2
        
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo_image)
        
        # Atualizar informações
        if info:
            self.label_info.config(text=info)
        else:
            self.label_info.config(text=f"{altura}x{largura}")
    
    def limpar(self):
        """Limpa o painel"""
        self.canvas.delete("all")
        self.imagem_atual = None
        self.photo_image = None
        self.label_info.config(text="Nenhuma imagem")
    
    def obter_imagem(self):
        """Retorna a imagem atual"""
        return self.imagem_atual


class PainelParametros(tk.LabelFrame):
    """
    Painel para ajuste de parâmetros
    """
    
    def __init__(self, parent, titulo="Parâmetros"):
        super().__init__(parent, text=titulo, font=('Arial', 10, 'bold'))
        
        self.parametros = {}
        self.widgets = {}
    
    def adicionar_slider(self, nome, label, minimo, maximo, valor_inicial, resolucao=0.1):
        """
        Adiciona um slider de parâmetro
        
        Args:
            nome (str): Nome do parâmetro
            label (str): Texto do label
            minimo (float): Valor mínimo
            maximo (float): Valor máximo
            valor_inicial (float): Valor inicial
            resolucao (float): Resolução do slider
        """
        frame = tk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Label
        tk.Label(frame, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        # Variável
        var = tk.DoubleVar(value=valor_inicial)
        self.parametros[nome] = var
        
        # Slider
        slider = tk.Scale(
            frame,
            from_=minimo,
            to=maximo,
            resolution=resolucao,
            orient=tk.HORIZONTAL,
            variable=var,
            length=200
        )
        slider.pack(side=tk.LEFT, padx=5)
        
        # Label do valor
        label_valor = tk.Label(frame, textvariable=var, width=6)
        label_valor.pack(side=tk.LEFT)
        
        self.widgets[nome] = {'frame': frame, 'slider': slider, 'var': var}
    
    def adicionar_checkbox(self, nome, label, valor_inicial=True):
        """
        Adiciona um checkbox
        """
        var = tk.BooleanVar(value=valor_inicial)
        self.parametros[nome] = var
        
        checkbox = tk.Checkbutton(self, text=label, variable=var)
        checkbox.pack(anchor=tk.W, padx=5, pady=2)
        
        self.widgets[nome] = {'checkbox': checkbox, 'var': var}
    
    def adicionar_combobox(self, nome, label, opcoes, valor_inicial=None):
        """
        Adiciona um combobox
        """
        frame = tk.Frame(self)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(frame, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        var = tk.StringVar(value=valor_inicial if valor_inicial else opcoes[0])
        self.parametros[nome] = var
        
        combo = ttk.Combobox(frame, textvariable=var, values=opcoes, state='readonly', width=15)
        combo.pack(side=tk.LEFT, padx=5)
        
        self.widgets[nome] = {'frame': frame, 'combo': combo, 'var': var}
    
    def obter_valores(self):
        """
        Retorna um dicionário com todos os valores dos parâmetros
        """
        return {nome: var.get() for nome, var in self.parametros.items()}
    
    def obter_valor(self, nome):
        """
        Retorna o valor de um parâmetro específico
        """
        return self.parametros[nome].get()


class JanelaProgresso(tk.Toplevel):
    """
    Janela de progresso para operações demoradas
    """
    
    def __init__(self, parent, titulo="Processando..."):
        super().__init__(parent)
        
        self.title(titulo)
        self.geometry("300x100")
        self.resizable(False, False)
        
        # Centralizar na tela
        self.transient(parent)
        self.grab_set()
        
        # Label
        self.label = tk.Label(self, text="Processando...", font=('Arial', 10))
        self.label.pack(pady=10)
        
        # Barra de progresso
        self.progressbar = ttk.Progressbar(
            self, 
            mode='indeterminate',
            length=250
        )
        self.progressbar.pack(pady=10)
        self.progressbar.start(10)
    
    def atualizar_mensagem(self, mensagem):
        """Atualiza a mensagem"""
        self.label.config(text=mensagem)
        self.update()
    
    def fechar(self):
        """Fecha a janela"""
        self.progressbar.stop()
        self.destroy()


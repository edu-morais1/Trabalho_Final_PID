import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os
import numpy as np

# Adicionar path do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algoritmos import (
    MarrHildreth, Canny, comparar_detectores,
    Otsu, Watershed, contar_objetos,
    CadeiaFreeman, FiltroBox, SegmentacaoCustomizada
)
from utils import carregar_imagem, salvar_imagem, plotar_comparacao
from interface.componentes import PainelImagem, JanelaProgresso


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Processamento de Imagens Digitais - Trabalho Final")
        self.geometry("1500x850") # Aumentei a largura para caber as 3 colunas
        
        self.imagem_original = None
        self.imagem_processada = None
        
        self.criar_menu()
        self.criar_interface()
        self.centralizar_janela()
    
    def centralizar_janela(self):
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f'{largura}x{altura}+{x}+{y}')

    def criar_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Abrir Imagem...", command=self.carregar_imagem, accelerator="Ctrl+O")
        menu_arquivo.add_command(label="Salvar Resultado...", command=self.salvar_resultado, accelerator="Ctrl+S")
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.quit)
        
        menu_questoes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Questões", menu=menu_questoes)
        
        menu_q1 = tk.Menu(menu_questoes, tearoff=0)
        menu_questoes.add_cascade(label="Q1: Detectores de Borda", menu=menu_q1)
        menu_q1.add_command(label="Marr-Hildreth", command=lambda: self.aplicar_detector('marr'))
        menu_q1.add_command(label="Canny", command=lambda: self.aplicar_detector('canny'))
        menu_q1.add_command(label="Otsu", command=lambda: self.aplicar_detector('otsu'))
        menu_q1.add_command(label="Watershed", command=lambda: self.aplicar_detector('watershed'))
        
        menu_questoes.add_command(label="Q2: Comparar Marr-Hildreth vs Canny", command=self.comparar_detectores)
        menu_questoes.add_command(label="Q3: Otsu + Contar Objetos", command=self.contar_objetos)
        menu_questoes.add_command(label="Q4: Cadeia de Freeman", command=self.aplicar_freeman)
        
        menu_q5 = tk.Menu(menu_questoes, tearoff=0)
        menu_questoes.add_cascade(label="Q5: Filtros Box", menu=menu_q5)
        for tam in [2, 3, 5, 7, 11, 21, 31]:
            menu_q5.add_command(label=f"Box {tam}x{tam}", command=lambda t=tam: self.aplicar_filtro_box(t))
        menu_q5.add_separator()
        menu_q5.add_command(label="Comparar Múltiplos", command=self.comparar_filtros_box)
        
        menu_questoes.add_command(label="Q6: Segmentação Customizada", command=self.aplicar_segmentacao_custom)

        self.bind('<Control-o>', lambda e: self.carregar_imagem())
        self.bind('<Control-s>', lambda e: self.salvar_resultado())

    def criar_interface(self):
        # Frame principal
        frame_principal = tk.Frame(self)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de Conteúdo (IMAGENS + CONSOLE lado a lado)
        frame_conteudo = tk.Frame(frame_principal)
        frame_conteudo.pack(fill=tk.BOTH, expand=True)
        
        # 1. Imagem Original
        self.painel_original = PainelImagem(frame_conteudo, "Imagem Original", 480, 480)
        self.painel_original.pack(side=tk.LEFT, padx=5, expand=True)
        
        # 2. Imagem Processada
        self.painel_processada = PainelImagem(frame_conteudo, "Imagem Processada", 480, 480)
        self.painel_processada.pack(side=tk.LEFT, padx=5, expand=True)
        
        # 3. Console (Agora à DIREITA da Imagem Processada)
        frame_console = tk.LabelFrame(frame_conteudo, text="Console de Saída", font=('Arial', 10, 'bold'))
        frame_console.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        self.text_console = tk.Text(frame_console, width=45, font=('Courier', 9))
        self.text_console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_console, command=self.text_console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_console.config(yscrollcommand=scrollbar.set)
        
        # Frame de Controles (EMBAIXO de tudo)
        frame_inferior = tk.Frame(frame_principal)
        frame_inferior.pack(fill=tk.X, pady=10)
        
        frame_controles = tk.LabelFrame(frame_inferior, text="Controles", font=('Arial', 10, 'bold'))
        frame_controles.pack(fill=tk.X, padx=5)
        
        tk.Button(frame_controles, text="📁 Abrir Imagem", command=self.carregar_imagem, 
                  font=('Arial', 10), width=18).pack(side=tk.LEFT, pady=5, padx=10)
        
        tk.Button(frame_controles, text="💾 Salvar Resultado", command=self.salvar_resultado, 
                  font=('Arial', 10), width=18).pack(side=tk.LEFT, pady=5, padx=10)
        
        tk.Button(frame_controles, text="🔄 Limpar Tudo", command=self.limpar_tudo, 
                  font=('Arial', 10), width=18).pack(side=tk.LEFT, pady=5, padx=10)
        
        sys.stdout = ConsoleRedirect(self.text_console)

    # --- MÉTODOS DE AÇÃO ---

    def carregar_imagem(self):
        caminho = filedialog.askopenfilename(title="Selecionar Imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"), ("Todos os arquivos", "*.*")])
        if caminho:
            try:
                self.imagem_original = carregar_imagem(caminho)
                self.painel_original.exibir_imagem(self.imagem_original)
                print(f"✓ Imagem carregada: {os.path.basename(caminho)}")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def salvar_resultado(self):
        if self.imagem_processada is None:
            messagebox.showwarning("Aviso", "Não há resultado para salvar.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".png")
        if caminho:
            salvar_imagem(self.imagem_processada, caminho)
            print(f"✓ Resultado salvo: {caminho}")

    def aplicar_detector(self, tipo):
        if self.imagem_original is None: return
        try:
            if tipo == 'marr':
                det = MarrHildreth(sigma=1.5, threshold=0.04)
                self.imagem_processada = det.aplicar(self.imagem_original)
            elif tipo == 'canny':
                det = Canny(sigma=1.4)
                self.imagem_processada = det.aplicar(self.imagem_original)
            elif tipo == 'otsu':
                det = Otsu()
                self.imagem_processada, _ = det.aplicar(self.imagem_original)
            elif tipo == 'watershed':
                det = Watershed()
                self.imagem_processada = det.aplicar(self.imagem_original)
            self.painel_processada.exibir_imagem(self.imagem_processada, tipo.upper())
        except Exception as e: print(f"Erro: {e}")

    def comparar_detectores(self):
        if self.imagem_original is None: return
        try:
            marr, canny = comparar_detectores(self.imagem_original)
            self.imagem_processada = canny
            self.painel_processada.exibir_imagem(canny, "Canny (Q2)")
            plotar_comparacao(marr, canny, "Marr-Hildreth", "Canny")
        except Exception as e: print(f"Erro na comparação: {e}")

    def contar_objetos(self):
        if self.imagem_original is None: return
        otsu = Otsu()
        bin_img, _ = otsu.aplicar(self.imagem_original)
        n, _ = contar_objetos(bin_img)
        self.imagem_processada = bin_img
        self.painel_processada.exibir_imagem(bin_img, f"{n} objetos detectados")

    def aplicar_freeman(self):
        if self.imagem_original is None: return
        otsu = Otsu()
        bin_img, _ = otsu.aplicar(self.imagem_original)
        freeman = CadeiaFreeman()
        res = freeman.aplicar(bin_img)
        if res:
            contorno = freeman.visualizar_contorno(self.imagem_original, res['contorno'])
            self.imagem_processada = contorno
            self.painel_processada.exibir_imagem(contorno, f"Freeman ({len(res['contorno'])} pontos)")

    def aplicar_filtro_box(self, tam):
        if self.imagem_original is None: return
        f = FiltroBox()
        self.imagem_processada = f.aplicar(self.imagem_original, tam)
        self.painel_processada.exibir_imagem(self.imagem_processada, f"Box {tam}x{tam}")

    def comparar_filtros_box(self):
        if self.imagem_original is None: return
        f = FiltroBox()
        f.aplicar_multiplos(self.imagem_original, [3, 5, 7, 11])

    def aplicar_segmentacao_custom(self):
        if self.imagem_original is None: return
        s = SegmentacaoCustomizada()
        self.imagem_processada = s.aplicar(self.imagem_original)
        self.painel_processada.exibir_imagem(self.imagem_processada, "Posterização")

    def limpar_tudo(self):
        self.imagem_original = None
        self.imagem_processada = None
        self.painel_original.limpar()
        self.painel_processada.limpar()
        self.text_console.delete(1.0, tk.END)

class ConsoleRedirect:
    def __init__(self, text_widget): self.text_widget = text_widget
    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
    def flush(self): pass

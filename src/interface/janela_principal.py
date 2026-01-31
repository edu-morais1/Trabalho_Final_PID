"""
Interface Gráfica Principal do Sistema

Autor: [Seu Nome]
Data: Janeiro/2026
"""

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
from interface.componentes import PainelImagem, PainelParametros, JanelaProgresso


class JanelaPrincipal(tk.Tk):
    """
    Interface principal do sistema de processamento de imagens
    """
    
    def __init__(self):
        super().__init__()
        
        self.title("Processamento de Imagens Digitais - Trabalho Final")
        self.geometry("1400x900")
        
        # Variáveis
        self.imagem_original = None
        self.imagem_processada = None
        self.caminho_imagem_atual = None
        self.resultado_freeman = None
        
        # Criar interface
        self.criar_menu()
        self.criar_interface()
        
        # Centralizar janela
        self.centralizar_janela()
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)
        self.geometry(f'{largura}x{altura}+{x}+{y}')
    
    def criar_menu(self):
        """Cria a barra de menu"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Abrir Imagem...", command=self.carregar_imagem, accelerator="Ctrl+O")
        menu_arquivo.add_command(label="Salvar Resultado...", command=self.salvar_resultado, accelerator="Ctrl+S")
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.quit)
        
        # Menu Questões
        menu_questoes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Questões", menu=menu_questoes)
        
        # Q1: Detectores
        menu_q1 = tk.Menu(menu_questoes, tearoff=0)
        menu_questoes.add_cascade(label="Q1: Detectores de Borda", menu=menu_q1)
        menu_q1.add_command(label="Marr-Hildreth", command=lambda: self.aplicar_detector('marr'))
        menu_q1.add_command(label="Canny", command=lambda: self.aplicar_detector('canny'))
        menu_q1.add_command(label="Otsu", command=lambda: self.aplicar_detector('otsu'))
        menu_q1.add_command(label="Watershed", command=lambda: self.aplicar_detector('watershed'))
        
        # Q2: Comparativo
        menu_questoes.add_command(label="Q2: Comparar Marr-Hildreth vs Canny", command=self.comparar_detectores)
        
        # Q3: Contar objetos
        menu_questoes.add_command(label="Q3: Otsu + Contar Objetos", command=self.contar_objetos)
        
        # Q4: Freeman
        menu_questoes.add_command(label="Q4: Cadeia de Freeman", command=self.aplicar_freeman)
        
        # Q5: Filtros Box
        menu_q5 = tk.Menu(menu_questoes, tearoff=0)
        menu_questoes.add_cascade(label="Q5: Filtros Box", menu=menu_q5)
        for tam in [2, 3, 5, 7, 11, 21, 31]:
            menu_q5.add_command(label=f"Box {tam}x{tam}", command=lambda t=tam: self.aplicar_filtro_box(t))
        menu_q5.add_separator()
        menu_q5.add_command(label="Comparar Múltiplos", command=self.comparar_filtros_box)
        
        # Q6: Segmentação Custom
        menu_questoes.add_command(label="Q6: Segmentação Customizada", command=self.aplicar_segmentacao_custom)
        
        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
        
        # Atalhos
        self.bind('<Control-o>', lambda e: self.carregar_imagem())
        self.bind('<Control-s>', lambda e: self.salvar_resultado())
    
    def criar_interface(self):
        """Cria os componentes da interface"""
        
        # Frame principal
        frame_principal = tk.Frame(self)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior (imagens)
        frame_imagens = tk.Frame(frame_principal)
        frame_imagens.pack(fill=tk.BOTH, expand=True)
        
        # Painel imagem original
        self.painel_original = PainelImagem(frame_imagens, "Imagem Original", 500, 500)
        self.painel_original.pack(side=tk.LEFT, padx=5)
        
        # Painel imagem processada
        self.painel_processada = PainelImagem(frame_imagens, "Imagem Processada", 500, 500)
        self.painel_processada.pack(side=tk.LEFT, padx=5)
        
        # Frame inferior (controles)
        frame_controles = tk.Frame(frame_principal)
        frame_controles.pack(fill=tk.X, pady=10)
        
        # Botões principais
        frame_botoes = tk.Frame(frame_controles)
        frame_botoes.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botoes,
            text="📁 Carregar Imagem",
            command=self.carregar_imagem,
            font=('Arial', 10),
            width=20,
            height=2
        ).pack(pady=2)
        
        tk.Button(
            frame_botoes,
            text="💾 Salvar Resultado",
            command=self.salvar_resultado,
            font=('Arial', 10),
            width=20,
            height=2
        ).pack(pady=2)
        
        tk.Button(
            frame_botoes,
            text="🔄 Limpar",
            command=self.limpar_tudo,
            font=('Arial', 10),
            width=20,
            height=2
        ).pack(pady=2)
        
        # Painel de parâmetros
        self.painel_parametros = PainelParametros(frame_controles, "Parâmetros")
        self.painel_parametros.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Console de saída
        frame_console = tk.LabelFrame(frame_controles, text="Console", font=('Arial', 10, 'bold'))
        frame_console.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        
        self.text_console = tk.Text(frame_console, height=8, width=40, font=('Courier', 9))
        self.text_console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_console, command=self.text_console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_console.config(yscrollcommand=scrollbar.set)
        
        # Redirecionar print para console
        sys.stdout = ConsoleRedirect(self.text_console)
    
    def carregar_imagem(self):
        """Carrega uma imagem"""
        caminho = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if not caminho:
            return
        
        try:
            self.imagem_original = carregar_imagem(caminho)
            self.caminho_imagem_atual = caminho
            
            # Exibir
            self.painel_original.exibir_imagem(
                self.imagem_original,
                f"{self.imagem_original.shape[0]}x{self.imagem_original.shape[1]}"
            )
            
            print(f"✓ Imagem carregada: {os.path.basename(caminho)}")
            print(f"  Dimensões: {self.imagem_original.shape}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{str(e)}")
    
    def salvar_resultado(self):
        """Salva a imagem processada"""
        if self.imagem_processada is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem processada para salvar")
            return
        
        caminho = filedialog.asksaveasfilename(
            title="Salvar Resultado",
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg"),
                ("BMP", "*.bmp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if not caminho:
            return
        
        try:
            salvar_imagem(self.imagem_processada, caminho)
            print(f"✓ Resultado salvo: {os.path.basename(caminho)}")
            messagebox.showinfo("Sucesso", "Imagem salva com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar imagem:\n{str(e)}")
    
    def aplicar_detector(self, tipo):
        """Aplica um detector de borda"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        try:
            if tipo == 'marr':
                detector = MarrHildreth(sigma=1.5, threshold=0.04)
                self.imagem_processada = detector.aplicar(self.imagem_original)
                self.painel_processada.exibir_imagem(self.imagem_processada, "Marr-Hildreth")
                
            elif tipo == 'canny':
                detector = Canny(sigma=1.4, threshold_low=0.04, threshold_high=0.10)
                self.imagem_processada = detector.aplicar(self.imagem_original)
                self.painel_processada.exibir_imagem(self.imagem_processada, "Canny")
                
            elif tipo == 'otsu':
                otsu = Otsu()
                self.imagem_processada, threshold = otsu.aplicar(self.imagem_original)
                self.painel_processada.exibir_imagem(
                    self.imagem_processada,
                    f"Otsu (T={threshold})"
                )
                
            elif tipo == 'watershed':
                watershed = Watershed(suavizacao=True, sigma=1.0)
                self.imagem_processada = watershed.aplicar(self.imagem_original)
                self.painel_processada.exibir_imagem(self.imagem_processada, "Watershed")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar:\n{str(e)}")
            print(f"ERRO: {str(e)}")
    
    def comparar_detectores(self):
        """Compara Marr-Hildreth vs Canny (Q2)"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        try:
            marr, canny = comparar_detectores(self.imagem_original)
            
            # Mostrar Canny no painel
            self.imagem_processada = canny
            self.painel_processada.exibir_imagem(canny, "Canny (melhor)")
            
            # Mostrar comparação em matplotlib
            plotar_comparacao(marr, canny, "Marr-Hildreth", "Canny")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao comparar:\n{str(e)}")
    
    def contar_objetos(self):
        """Aplica Otsu e conta objetos (Q3)"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        try:
            # Aplicar Otsu
            otsu = Otsu()
            img_bin, threshold = otsu.aplicar(self.imagem_original)
            
            # Contar objetos
            num_objetos, img_rotulada = contar_objetos(img_bin)
            
            # Exibir
            self.imagem_processada = img_bin
            self.painel_processada.exibir_imagem(
                img_bin,
                f"{num_objetos} objetos encontrados"
            )
            
            messagebox.showinfo(
                "Contagem de Objetos",
                f"Número de objetos encontrados: {num_objetos}"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao contar objetos:\n{str(e)}")
    
    def aplicar_freeman(self):
        """Aplica Cadeia de Freeman (Q4)"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        try:
            # Primeiro binarizar com Otsu
            otsu = Otsu()
            img_bin, _ = otsu.aplicar(self.imagem_original)
            
            # Aplicar Freeman
            freeman = CadeiaFreeman()
            self.resultado_freeman = freeman.aplicar(img_bin)
            
            if self.resultado_freeman is None:
                return
            
            # Visualizar contorno
            contorno_img = freeman.visualizar_contorno(
                self.imagem_original,
                self.resultado_freeman['contorno']
            )
            
            self.imagem_processada = contorno_img
            self.painel_processada.exibir_imagem(
                contorno_img,
                f"Contorno ({len(self.resultado_freeman['contorno'])} pontos)"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar Freeman:\n{str(e)}")
    
    def aplicar_filtro_box(self, tamanho):
        """Aplica filtro Box (Q5)"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        try:
            filtro = FiltroBox()
            self.imagem_processada = filtro.aplicar(self.imagem_original, tamanho)
            self.painel_processada.exibir_imagem(
                self.imagem_processada,
                f"Box {tamanho}x{tamanho}"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao aplicar filtro:\n{str(e)}")
    
    def comparar_filtros_box(self):
        """Compara múltiplos tamanhos de filtro Box"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        try:
            filtro = FiltroBox()
            resultados = filtro.aplicar_multiplos(self.imagem_original, [3, 5, 7, 11])
            
            # Mostrar o último no painel
            self.imagem_processada = resultados[11]
            self.painel_processada.exibir_imagem(resultados[11], "Box 11x11")
            
            print("Comparação de filtros concluída. Ver console.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao comparar filtros:\n{str(e)}")
    
    def aplicar_segmentacao_custom(self):
        """Aplica segmentação customizada (Q6)"""
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        try:
            segmentador = SegmentacaoCustomizada()
            self.imagem_processada = segmentador.aplicar(self.imagem_original)
            
            self.painel_processada.exibir_imagem(
                self.imagem_processada,
                "Segmentação Customizada"
            )
            
            # Analisar
            segmentador.analisar_distribuicao(self.imagem_original, self.imagem_processada)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao segmentar:\n{str(e)}")
    
    def limpar_tudo(self):
        """Limpa todas as imagens e reseta interface"""
        self.imagem_original = None
        self.imagem_processada = None
        self.painel_original.limpar()
        self.painel_processada.limpar()
        self.text_console.delete(1.0, tk.END)
        print("Interface limpa")
    
    def mostrar_sobre(self):
        """Mostra informações sobre o sistema"""
        messagebox.showinfo(
            "Sobre",
            "Processamento de Imagens Digitais\n"
            "Trabalho Final\n\n"
            "Aluno: [Seu Nome]\n"
            "Curso: Ciência da Computação\n"
            "UNIOESTE - Campus Cascavel\n"
            "Data: Fevereiro/2026\n\n"
            "Professor: [Nome do Professor]\n\n"
            "Implementa:\n"
            "• Detectores de borda (Marr-Hildreth, Canny)\n"
            "• Segmentação (Otsu, Watershed)\n"
            "• Cadeia de Freeman\n"
            "• Filtros Box\n"
            "• Segmentação customizada"
        )


class ConsoleRedirect:
    """Redireciona saída do print para o widget Text"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
    
    def write(self, text):
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
    
    def flush(self):
        pass


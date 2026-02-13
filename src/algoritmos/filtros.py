import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.processamento import adicionar_padding


class FiltroBox:
    """
    Filtro Box (Filtro da Média)
    
    Filtro passa-baixa com pesos uniformes
    - Reduz ruído
    - Causa borramento (smoothing)
    - Maior a máscara, maior o efeito
    
    Máscara nxn: todos os elementos = 1/(n²)
   
    """
    
    def criar_mascara(self, tamanho):
        """
        Cria máscara do filtro Box
        
        Args:
            tamanho (int): Tamanho da máscara (2, 3, 5, 7, 11, etc.)
            
        Returns:
            numpy.ndarray: Máscara normalizada
        """
        # Todos os elementos têm peso igual
        mascara = np.ones((tamanho, tamanho), dtype=np.float64)
        
        # Normalizar (soma = 1)
        mascara = mascara / (tamanho * tamanho)
        
        return mascara
    
    def aplicar_manual(self, imagem, tamanho):
        """
        Aplica filtro Box manualmente (sem usar funções prontas)
        
        Implementação manual conforme solicitado no trabalho
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            tamanho (int): Tamanho da máscara
            
        Returns:
            numpy.ndarray: Imagem filtrada
        """
        print(f"Aplicando Filtro Box {tamanho}x{tamanho}...")
        
        altura, largura = imagem.shape
        
        # Criar máscara
        mascara = self.criar_mascara(tamanho)
        
        # Calcular padding
        pad = tamanho // 2
        
        # Adicionar padding (repetir bordas)
        img_padded = adicionar_padding(imagem, pad, valor=0)
        
        # Criar imagem de saída
        resultado = np.zeros_like(imagem, dtype=np.float64)
        
        # Aplicar filtro (convolução manual)
        for i in range(altura):
            for j in range(largura):
                # Extrair região
                regiao = img_padded[i:i+tamanho, j:j+tamanho]
                
                # Calcular média ponderada
                resultado[i, j] = np.sum(regiao * mascara)
        
        print(f"Filtro Box {tamanho}x{tamanho} aplicado com sucesso")
        
        return resultado.astype(np.uint8)
    
    def aplicar(self, imagem, tamanho):
        """
        Aplica filtro Box (Questão 5)
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            tamanho (int): Tamanho da máscara (2, 3, 5, 7, 11, 21, etc.)
            
        Returns:
            numpy.ndarray: Imagem filtrada
            
       """
        # Verificar tamanho da imagem
        altura, largura = imagem.shape
        tamanho_img = max(altura, largura)
        
        if tamanho_img > 1024 and tamanho < 11:
            print(f"AVISO: Imagem grande ({altura}x{largura})")
            print(f"       Considere usar máscara maior (11x11, 21x21, 31x31)")
        
        return self.aplicar_manual(imagem, tamanho)
    
    def aplicar_multiplos(self, imagem, tamanhos=[2, 3, 5, 7]):
        """
        Aplica múltiplos tamanhos de filtro Box (para comparação)
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            tamanhos (list): Lista de tamanhos a aplicar
            
        Returns:
            dict: Dicionário {tamanho: imagem_filtrada}
        """
        resultados = {}
        
        print("\n" + "="*60)
        print(f"APLICANDO FILTROS BOX: {tamanhos}")
        print("="*60 + "\n")
        
        for tamanho in tamanhos:
            resultado = self.aplicar(imagem, tamanho)
            resultados[tamanho] = resultado
        
        print("="*60 + "\n")
        
        return resultados


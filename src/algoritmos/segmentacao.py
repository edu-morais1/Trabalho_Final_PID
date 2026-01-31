"""
Algoritmos de Segmentação: Otsu e Watershed

Autor: [Seu Nome]
Data: Janeiro/2026

Referências:
- Otsu, N. (1979). A threshold selection method from gray-level histograms
- Aula 13 - Segmentação de Imagens (Prof. Matheus Raffael Simon)
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.processamento import criar_histograma, calcular_gradiente, convolucao, criar_mascara_gaussiana


class Otsu:
    """
    Método de limiarização de Otsu (1979)
    
    Determina o limiar ótimo que maximiza a variância entre classes
    (foreground e background)
    
    Fórmula: σ²(t) = w_b(t) * w_f(t) * [m_b(t) - m_f(t)]²
    
    Onde:
    - w_b: peso do background
    - w_f: peso do foreground
    - m_b: média do background
    - m_f: média do foreground
    
    Referência: Slides 63-64, Aula 13
    """
    
    def calcular_threshold(self, imagem):
        """
        Calcula o threshold ótimo pelo método de Otsu
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            
        Returns:
            int: Threshold ótimo (0-255)
        """
        # 1. Construir histograma
        histograma = criar_histograma(imagem)
        total_pixels = imagem.size
        
        # 2. Inicializar variáveis
        max_variancia = 0
        threshold_otimo = 0
        soma_total = np.sum(np.arange(256) * histograma)
        
        # 3. Percorrer todos os possíveis thresholds
        peso_background = 0
        soma_background = 0
        
        for t in range(256):
            # Atualizar peso e soma do background
            peso_background += histograma[t]
            
            if peso_background == 0:
                continue
            
            # Calcular peso do foreground
            peso_foreground = total_pixels - peso_background
            
            if peso_foreground == 0:
                break
            
            # Atualizar soma do background
            soma_background += t * histograma[t]
            
            # Calcular médias
            media_background = soma_background / peso_background
            media_foreground = (soma_total - soma_background) / peso_foreground
            
            # Calcular variância entre classes
            variancia_entre = (peso_background / total_pixels) * \
                             (peso_foreground / total_pixels) * \
                             (media_background - media_foreground) ** 2
            
            # Atualizar threshold se variância for maior
            if variancia_entre > max_variancia:
                max_variancia = variancia_entre
                threshold_otimo = t
        
        print(f"Otsu: threshold ótimo = {threshold_otimo}, variância = {max_variancia:.6f}")
        
        return threshold_otimo
    
    def aplicar(self, imagem):
        """
        Aplica o método de Otsu para segmentação
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            
        Returns:
            tuple: (imagem_binaria, threshold)
        """
        threshold = self.calcular_threshold(imagem)
        
        # Aplicar threshold
        imagem_binaria = (imagem >= threshold).astype(np.uint8) * 255
        
        return imagem_binaria, threshold


def contar_objetos(imagem_binaria):
    """
    Conta objetos em uma imagem binária (Questão 3)
    
    Usa rotulação de componentes conectados (8-conectividade)
    
    Args:
        imagem_binaria (numpy.ndarray): Imagem binária (0 ou 255)
        
    Returns:
        tuple: (num_objetos, imagem_rotulada)
        
    Referência: Componentes Conexos - Fundamentos
    """
    # Normalizar para 0 e 1
    imagem_bin = (imagem_binaria > 0).astype(int)
    
    altura, largura = imagem_bin.shape
    rotulos = np.zeros((altura, largura), dtype=int)
    rotulo_atual = 1
    
    # Percorrer a imagem
    for i in range(altura):
        for j in range(largura):
            if imagem_bin[i, j] == 1 and rotulos[i, j] == 0:
                # Novo objeto encontrado - usar flood fill
                pilha = [(i, j)]
                rotulos[i, j] = rotulo_atual
                
                while pilha:
                    y, x = pilha.pop()
                    
                    # Verificar vizinhos 8-conectados
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            
                            ny, nx = y + dy, x + dx
                            
                            # Verificar limites
                            if 0 <= ny < altura and 0 <= nx < largura:
                                if imagem_bin[ny, nx] == 1 and rotulos[ny, nx] == 0:
                                    rotulos[ny, nx] = rotulo_atual
                                    pilha.append((ny, nx))
                
                rotulo_atual += 1
    
    num_objetos = rotulo_atual - 1
    print(f"Contagem: {num_objetos} objetos encontrados")
    
    return num_objetos, rotulos


class Watershed:
    """
    Segmentação por Watershed (Bacias Hidrográficas)
    
    Conceito: Trata a imagem como uma topografia 3D onde:
    - Intensidade = altitude
    - Mínimos regionais = vales (objetos)
    - Divisores de água = fronteiras entre objetos
    
    Implementação simplificada usando marcadores
    
    Referência: Slides 85-97, Aula 13
    """
    
    def __init__(self, suavizacao=True, sigma=1.0):
        """
        Inicializa Watershed
        
        Args:
            suavizacao (bool): Se deve suavizar antes
            sigma (float): Sigma para suavização
        """
        self.suavizacao = suavizacao
        self.sigma = sigma
    
    def aplicar(self, imagem, marcadores=None):
        """
        Aplica segmentação Watershed
        
        Implementação simplificada baseada no gradiente morfológico
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            marcadores (numpy.ndarray, opcional): Marcadores dos objetos
            
        Returns:
            numpy.ndarray: Imagem segmentada
        """
        print("Watershed: aplicando segmentação...")
        
        # 1. Suavizar imagem se solicitado
        if self.suavizacao:
            tamanho = int(np.ceil(6 * self.sigma))
            if tamanho % 2 == 0:
                tamanho += 1
            mascara = criar_mascara_gaussiana(tamanho, self.sigma)
            imagem = convolucao(imagem, mascara)
        
        # 2. Calcular gradiente (magnitude)
        magnitude, _ = calcular_gradiente(imagem, metodo='sobel')
        
        # 3. Se não houver marcadores, usar Otsu para criar marcadores básicos
        if marcadores is None:
            otsu = Otsu()
            imagem_bin, _ = otsu.aplicar(imagem)
            marcadores = imagem_bin
        
        # 4. Aplicar threshold no gradiente para obter fronteiras
        # (implementação simplificada - a versão completa requer algoritmo complexo)
        threshold_grad = np.percentile(magnitude, 85)
        fronteiras = (magnitude > threshold_grad).astype(np.uint8) * 255
        
        # 5. Combinar marcadores com fronteiras
        resultado = marcadores.copy()
        resultado[fronteiras > 0] = 128  # Cinza para fronteiras
        
        print("Watershed: segmentação concluída")
        print("Nota: Esta é uma implementação simplificada")
        print("Para resultados melhores, usar scipy.ndimage.watershed_ift")
        
        return resultado


"""
Detectores de Borda: Marr-Hildreth e Canny

Autor: [Seu Nome]
Data: Janeiro/2026

Referências:
- Marr, D., Hildreth, E. (1980). Theory of Edge Detection
- Canny, J. (1986). A Computational Approach to Edge Detection
- Aula 13 - Segmentação de Imagens (Prof. Matheus Raffael Simon)
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.processamento import (
    criar_mascara_gaussiana, 
    convolucao, 
    calcular_gradiente,
    normalizar_imagem
)


class MarrHildreth:
    """
    Detector de bordas de Marr-Hildreth (1980)
    
    Teoria:
    - Utiliza o Laplaciano da Gaussiana (LoG)
    - Detecta bordas através de cruzamentos por zero
    - Formula LoG: ∇²G(x,y) = [(x²+y²-2σ⁴)/σ⁴] * e^(-(x²+y²)/(2σ²))
    - Tamanho da máscara: n = menor ímpar > 6σ
    
    Passos:
    1. Filtrar com Gaussiano passa-baixa
    2. Calcular Laplaciano
    3. Encontrar cruzamentos por zero
    4. Aplicar threshold
    
    Referência: Slides 26-32, Aula 13
    """
    
    def __init__(self, sigma=1.5, threshold=0.04):
        """
        Inicializa o detector Marr-Hildreth
        
        Args:
            sigma (float): Desvio padrão do filtro Gaussiano
            threshold (float): Limiar para validar cruzamentos (% do max LoG)
        """
        self.sigma = sigma
        self.threshold = threshold
        
    def criar_log(self, tamanho, sigma):
        """
        Cria a máscara Laplaciano da Gaussiana (LoG)
        
        Fórmula: ∇²G(x,y) = [(x²+y²-2σ⁴)/σ⁴] * e^(-(x²+y²)/(2σ²))
        
        Args:
            tamanho (int): Tamanho da máscara (deve ser ímpar)
            sigma (float): Desvio padrão
            
        Returns:
            numpy.ndarray: Máscara LoG
        """
        # Garantir tamanho ímpar
        if tamanho % 2 == 0:
            tamanho += 1
            
        centro = tamanho // 2
        log_mask = np.zeros((tamanho, tamanho))
        
        # Calcular valores do LoG
        for i in range(tamanho):
            for j in range(tamanho):
                x = i - centro
                y = j - centro
                r2 = x**2 + y**2
                sigma2 = sigma**2
                sigma4 = sigma**4
                
                # Fórmula do LoG
                log_mask[i, j] = ((r2 - 2*sigma2) / sigma4) * np.exp(-r2 / (2*sigma2))
        
        return log_mask
    
    def encontrar_cruzamentos_zero(self, imagem_log, threshold_abs):
        """
        Encontra cruzamentos por zero no LoG
        
        Um cruzamento por zero ocorre quando vizinhos opostos têm sinais diferentes
        e a diferença entre eles excede o threshold
        
        Args:
            imagem_log (numpy.ndarray): Imagem após aplicar LoG
            threshold_abs (float): Threshold absoluto
            
        Returns:
            numpy.ndarray: Imagem binária com bordas
            
        Referência: Slide 31, Aula 13
        """
        altura, largura = imagem_log.shape
        bordas = np.zeros((altura, largura), dtype=np.uint8)
        
        # Percorrer a imagem (exceto bordas)
        for i in range(1, altura-1):
            for j in range(1, largura-1):
                pixel = imagem_log[i, j]
                
                # Verificar os 4 pares de vizinhos opostos
                # p4-p5 (esquerda-direita)
                if (pixel * imagem_log[i, j-1] < 0 and 
                    abs(pixel - imagem_log[i, j-1]) > threshold_abs):
                    bordas[i, j] = 255
                    continue
                
                # p2-p7 (cima-baixo)
                if (pixel * imagem_log[i-1, j] < 0 and 
                    abs(pixel - imagem_log[i-1, j]) > threshold_abs):
                    bordas[i, j] = 255
                    continue
                
                # p1-p8 (diagonal \)
                if (pixel * imagem_log[i-1, j-1] < 0 and 
                    abs(pixel - imagem_log[i-1, j-1]) > threshold_abs):
                    bordas[i, j] = 255
                    continue
                
                # p3-p6 (diagonal /)
                if (pixel * imagem_log[i-1, j+1] < 0 and 
                    abs(pixel - imagem_log[i-1, j+1]) > threshold_abs):
                    bordas[i, j] = 255
        
        return bordas
    
    def aplicar(self, imagem):
        """
        Aplica o detector de Marr-Hildreth
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            
        Returns:
            numpy.ndarray: Imagem binária com bordas detectadas
        """
        # 1. Calcular tamanho da máscara: n = menor ímpar > 6σ
        tamanho = int(np.ceil(6 * self.sigma))
        if tamanho % 2 == 0:
            tamanho += 1
        
        print(f"Marr-Hildreth: σ={self.sigma}, tamanho máscara={tamanho}x{tamanho}")
        
        # 2. Criar máscara LoG
        log_mask = self.criar_log(tamanho, self.sigma)
        
        # 3. Aplicar convolução com LoG
        imagem_log = convolucao(imagem, log_mask)
        
        # 4. Calcular threshold absoluto (% do valor máximo absoluto)
        max_abs = np.max(np.abs(imagem_log))
        threshold_abs = self.threshold * max_abs
        
        print(f"Marr-Hildreth: max(|LoG|)={max_abs:.2f}, threshold={threshold_abs:.2f}")
        
        # 5. Encontrar cruzamentos por zero
        bordas = self.encontrar_cruzamentos_zero(imagem_log, threshold_abs)
        
        return bordas


class Canny:
    """
    Detector de bordas de Canny (1986)
    
    Considerado o melhor detector de bordas
    
    Objetivos:
    1. Baixa taxa de erros (bordas verdadeiras)
    2. Boa localização (próximo ao centro da borda)
    3. Resposta única por borda
    
    Passos:
    1. Suavização com Gaussiano
    2. Cálculo do gradiente (magnitude e direção)
    3. Supressão não-máxima
    4. Dupla limiarização com histerese
    
    Referência: Slides 33-38, Aula 13
    """
    
    def __init__(self, sigma=1.4, threshold_low=0.04, threshold_high=0.10):
        """
        Inicializa o detector Canny
        
        Args:
            sigma (float): Desvio padrão do filtro Gaussiano
            threshold_low (float): Limiar baixo (% do máximo)
            threshold_high (float): Limiar alto (% do máximo)
            
        Nota: Razão recomendada TH:TL = 2:1 ou 3:1
        """
        self.sigma = sigma
        self.threshold_low = threshold_low
        self.threshold_high = threshold_high
    
    def supressao_nao_maxima(self, magnitude, direcao):
        """
        Aplica supressão não-máxima para afinar bordas
        
        Compara o pixel com seus vizinhos na direção do gradiente.
        Mantém apenas os máximos locais.
        
        Direções:
        - 0° (horizontal): compara com pixels à esquerda e direita
        - 45°: compara com diagonais NO-SE
        - 90° (vertical): compara com pixels acima e abaixo
        - 135°: compara com diagonais NE-SO
        
        Args:
            magnitude (numpy.ndarray): Magnitude do gradiente
            direcao (numpy.ndarray): Direção do gradiente (radianos)
            
        Returns:
            numpy.ndarray: Magnitude após supressão não-máxima
            
        Referência: Slides 35-36, Aula 13
        """
        altura, largura = magnitude.shape
        resultado = np.zeros((altura, largura))
        
        # Converter radianos para graus e normalizar para 0-180
        angulo = np.rad2deg(direcao) % 180
        
        for i in range(1, altura-1):
            for j in range(1, largura-1):
                mag = magnitude[i, j]
                ang = angulo[i, j]
                
                # Determinar direção e vizinhos a comparar
                # Direção 0° (horizontal): comparar p4 e p5
                if (0 <= ang < 22.5) or (157.5 <= ang <= 180):
                    vizinho1 = magnitude[i, j-1]
                    vizinho2 = magnitude[i, j+1]
                
                # Direção 45°: comparar p3 e p6
                elif 22.5 <= ang < 67.5:
                    vizinho1 = magnitude[i-1, j+1]
                    vizinho2 = magnitude[i+1, j-1]
                
                # Direção 90° (vertical): comparar p2 e p7
                elif 67.5 <= ang < 112.5:
                    vizinho1 = magnitude[i-1, j]
                    vizinho2 = magnitude[i+1, j]
                
                # Direção 135°: comparar p1 e p8
                else:  # 112.5 <= ang < 157.5
                    vizinho1 = magnitude[i-1, j-1]
                    vizinho2 = magnitude[i+1, j+1]
                
                # Manter pixel se for máximo local
                if mag >= vizinho1 and mag >= vizinho2:
                    resultado[i, j] = mag
        
        return resultado
    
    def dupla_limiarizacao_histerese(self, magnitude_suprimida, threshold_low_abs, threshold_high_abs):
        """
        Aplica dupla limiarização com histerese
        
        Cria duas imagens:
        - Bordas fortes: magnitude > threshold_high
        - Bordas fracas: threshold_low < magnitude < threshold_high
        
        Conecta bordas fracas que estão ligadas a bordas fortes
        
        Args:
            magnitude_suprimida (numpy.ndarray): Magnitude após supressão não-máxima
            threshold_low_abs (float): Threshold baixo absoluto
            threshold_high_abs (float): Threshold alto absoluto
            
        Returns:
            numpy.ndarray: Imagem binária com bordas finais
            
        Referência: Slides 37-38, Aula 13
        """
        altura, largura = magnitude_suprimida.shape
        
        # Criar imagens de bordas fortes e fracas
        bordas_fortes = (magnitude_suprimida >= threshold_high_abs).astype(np.uint8)
        bordas_fracas = ((magnitude_suprimida >= threshold_low_abs) & 
                        (magnitude_suprimida < threshold_high_abs)).astype(np.uint8)
        
        # Resultado final (inicialmente apenas bordas fortes)
        resultado = bordas_fortes.copy()
        
        # Conectar bordas fracas que estão ligadas a bordas fortes (conectividade-8)
        alterado = True
        while alterado:
            alterado = False
            for i in range(1, altura-1):
                for j in range(1, largura-1):
                    # Se é borda fraca e ainda não foi adicionada
                    if bordas_fracas[i, j] == 1 and resultado[i, j] == 0:
                        # Verificar se tem vizinho forte (8-conectividade)
                        vizinhanca = resultado[i-1:i+2, j-1:j+2]
                        if np.any(vizinhanca == 1):
                            resultado[i, j] = 1
                            alterado = True
        
        return (resultado * 255).astype(np.uint8)
    
    def aplicar(self, imagem):
        """
        Aplica o detector de Canny
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            
        Returns:
            numpy.ndarray: Imagem binária com bordas detectadas
        """
        print(f"Canny: σ={self.sigma}, TL={self.threshold_low}, TH={self.threshold_high}")
        
        # 1. Suavização com filtro Gaussiano
        tamanho_mask = int(np.ceil(6 * self.sigma))
        if tamanho_mask % 2 == 0:
            tamanho_mask += 1
        
        mascara_gaussiana = criar_mascara_gaussiana(tamanho_mask, self.sigma)
        imagem_suavizada = convolucao(imagem, mascara_gaussiana)
        
        # 2. Calcular gradiente (magnitude e direção)
        magnitude, direcao = calcular_gradiente(imagem_suavizada, metodo='sobel')
        
        # 3. Supressão não-máxima
        magnitude_suprimida = self.supressao_nao_maxima(magnitude, direcao)
        
        # 4. Calcular thresholds absolutos
        max_mag = np.max(magnitude_suprimida)
        threshold_low_abs = self.threshold_low * max_mag
        threshold_high_abs = self.threshold_high * max_mag
        
        print(f"Canny: max_magnitude={max_mag:.2f}, TL_abs={threshold_low_abs:.2f}, TH_abs={threshold_high_abs:.2f}")
        
        # 5. Dupla limiarização com histerese
        bordas = self.dupla_limiarizacao_histerese(
            magnitude_suprimida, 
            threshold_low_abs, 
            threshold_high_abs
        )
        
        return bordas


def comparar_detectores(imagem, sigma_marr=1.5, sigma_canny=1.4, 
                       threshold_marr=0.04, threshold_low=0.04, threshold_high=0.10):
    """
    Compara os detectores Marr-Hildreth e Canny (Questão 2)
    
    Args:
        imagem (numpy.ndarray): Imagem em escala de cinza
        sigma_marr (float): Sigma para Marr-Hildreth
        sigma_canny (float): Sigma para Canny
        threshold_marr (float): Threshold para Marr-Hildreth
        threshold_low (float): Threshold baixo para Canny
        threshold_high (float): Threshold alto para Canny
        
    Returns:
        tuple: (bordas_marr, bordas_canny)
    """
    print("\n" + "="*60)
    print("COMPARAÇÃO: Marr-Hildreth vs Canny")
    print("="*60)
    
    # Aplicar Marr-Hildreth
    print("\n--- Marr-Hildreth ---")
    marr = MarrHildreth(sigma=sigma_marr, threshold=threshold_marr)
    bordas_marr = marr.aplicar(imagem)
    
    # Aplicar Canny
    print("\n--- Canny ---")
    canny = Canny(sigma=sigma_canny, threshold_low=threshold_low, threshold_high=threshold_high)
    bordas_canny = canny.aplicar(imagem)
    
    print("\n" + "="*60)
    print("Diferenças principais:")
    print("- Marr-Hildreth: usa 2ª derivada (LoG), cruzamentos por zero")
    print("- Canny: usa 1ª derivada (gradiente), supressão não-máxima + histerese")
    print("- Canny geralmente produz bordas mais finas e contínuas")
    print("="*60 + "\n")
    
    return bordas_marr, bordas_canny


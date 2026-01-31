"""
Descritores de Fronteira: Cadeia de Freeman

Autor: [Seu Nome]
Data: Janeiro/2026

Referências:
- Freeman, H. (1961). On the encoding of arbitrary geometric configurations
- Aula 14 - Representação e Descrição (Prof. Matheus Raffael Simon)
"""

import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CadeiaFreeman:
    """
    Código da Cadeia de Freeman (8 direções)
    
    Representa fronteira como sequência de segmentos direcionais
    
    Direções (8-conectividade):
        3  2  1
        4  *  0
        5  6  7
        
    Onde:
    0 = Leste (→)      4 = Oeste (←)
    1 = Nordeste (↗)   5 = Sudoeste (↙)
    2 = Norte (↑)      6 = Sul (↓)
    3 = Noroeste (↖)   7 = Sudeste (↘)
    
    Primeira Diferença:
    - Torna o código invariante à rotação
    - Conta mudanças de direção entre segmentos adjacentes
    
    Referência: Slides 6-10, Aula 14
    """
    
    def __init__(self, conectividade=8):
        """
        Inicializa o extrator de Cadeia de Freeman
        
        Args:
            conectividade (int): 4 ou 8 conectividade
        """
        self.conectividade = conectividade
        
        # Direções para 8-conectividade
        # [dy, dx] para cada direção
        self.direcoes_8 = {
            0: (0, 1),    # Leste
            1: (-1, 1),   # Nordeste
            2: (-1, 0),   # Norte
            3: (-1, -1),  # Noroeste
            4: (0, -1),   # Oeste
            5: (1, -1),   # Sudoeste
            6: (1, 0),    # Sul
            7: (1, 1)     # Sudeste
        }
        
    def encontrar_ponto_inicial(self, imagem_binaria):
        """
        Encontra o ponto inicial do contorno
        
        Ponto inicial: pixel mais alto e mais à esquerda
        
        Args:
            imagem_binaria (numpy.ndarray): Imagem binária (0 ou 255)
            
        Returns:
            tuple: (linha, coluna) do ponto inicial, ou None se não encontrar
            
        Referência: Slide 4, Aula 14
        """
        # Normalizar para 0 e 1
        img_bin = (imagem_binaria > 0).astype(int)
        
        # Procurar de cima para baixo, esquerda para direita
        altura, largura = img_bin.shape
        for i in range(altura):
            for j in range(largura):
                if img_bin[i, j] == 1:
                    return (i, j)
        
        return None
    
    def obter_vizinhos_8(self, ponto):
        """
        Retorna os 8 vizinhos de um ponto em ordem horária
        
        Args:
            ponto (tuple): (linha, coluna)
            
        Returns:
            list: Lista de tuplas (linha, coluna) dos vizinhos
        """
        i, j = ponto
        vizinhos = []
        
        for direcao in range(8):
            dy, dx = self.direcoes_8[direcao]
            vizinhos.append((i + dy, j + dx))
        
        return vizinhos
    
    def seguir_contorno(self, imagem_binaria, ponto_inicial):
        """
        Segue o contorno a partir do ponto inicial
        
        Algoritmo do Seguidor de Fronteira:
        1. b0 = ponto inicial, c0 = vizinho oeste
        2. Examinar vizinhança-8 em sentido horário a partir de c0
        3. b1 = primeiro vizinho 1 encontrado
        4. Repetir até retornar a b0
        
        Args:
            imagem_binaria (numpy.ndarray): Imagem binária
            ponto_inicial (tuple): (linha, coluna) do ponto inicial
            
        Returns:
            list: Lista de pontos do contorno [(i0,j0), (i1,j1), ...]
            
        Referência: Slides 4-5, Aula 14
        """
        # Normalizar para 0 e 1
        img_bin = (imagem_binaria > 0).astype(int)
        altura, largura = img_bin.shape
        
        contorno = [ponto_inicial]
        
        # b0 = ponto inicial
        b_atual = ponto_inicial
        
        # c0 = vizinho a oeste (direção 4)
        dy, dx = self.direcoes_8[4]
        c_atual = (b_atual[0] + dy, b_atual[1] + dx)
        
        max_iteracoes = altura * largura  # Prevenir loops infinitos
        iteracao = 0
        
        while iteracao < max_iteracoes:
            iteracao += 1
            
            # Encontrar direção de c_atual em relação a b_atual
            dc_i = c_atual[0] - b_atual[0]
            dc_j = c_atual[1] - b_atual[1]
            
            # Encontrar qual direção isso representa
            direcao_c = None
            for d, (dy, dx) in self.direcoes_8.items():
                if dy == dc_i and dx == dc_j:
                    direcao_c = d
                    break
            
            if direcao_c is None:
                direcao_c = 0
            
            # Examinar vizinhos em sentido horário a partir de c_atual
            encontrado = False
            for offset in range(8):
                direcao = (direcao_c + offset) % 8
                dy, dx = self.direcoes_8[direcao]
                vizinho = (b_atual[0] + dy, b_atual[1] + dx)
                
                # Verificar limites
                if 0 <= vizinho[0] < altura and 0 <= vizinho[1] < largura:
                    if img_bin[vizinho[0], vizinho[1]] == 1:
                        # Encontrou próximo ponto do contorno
                        b_proximo = vizinho
                        
                        # c_proximo é o vizinho anterior ao b_proximo
                        direcao_anterior = (direcao - 1) % 8
                        dy_ant, dx_ant = self.direcoes_8[direcao_anterior]
                        c_proximo = (b_atual[0] + dy_ant, b_atual[1] + dx_ant)
                        
                        # Verificar se voltou ao início
                        if len(contorno) > 2 and b_proximo == ponto_inicial:
                            return contorno
                        
                        contorno.append(b_proximo)
                        b_atual = b_proximo
                        c_atual = c_proximo
                        encontrado = True
                        break
            
            if not encontrado:
                break
        
        return contorno
    
    def gerar_codigo(self, contorno):
        """
        Gera o código da cadeia de Freeman a partir do contorno
        
        Args:
            contorno (list): Lista de pontos [(i0,j0), (i1,j1), ...]
            
        Returns:
            list: Código da cadeia (lista de direções 0-7)
            
        Referência: Slide 7, Aula 14
        """
        if len(contorno) < 2:
            return []
        
        codigo = []
        
        for k in range(len(contorno) - 1):
            p_atual = contorno[k]
            p_proximo = contorno[k + 1]
            
            # Calcular diferença
            di = p_proximo[0] - p_atual[0]
            dj = p_proximo[1] - p_atual[1]
            
            # Encontrar direção correspondente
            for direcao, (dy, dx) in self.direcoes_8.items():
                if dy == di and dx == dj:
                    codigo.append(direcao)
                    break
        
        return codigo
    
    def normalizar_codigo(self, codigo):
        """
        Normaliza o código para obter o menor número inteiro
        
        Torna o código invariante ao ponto de partida
        
        Args:
            codigo (list): Código da cadeia
            
        Returns:
            list: Código normalizado
            
        Referência: Slide 7, Aula 14
        """
        if not codigo:
            return codigo
        
        # Converter para string para comparação
        codigo_str = ''.join(map(str, codigo))
        
        menor = codigo_str
        for i in range(1, len(codigo)):
            rotacao = codigo_str[i:] + codigo_str[:i]
            if rotacao < menor:
                menor = rotacao
        
        return [int(d) for d in menor]
    
    def primeira_diferenca(self, codigo):
        """
        Calcula a primeira diferença do código
        
        Torna o código invariante à rotação
        
        Primeira diferença = número de mudanças de direção (sentido horário)
        entre segmentos adjacentes
        
        Args:
            codigo (list): Código da cadeia
            
        Returns:
            list: Primeira diferença
            
        Referência: Slide 9, Aula 14
        """
        if len(codigo) < 2:
            return []
        
        primeira_dif = []
        
        for i in range(len(codigo)):
            # Próximo elemento (circular)
            proximo = (i + 1) % len(codigo)
            
            # Diferença entre direções (módulo 8)
            dif = (codigo[proximo] - codigo[i]) % 8
            primeira_dif.append(dif)
        
        return primeira_dif
    
    def aplicar(self, imagem_binaria):
        """
        Aplica extração completa da Cadeia de Freeman (Questão 4)
        
        Args:
            imagem_binaria (numpy.ndarray): Imagem binária
            
        Returns:
            dict: Dicionário com resultados
                - 'contorno': lista de pontos
                - 'codigo': código da cadeia
                - 'codigo_normalizado': código normalizado
                - 'primeira_diferenca': primeira diferença
        """
        print("\n" + "="*60)
        print("CADEIA DE FREEMAN")
        print("="*60)
        
        # 1. Encontrar ponto inicial
        ponto_inicial = self.encontrar_ponto_inicial(imagem_binaria)
        
        if ponto_inicial is None:
            print("ERRO: Nenhum objeto encontrado na imagem")
            return None
        
        print(f"Ponto inicial: {ponto_inicial}")
        
        # 2. Seguir contorno
        contorno = self.seguir_contorno(imagem_binaria, ponto_inicial)
        print(f"Contorno extraído: {len(contorno)} pontos")
        
        # 3. Gerar código
        codigo = self.gerar_codigo(contorno)
        print(f"Código da cadeia: {''.join(map(str, codigo))}")
        print(f"Comprimento: {len(codigo)}")
        
        # 4. Normalizar código
        codigo_normalizado = self.normalizar_codigo(codigo)
        print(f"Código normalizado: {''.join(map(str, codigo_normalizado))}")
        
        # 5. Calcular primeira diferença
        primeira_dif = self.primeira_diferenca(codigo)
        print(f"Primeira diferença: {''.join(map(str, primeira_dif))}")
        
        print("="*60 + "\n")
        
        return {
            'contorno': contorno,
            'codigo': codigo,
            'codigo_normalizado': codigo_normalizado,
            'primeira_diferenca': primeira_dif
        }
    
    def visualizar_contorno(self, imagem, contorno):
        """
        Cria imagem com contorno destacado
        
        Args:
            imagem (numpy.ndarray): Imagem original
            contorno (list): Lista de pontos do contorno
            
        Returns:
            numpy.ndarray: Imagem com contorno em branco
        """
        resultado = imagem.copy()
        
        for ponto in contorno:
            i, j = ponto
            if 0 <= i < resultado.shape[0] and 0 <= j < resultado.shape[1]:
                resultado[i, j] = 255
        
        return resultado


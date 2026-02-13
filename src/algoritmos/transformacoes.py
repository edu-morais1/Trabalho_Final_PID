import numpy as np


class SegmentacaoCustomizada:
    """
    Segmentação customizada por faixas de intensidade (Questão 6)
    
    Transforma intensidades conforme tabela:
    [0-50]     → 25
    [51-100]   → 75
    [101-150]  → 125
    [151-200]  → 175
    [201-255]  → 255
    
    Este tipo de transformação é conhecido como posterização
    ou quantização uniforme de níveis de cinza
    """
    
    def __init__(self):
        """
        Inicializa com a tabela de transformação padrão
        """
        # Tabela: (min, max, novo_valor)
        self.tabela = [
            (0, 50, 25),
            (51, 100, 75),
            (101, 150, 125),
            (151, 200, 175),
            (201, 255, 255)
        ]
    
    def aplicar(self, imagem):
        """
        Aplica segmentação customizada (Questão 6)
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            
        Returns:
            numpy.ndarray: Imagem segmentada
        """
        print("\n" + "="*60)
        print("SEGMENTAÇÃO CUSTOMIZADA")
        print("="*60)
        print("Tabela de transformação:")
        print("  [0-50]     → 25")
        print("  [51-100]   → 75")
        print("  [101-150]  → 125")
        print("  [151-200]  → 175")
        print("  [201-255]  → 255")
        print("="*60 + "\n")
        
        # Criar cópia da imagem
        resultado = imagem.copy()
        
        # Aplicar transformação para cada faixa
        for min_val, max_val, novo_val in self.tabela:
            # Criar máscara para pixels na faixa
            mascara = (resultado >= min_val) & (resultado <= max_val)
            
            # Contar pixels transformados
            num_pixels = np.sum(mascara)
            
            # Aplicar transformação
            resultado[mascara] = novo_val
            
            print(f"Faixa [{min_val:3d}-{max_val:3d}] → {novo_val:3d}: {num_pixels:6d} pixels")
        
        print("\nSegmentação concluída\n")
        
        return resultado
    
    def aplicar_customizado(self, imagem, tabela_custom):
        """
        Aplica segmentação com tabela customizada
        
        Args:
            imagem (numpy.ndarray): Imagem em escala de cinza
            tabela_custom (list): Lista de tuplas (min, max, novo_valor)
            
        Returns:
            numpy.ndarray: Imagem segmentada
        """
        resultado = imagem.copy()
        
        for min_val, max_val, novo_val in tabela_custom:
            mascara = (resultado >= min_val) & (resultado <= max_val)
            resultado[mascara] = novo_val
        
        return resultado
    
    def analisar_distribuicao(self, imagem_original, imagem_segmentada):
        """
        Analisa a distribuição de intensidades antes e depois
        
        Args:
            imagem_original (numpy.ndarray): Imagem original
            imagem_segmentada (numpy.ndarray): Imagem segmentada
            
        Returns:
            dict: Estatísticas
        """
        stats = {
            'original': {
                'min': imagem_original.min(),
                'max': imagem_original.max(),
                'media': imagem_original.mean(),
                'desvio': imagem_original.std(),
                'niveis_unicos': len(np.unique(imagem_original))
            },
            'segmentada': {
                'min': imagem_segmentada.min(),
                'max': imagem_segmentada.max(),
                'media': imagem_segmentada.mean(),
                'desvio': imagem_segmentada.std(),
                'niveis_unicos': len(np.unique(imagem_segmentada))
            }
        }
        
        print("\n" + "="*60)
        print("ANÁLISE DA SEGMENTAÇÃO")
        print("="*60)
        print("\nImagem Original:")
        print(f"  Mín: {stats['original']['min']:.2f}")
        print(f"  Máx: {stats['original']['max']:.2f}")
        print(f"  Média: {stats['original']['media']:.2f}")
        print(f"  Desvio: {stats['original']['desvio']:.2f}")
        print(f"  Níveis únicos: {stats['original']['niveis_unicos']}")
        
        print("\nImagem Segmentada:")
        print(f"  Mín: {stats['segmentada']['min']:.2f}")
        print(f"  Máx: {stats['segmentada']['max']:.2f}")
        print(f"  Média: {stats['segmentada']['media']:.2f}")
        print(f"  Desvio: {stats['segmentada']['desvio']:.2f}")
        print(f"  Níveis únicos: {stats['segmentada']['niveis_unicos']}")
        print("="*60 + "\n")
        
        return stats


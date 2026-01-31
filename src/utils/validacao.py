"""
Funções de validação

Autor: [Seu Nome]
Data: Janeiro/2026
"""

import numpy as np


def validar_imagem_greyscale(imagem):
    """
    Valida se a imagem está em escala de cinza
    
    Args:
        imagem (numpy.ndarray): Imagem a validar
        
    Returns:
        bool: True se válida
        
    Raises:
        ValueError: Se imagem inválida
    """
    if imagem is None:
        raise ValueError("Imagem não pode ser None")
    
    if not isinstance(imagem, np.ndarray):
        raise ValueError("Imagem deve ser um numpy array")
    
    if len(imagem.shape) != 2:
        raise ValueError("Imagem deve estar em escala de cinza (2D)")
    
    return True


def validar_imagem_binaria(imagem):
    """
    Valida se a imagem é binária (apenas 0 e 1)
    
    Args:
        imagem (numpy.ndarray): Imagem a validar
        
    Returns:
        bool: True se válida
    """
    valores_unicos = np.unique(imagem)
    return len(valores_unicos) <= 2 and all(v in [0, 1, 0.0, 1.0, 255] for v in valores_unicos)


def validar_parametros_numericos(valor, minimo=None, maximo=None, nome="parâmetro"):
    """
    Valida parâmetros numéricos
    
    Args:
        valor: Valor a validar
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
        nome: Nome do parâmetro (para mensagem de erro)
        
    Returns:
        bool: True se válido
        
    Raises:
        ValueError: Se inválido
    """
    if not isinstance(valor, (int, float)):
        raise ValueError(f"{nome} deve ser numérico")
    
    if minimo is not None and valor < minimo:
        raise ValueError(f"{nome} deve ser >= {minimo}")
    
    if maximo is not None and valor > maximo:
        raise ValueError(f"{nome} deve ser <= {maximo}")
    
    return True


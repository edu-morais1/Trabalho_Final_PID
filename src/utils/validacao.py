import numpy as np


def validar_imagem_greyscale(imagem):
    if imagem is None:
        raise ValueError("Imagem não pode ser None")
    
    if not isinstance(imagem, np.ndarray):
        raise ValueError("Imagem deve ser um numpy array")
    
    if len(imagem.shape) != 2:
        raise ValueError("Imagem deve estar em escala de cinza (2D)")
    
    return True


def validar_imagem_binaria(imagem):
    valores_unicos = np.unique(imagem)
    return len(valores_unicos) <= 2 and all(v in [0, 1, 0.0, 1.0, 255] for v in valores_unicos)


def validar_parametros_numericos(valor, minimo=None, maximo=None, nome="parâmetro"):
    if not isinstance(valor, (int, float)):
        raise ValueError(f"{nome} deve ser numérico")
    
    if minimo is not None and valor < minimo:
        raise ValueError(f"{nome} deve ser >= {minimo}")
    
    if maximo is not None and valor > maximo:
        raise ValueError(f"{nome} deve ser <= {maximo}")
    
    return True


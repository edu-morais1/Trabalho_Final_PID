import numpy as np
from PIL import Image


def carregar_imagem(caminho):
    img = Image.open(caminho)
    
    # Converter para escala de cinza se necessário
    if img.mode != 'L':
        img = img.convert('L')
    
    return np.array(img, dtype=np.float64)


def salvar_imagem(imagem, caminho):
    # Normalizar para 0-255 se necessário
    if imagem.max() <= 1.0:
        imagem = imagem * 255
    
    imagem = np.clip(imagem, 0, 255).astype(np.uint8)
    img = Image.fromarray(imagem)
    img.save(caminho)


def normalizar_imagem(imagem):
    img_min = imagem.min()
    img_max = imagem.max()
    
    if img_max == img_min:
        return np.zeros_like(imagem)
    
    return ((imagem - img_min) / (img_max - img_min) * 255).astype(np.uint8)


def adicionar_padding(imagem, pad_size, valor=0):
    return np.pad(imagem, pad_size, mode='constant', constant_values=valor)


def criar_mascara_gaussiana(tamanho, sigma):
    # Garantir que o tamanho seja ímpar
    if tamanho % 2 == 0:
        tamanho += 1
    
    centro = tamanho // 2
    mascara = np.zeros((tamanho, tamanho))
    
    # Calcular valores da gaussiana
    for i in range(tamanho):
        for j in range(tamanho):
            x = i - centro
            y = j - centro
            mascara[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # Normalizar para que a soma seja 1
    return mascara / mascara.sum()


def calcular_gradiente(imagem, metodo='sobel'):
    if metodo == 'sobel':
        # Máscaras de Sobel
        gx_mask = np.array([[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]])
        gy_mask = np.array([[-1, -2, -1],
                           [0, 0, 0],
                           [1, 2, 1]])
    
    elif metodo == 'prewitt':
        # Máscaras de Prewitt
        gx_mask = np.array([[-1, 0, 1],
                           [-1, 0, 1],
                           [-1, 0, 1]])
        gy_mask = np.array([[-1, -1, -1],
                           [0, 0, 0],
                           [1, 1, 1]])
    
    elif metodo == 'roberts':
        # Máscaras de Roberts
        gx_mask = np.array([[1, 0],
                           [0, -1]])
        gy_mask = np.array([[0, 1],
                           [-1, 0]])
    
    # Aplicar convolução
    gx = convolucao(imagem, gx_mask)
    gy = convolucao(imagem, gy_mask)
    
    # Calcular magnitude e direção
    magnitude = np.sqrt(gx**2 + gy**2)
    direcao = np.arctan2(gy, gx)
    
    return magnitude, direcao


def convolucao(imagem, mascara):
    altura_img, largura_img = imagem.shape
    altura_mask, largura_mask = mascara.shape
    
    # Calcular padding necessário
    pad_h = altura_mask // 2
    pad_w = largura_mask // 2
    
    # Adicionar padding
    img_padded = adicionar_padding(imagem, ((pad_h, pad_h), (pad_w, pad_w)))
    
    # Criar imagem de saída
    resultado = np.zeros_like(imagem)
    
    # Aplicar convolução
    for i in range(altura_img):
        for j in range(largura_img):
            # Extrair região
            regiao = img_padded[i:i+altura_mask, j:j+largura_mask]
            # Aplicar máscara (convolução = rotação 180° + correlação)
            resultado[i, j] = np.sum(regiao * np.flip(mascara))
    
    return resultado


def correlacao(imagem, mascara):
    altura_img, largura_img = imagem.shape
    altura_mask, largura_mask = mascara.shape
    
    pad_h = altura_mask // 2
    pad_w = largura_mask // 2
    
    img_padded = adicionar_padding(imagem, ((pad_h, pad_h), (pad_w, pad_w)))
    resultado = np.zeros_like(imagem)
    
    for i in range(altura_img):
        for j in range(largura_img):
            regiao = img_padded[i:i+altura_mask, j:j+largura_mask]
            resultado[i, j] = np.sum(regiao * mascara)
    
    return resultado


def criar_histograma(imagem):
    histograma = np.zeros(256, dtype=int)
    
    imagem_int = imagem.astype(int)
    
    for valor in range(256):
        histograma[valor] = np.sum(imagem_int == valor)
    
    return histograma

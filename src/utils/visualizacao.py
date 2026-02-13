import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


def array_para_photoimage(imagem_array):
    # Normalizar se necessário
    if imagem_array.max() > 255 or imagem_array.min() < 0:
        imagem_array = np.clip(imagem_array, 0, 255)
    
    imagem_array = imagem_array.astype(np.uint8)
    
    # Converter para PIL Image
    img_pil = Image.fromarray(imagem_array)
    
    # Converter para PhotoImage
    return ImageTk.PhotoImage(img_pil)


def redimensionar_imagem(imagem, max_largura=400, max_altura=400):
    altura, largura = imagem.shape
    
    # Calcular proporção
    proporcao = min(max_largura/largura, max_altura/altura)
    
    if proporcao >= 1:
        return imagem
    
    nova_largura = int(largura * proporcao)
    nova_altura = int(altura * proporcao)
    
    # Usar PIL para redimensionar
    img_pil = Image.fromarray(imagem.astype(np.uint8))
    img_redimensionada = img_pil.resize((nova_largura, nova_altura), Image.LANCZOS)
    
    return np.array(img_redimensionada)


def plotar_histograma(imagem, titulo="Histograma"):
    plt.figure(figsize=(10, 4))
    plt.hist(imagem.ravel(), bins=256, range=(0, 256), color='gray')
    plt.title(titulo)
    plt.xlabel('Intensidade')
    plt.ylabel('Frequência')
    plt.grid(True, alpha=0.3)
    plt.show()


def plotar_comparacao(img1, img2, titulo1="Original", titulo2="Processada"):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    axes[0].imshow(img1, cmap='gray')
    axes[0].set_title(titulo1)
    axes[0].axis('off')
    
    axes[1].imshow(img2, cmap='gray')
    axes[1].set_title(titulo2)
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()


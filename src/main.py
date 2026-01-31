"""
Trabalho de Processamento de Imagens Digitais

Aluno: [Seu Nome]
Curso: Ciência da Computação - UNIOESTE
Professor: [Nome do Professor]
Disciplina: Processamento de Imagens Digitais
Data: Fevereiro/2026

Questões implementadas:
1. Detectores: Marr-Hildreth, Canny, Otsu, Watershed
2. Comparativo: Marr-Hildreth vs Canny
3. Contagem de objetos com Otsu
4. Cadeia de Freeman
5. Filtros Box (2x2, 3x3, 5x5, 7x7, 11x11, 21x21)
6. Segmentação customizada

Referências:
- GONZALEZ, R. C., WOODS, R. E. Processamento Digital de Imagens
- Material de aula - Prof. Matheus Raffael Simon - UNIOESTE
- Marr, D., Hildreth, E. (1980). Theory of Edge Detection
- Canny, J. (1986). A Computational Approach to Edge Detection
- Otsu, N. (1979). A threshold selection method from gray-level histograms

Bibliotecas utilizadas:
- NumPy: operações com arrays (permitido)
- Pillow: leitura/escrita de imagens (permitido)
- Tkinter: interface gráfica (permitido)
- Matplotlib: visualização (permitido)
- SciPy: apenas para funções auxiliares básicas (não para algoritmos principais)

IMPORTANTE:
Todos os algoritmos principais foram implementados manualmente,
sem uso de funções prontas de bibliotecas.
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interface import JanelaPrincipal

# Variável solicitada no enunciado (Questão 3)
gol = 0


def main():
    """
    Função principal do programa
    """
    print("="*60)
    print("TRABALHO DE PROCESSAMENTO DE IMAGENS DIGITAIS")
    print("="*60)
    print("Aluno: [Seu Nome]")
    print("UNIOESTE - Ciência da Computação")
    print("="*60)
    print()
    
    # Criar e executar aplicação
    app = JanelaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()


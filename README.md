# Trabalho Final - Processamento de Imagens Digitais

**Aluno:** Eduardo Morais  
**Curso:** Ciência da Computação - UNIOESTE  
**Disciplina:** Processamento de Imagens Digitais  
**Professor:** [Nome do Professor]  
**Data:** Fevereiro/2026

## 📋 Descrição

Sistema completo de processamento de imagens digitais implementando algoritmos fundamentais da área.

## ✨ Funcionalidades

### Questão 1: Detectores de Borda
- ✅ **Marr-Hildreth**: Detector baseado em LoG (Laplaciano da Gaussiana)
- ✅ **Canny**: Detector multi-estágio com supressão não-máxima
- ✅ **Otsu**: Limiarização automática por variância entre classes
- ✅ **Watershed**: Segmentação por bacias hidrográficas

### Questão 2: Comparativo
- ✅ Análise comparativa entre Marr-Hildreth e Canny
- ✅ Visualização lado a lado dos resultados

### Questão 3: Contagem de Objetos
- ✅ Aplicação do método de Otsu
- ✅ Rotulação de componentes conectados (8-conectividade)
- ✅ Contagem automática de objetos

### Questão 4: Cadeia de Freeman
- ✅ Extração de contorno com seguidor de fronteira
- ✅ Código de 8 direções
- ✅ Primeira diferença (invariante à rotação)

### Questão 5: Filtros Box
- ✅ Implementação de filtros Box em múltiplos tamanhos (2x2, 3x3, 5x5, 7x7, 11x11, 21x21)
- ✅ Suporte para imagens de diferentes dimensões
- ✅ Comparação visual entre filtros

### Questão 6: Segmentação Customizada
- ✅ Posterização em 5 níveis conforme especificação
- ✅ Análise estatística antes/depois

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/edu-morais1/Trabalho_Final_PID.git
cd Trabalho_Final_PID
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

Execute o programa:
```bash
python src/main.py
```

### Interface Gráfica

1. **Carregar Imagem**: Clique em "📁 Carregar Imagem" ou use `Ctrl+O`
2. **Selecionar Algoritmo**: Use o menu "Questões" para escolher o algoritmo
3. **Ajustar Parâmetros**: Use os controles no painel de parâmetros (quando disponível)
4. **Salvar Resultado**: Clique em "💾 Salvar Resultado" ou use `Ctrl+S`

## 📁 Estrutura do Projeto

```
trabalho-processamento-imagens/
├── src/
│   ├── main.py                      # Arquivo principal
│   ├── algoritmos/                  # Implementação dos algoritmos
│   │   ├── detectores_borda.py     # Marr-Hildreth e Canny
│   │   ├── segmentacao.py          # Otsu e Watershed
│   │   ├── descritores.py          # Cadeia de Freeman
│   │   ├── filtros.py              # Filtro Box
│   │   └── transformacoes.py       # Segmentação customizada
│   ├── utils/                       # Funções auxiliares
│   │   ├── processamento.py        # Processamento de imagens
│   │   ├── visualizacao.py         # Funções de visualização
│   │   └── validacao.py            # Validações
│   └── interface/                   # Interface gráfica
│       ├── janela_principal.py     # Janela principal
│       └── componentes.py          # Componentes reutilizáveis
├── images/                          # Imagens de teste
│   ├── input/                      # Imagens de entrada
│   ├── output/                     # Resultados salvos
│   └── treinamento/                # Imagens para Q3
├── docs/                            # Documentação
├── tests/                           # Testes
├── requirements.txt                 # Dependências
└── README.md                        # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **NumPy**: Operações com arrays e matrizes
- **Pillow (PIL)**: Leitura e escrita de imagens
- **Tkinter**: Interface gráfica
- **Matplotlib**: Visualização de gráficos
- **SciPy**: Funções auxiliares básicas

## 📖 Algoritmos Implementados

### Marr-Hildreth
Utiliza o Laplaciano da Gaussiana (LoG) para detectar bordas através de cruzamentos por zero. A máscara LoG é calculada pela fórmula:

∇²G(x,y) = [(x²+y²-2σ⁴)/σ⁴] × e^(-(x²+y²)/(2σ²))

### Canny
Detector multi-estágio que garante:
- Baixa taxa de erros
- Boa localização das bordas
- Resposta única por borda

Passos: Suavização → Gradiente → Supressão não-máxima → Histerese dupla

### Otsu
Método de limiarização que maximiza a variância entre classes (foreground/background):

σ²(t) = w_b(t) × w_f(t) × [m_b(t) - m_f(t)]²

### Watershed
Segmentação baseada em conceitos de bacias hidrográficas, tratando a imagem como uma topografia 3D.

### Cadeia de Freeman
Representa contornos como sequências de segmentos direcionais em 8 direções (0-7).

### Filtro Box
Filtro passa-baixa com pesos uniformes para suavização de imagens.

## 📚 Referências

1. GONZALEZ, R. C., WOODS, R. E. **Processamento Digital de Imagens**. 3ª ed. Pearson, 2010.
2. Material de aula - Prof. Matheus Raffael Simon - UNIOESTE
3. Marr, D., Hildreth, E. (1980). **Theory of Edge Detection**. Proceedings of the Royal Society of London.
4. Canny, J. (1986). **A Computational Approach to Edge Detection**. IEEE Transactions on Pattern Analysis and Machine Intelligence.
5. Otsu, N. (1979). **A threshold selection method from gray-level histograms**. IEEE Transactions on Systems, Man, and Cybernetics.

## 📝 Observações Importantes

- ✅ Todos os algoritmos foram **implementados manualmente**
- ✅ Não foram utilizadas funções prontas de bibliotecas para os algoritmos principais
- ✅ O código está documentado com referências teóricas
- ✅ A implementação segue as especificações do material de aula
- ✅ Interface gráfica intuitiva com console integrado
- ✅ Suporte para múltiplos formatos de imagem (PNG, JPG, BMP, TIFF)

## 🎯 Detalhes de Implementação

### Questão 1
Cada detector foi implementado seguindo rigorosamente a teoria:
- **Marr-Hildreth**: Implementação manual do LoG e detecção de cruzamentos por zero
- **Canny**: Implementação completa incluindo supressão não-máxima e histerese
- **Otsu**: Algoritmo iterativo para encontrar threshold ótimo
- **Watershed**: Versão simplificada baseada em gradiente morfológico

### Questão 2
Comparação visual e quantitativa entre Marr-Hildreth e Canny, destacando:
- Diferenças na detecção (2ª vs 1ª derivada)
- Qualidade das bordas detectadas
- Sensibilidade a ruído

### Questão 3
Sistema completo de contagem usando:
- Otsu para binarização automática
- Flood fill para rotulação de componentes
- 8-conectividade para detecção precisa

### Questão 4
Implementação completa do algoritmo de seguimento de contorno com:
- Detecção do ponto inicial (mais alto e à esquerda)
- Vizinhança-8 em sentido horário
- Normalização do código
- Primeira diferença para invariância rotacional

### Questão 5
Filtros Box implementados manualmente com:
- Convolução manual (sem funções prontas)
- Suporte para múltiplos tamanhos
- Tratamento adequado de padding
- Otimização para imagens grandes

### Questão 6
Segmentação por posterização com:
- Tabela de transformação conforme especificação
- Análise estatística completa
- Visualização antes/depois

## 🐛 Solução de Problemas

### Erro ao carregar imagem
- Verifique se a imagem está em formato suportado (PNG, JPG, BMP, TIFF)
- Certifique-se de que o caminho do arquivo está correto

### Interface não abre
- Verifique se o Tkinter está instalado: `python -m tkinter`
- No Linux, pode ser necessário: `sudo apt-get install python3-tk`

### Processamento lento
- Para imagens grandes (>2000x2000), os algoritmos podem demorar
- Considere redimensionar a imagem antes do processamento
- Filtros Box maiores (11x11, 21x21) são mais lentos

## 📊 Exemplos de Uso

### Via Interface Gráfica
1. Execute `python src/main.py`
2. Carregue uma imagem
3. Selecione o algoritmo no menu
4. Visualize e salve o resultado

### Via Código (para testes)
```python
from src.algoritmos import Canny, Otsu
from src.utils import carregar_imagem, salvar_imagem

# Carregar imagem
img = carregar_imagem('images/input/teste.png')

# Aplicar Canny
canny = Canny(sigma=1.4, threshold_low=0.04, threshold_high=0.10)
resultado = canny.aplicar(img)

# Salvar resultado
salvar_imagem(resultado, 'images/output/resultado_canny.png')
```

## 🔄 Atualizações Futuras

Possíveis melhorias para versões futuras:
- [ ] Implementação de mais detectores (Sobel, Prewitt, Roberts)
- [ ] Suporte para imagens coloridas (RGB)
- [ ] Processamento em batch de múltiplas imagens
- [ ] Exportação de relatórios em PDF
- [ ] Modo de comparação lado a lado de múltiplos algoritmos
- [ ] Ajuste dinâmico de parâmetros com visualização em tempo real

## 👨‍💻 Autor

**Eduardo Morais**  
Ciência da Computação - UNIOESTE  
GitHub: [@edu-morais1](https://github.com/edu-morais1)

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto:
- GitHub Issues: [Criar Issue](https://github.com/edu-morais1/Trabalho_Final_PID/issues)
- Email: [seu-email@example.com]

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina de Processamento de Imagens Digitais da UNIOESTE.

O código é disponibilizado para referência educacional. Para uso em outros contextos, favor contactar o autor.

---

⭐ Se este projeto foi útil, considere dar uma estrela no repositório!

**Desenvolvido com 💙 por Eduardo Morais**

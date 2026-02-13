import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interface import JanelaPrincipal

def main():
  
    app = JanelaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()


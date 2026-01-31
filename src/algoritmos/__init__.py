"""
Módulo de algoritmos de processamento de imagens
"""

from .detectores_borda import MarrHildreth, Canny, comparar_detectores
from .segmentacao import Otsu, Watershed, contar_objetos
from .descritores import CadeiaFreeman
from .filtros import FiltroBox
from .transformacoes import SegmentacaoCustomizada

__all__ = [
    'MarrHildreth',
    'Canny',
    'comparar_detectores',
    'Otsu',
    'Watershed',
    'contar_objetos',
    'CadeiaFreeman',
    'FiltroBox',
    'SegmentacaoCustomizada'
]


import random
import math

def generar_nros_aleatorios(n):
    """Genera una lista de n números aleatorios uniformes entre 0 y 1."""
    return [random.random() for _ in range(n)]

def transformar_uniforme(serie_uniforme, a, b):
    return [a + rnd * (b - a) for rnd in serie_uniforme]

def transformar_exponencial(serie_uniforme, lambd):
    return [-(1 / lambd) * math.log(1 - rnd) for rnd in serie_uniforme]

def transformar_normal(serie_uniforme, media, desv):
    normales = []
    n = len(serie_uniforme)

    # Procesar de dos en dos los números de la serie
    for i in range(0, n - 1, 2):
        r1 = serie_uniforme[i]
        r2 = serie_uniforme[i + 1]

        z1 = math.sqrt(-2 * math.log(1 - r1)) * math.cos(2 * math.pi * r2)
        z2 = math.sqrt(-2 * math.log(1 - r1)) * math.sin(2 * math.pi * r2)

        normales.append(z1 * desv + media)
        normales.append(z2 * desv + media)

    return normales

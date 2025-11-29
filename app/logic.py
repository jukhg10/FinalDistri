import math
import random

def es_primo(n: int) -> bool:
    """
    Test de primalidad 'Puro' usando división hasta la raíz cuadrada.
    Sin optimizaciones de saltar pares.
    """
    if n <= 1: return False
    
    # Calculamos la raíz cuadrada entera
    raiz = int(math.isqrt(n))
    
    for i in range(2, raiz + 1):
        if n % i == 0:
            return False 
            
    return True

def generar_candidato_impar(digitos: int) -> int:
    """Genera un número aleatorio de N dígitos"""
    inicio = 10**(digitos - 1)
    fin = (10**digitos) - 1
    numero = random.randint(inicio, fin)
    return numero
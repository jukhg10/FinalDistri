import math
import random

def es_primo(n: int) -> bool:
    """
    Test de primalidad determinista por división de prueba.
    Garantiza 100% de certeza.
    """
    if n <= 1: return False
    if n == 2: return True
    if n % 2 == 0: return False
    
    # Optimizacion: Solo verificar impares hasta la raíz cuadrada
    limite = int(math.isqrt(n)) + 1
    for i in range(3, limite, 2):
        if n % i == 0:
            return False
    return True

def generar_candidato_impar(digitos: int) -> int:
    """Genera un número aleatorio impar de N dígitos"""
    inicio = 10**(digitos - 1)
    fin = (10**digitos) - 1
    numero = random.randint(inicio, fin)
    # Asegurar que sea impar para ahorrar tiempo
    if numero % 2 == 0:
        numero += 1
    return numero
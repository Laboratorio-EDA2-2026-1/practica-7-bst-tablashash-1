# practica_simple_hash_crack.py
# Versión simple para la práctica: conteo de frecuencias, búsqueda tosca de A, tablas y propuesta de mapeo

from math import floor
import random
import string

# Declaramos las variables globales
M = 31
A_OBJ = 0.6180339887498948
ASCII_MIN = 32
ASCII_MAX = 126

def mult_index(k, A, M):
    frac = (k * A) % 1.0
    return int(floor(M * frac)) + ASCII_MIN

def mod_index(k, M):
    return (k % M) + ASCII_MIN

def generar_tabla_simulada(seed=1):
    random.seed(seed)
    mapping = {}
    choice = {}
    for k in range(ASCII_MIN, ASCII_MAX + 1):
        if random.choice([True, False]):
            choice[k] = 'A'
            mapping[k] = mult_index(k, A_OBJ, M)
        else:
            choice[k] = 'M'
            mapping[k] = mod_index(k, M)
    return choice, mapping

def cifrar(texto, mapping):
    out = []
    for ch in texto:
        k = ord(ch)
        out.append(chr(mapping.get(k, ord(ch))))
    return ''.join(out)

def contar_freq(texto):
    freq = {}
    for ch in texto:
        k = ord(ch)
        freq[k] = freq.get(k, 0) + 1
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)

def buscar_A_tosca(k_plain, ascii_cipher, M, start=0.5, stop=0.7, step=1e-4):
    objetivo_bin = ascii_cipher - ASCII_MIN
    candidatos = []
    a = start
    while a < stop:
        frac = (k_plain * a) % 1.0
        if int(frac * M) == objetivo_bin:
            candidatos.append(round(a, 8))
        a += step
    return sorted(set(candidatos))

def tabla_multiplicativa(A):
    return {k: mult_index(k, A, M) for k in range(ASCII_MIN, ASCII_MAX + 1)}

def tabla_modulo():
    return {k: mod_index(k, M) for k in range(ASCII_MIN, ASCII_MAX + 1)}

def proponer_mapeo(freq_cipher_desc, orden_plain):
    m = {}
    for i, (cipher_k, f) in enumerate(freq_cipher_desc):
        if i < len(orden_plain):
            m[cipher_k] = orden_plain[i]
        else:
            m[cipher_k] = '?'
    return m

# Filtra caracteres no alfabéticos (solo deja a-z)
def filtrar_minusculas(texto):
    resultado = []
    for ch in texto:
        if ch in string.ascii_lowercase:
            resultado.append(ch)
        else:
            resultado.append('?')  # o elimina si prefieres: no agregar nada
    return ''.join(resultado)

# main
if __name__ == "__main__":
    # --- Texto cifrado real proporcionado ---
    cifrado = "(/-.-4%(+28.%#+2/($(6(#(3(8%.-/2(+(/(6.("
    print("CIFRADO:", cifrado)
    print()

    # --- Fase 1: conteo de frecuencias ---
    freq = contar_freq(cifrado)
    print("Top frecuencias (char, ascii, freq):")
    for ch_ascii, f in freq[:12]:
        print(chr(ch_ascii), ch_ascii, f)
    print()

    # --- Fase 2: suposición del carácter más frecuente ---
    top_cipher_ascii = freq[0][0]
    print("Suposición: el char cifrado más frecuente", chr(top_cipher_ascii),
          "(", top_cipher_ascii, ") -> ' ' (espacio)")
    k_space = ord(' ')

    # --- Fase 3: búsqueda tosca de A ---
    cand = buscar_A_tosca(k_space, top_cipher_ascii, M,
                          start=0.55, stop=0.65, step=1e-5)
    print("Candidatos A (muestra):", cand[:10])
    print()

    # --- Fase 4: tabla y prueba ---
    if cand:
        A_guess = cand[0]
        tab_mult = tabla_multiplicativa(A_guess)
        print("Indice mult para 'A' (65) con A_guess:", tab_mult[65])
    else:
        print("No se encontró A en la búsqueda tosca (ajusta intervalo o suposición).")
    print()

    # --- Fase 5: propuesta de mapeo ---
    orden_esp = [' ', 'e', 'a', 'o', 's', 'r', 'n', 'i', 'd', 'l', 't', 'u']
    prop_map = proponer_mapeo(freq, orden_esp)

    print("Mapa propuesto (cifrado ascii -> supuesto claro):")
    for k, fv in freq[:12]:
        print(chr(k), k, "->", prop_map.get(k))
    print()

    # --- Fase 6: descifrado parcial ---
    parcial = ''.join(prop_map.get(ord(ch), '?') for ch in cifrado)
    parcial_filtrado = filtrar_minusculas(parcial)

    print("Descifrado parcial (solo minúsculas):")
    print(parcial_filtrado)

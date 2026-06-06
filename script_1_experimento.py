"""
SCRIPT 1 — Toma de datos
Métodos Estadísticos 20261 · Universidad de Antioquia

Muestra en pantalla:
  1. Generación del diccionario de búsqueda
  2. Cálculo de los 9 hashes (3 contraseñas × 3 algoritmos)
  3. Ejecución de las 9 corridas en orden aleatorizado
  4. Tabla de resultados final

Uso: python3 script_1_experimento.py
"""

import hashlib, random, string, time, os

# ── Colores ANSI ───────────────────────────────────────────────────────────────
R  = "\033[0m"       # reset
B  = "\033[1m"       # bold
CY = "\033[96m"      # cyan
GR = "\033[92m"      # green
YL = "\033[93m"      # yellow
BL = "\033[94m"      # blue
MG = "\033[95m"      # magenta
DIM = "\033[2m"      # dim

def sep(char="─", n=62, color=CY):
    print(color + char * n + R)

def titulo(texto):
    sep()
    print(B + CY + f"  {texto}" + R)
    sep()

# ── Configuración del experimento ──────────────────────────────────────────────

CONTRASENAS = {
    "B1 — Simple":   "luna",
    "B2 — Media":    "cielo7",
    "B3 — Compleja": "Sol#2024",
}

POSICIONES = {
    "B1 — Simple":   1_000,
    "B2 — Media":    10_000,
    "B3 — Compleja": 100_000,
}

# Orden aleatorizado (seed=42, dentro de cada bloque)
CORRIDAS = [
    (1,  "B1 — Simple",   "SHA-1",   "luna"),
    (2,  "B1 — Simple",   "MD5",     "luna"),
    (3,  "B1 — Simple",   "SHA-256", "luna"),
    (4,  "B2 — Media",    "SHA-256", "cielo7"),
    (5,  "B2 — Media",    "SHA-1",   "cielo7"),
    (6,  "B2 — Media",    "MD5",     "cielo7"),
    (7,  "B3 — Compleja", "SHA-1",   "Sol#2024"),
    (8,  "B3 — Compleja", "SHA-256", "Sol#2024"),
    (9,  "B3 — Compleja", "MD5",     "Sol#2024"),
]

WORDLIST = os.path.join(os.path.dirname(__file__), "wordlist_experimento.txt")

# ── Funciones ──────────────────────────────────────────────────────────────────

def calcular_hash(palabra, algoritmo):
    pw = palabra.encode()
    if algoritmo == "MD5":     return hashlib.md5(pw).hexdigest()
    if algoritmo == "SHA-1":   return hashlib.sha1(pw).hexdigest()
    if algoritmo == "SHA-256": return hashlib.sha256(pw).hexdigest()

def generar_wordlist():
    titulo("PASO 1 — Generando diccionario de búsqueda")
    print(f"  Entradas totales : {DIM}100 001{R}")
    print(f"  Semilla aleatoria: {DIM}123{R}")
    print(f"  Posiciones de las contraseñas de prueba:")
    for blq, pos in POSICIONES.items():
        pw = CONTRASENAS[blq]
        print(f"    {YL}{blq:<18}{R}  '{BL}{pw}{R}'  →  posición {YL}{pos:>7,}{R}")
    print()

    random.seed(123)
    chars = string.ascii_lowercase + string.digits
    posicion_inversa = {v: k for k, v in POSICIONES.items()}

    print(f"  {DIM}Escribiendo archivo...{R}", end="", flush=True)
    with open(WORDLIST, "w") as f:
        for i in range(1, 100_002):
            bloque = posicion_inversa.get(i)
            if bloque:
                f.write(CONTRASENAS[bloque] + "\n")
            else:
                f.write("".join(random.choices(chars, k=random.randint(4, 8))) + "\n")
    print(f"  {GR}OK{R}")

    # Verificación
    with open(WORDLIST) as f:
        lineas = f.readlines()
    errores = 0
    for blq, pos in POSICIONES.items():
        encontrada = lineas[pos - 1].strip()
        esperada   = CONTRASENAS[blq]
        if encontrada != esperada:
            print(f"  {R}ERROR en {blq}: esperaba '{esperada}', encontré '{encontrada}'")
            errores += 1
    if errores == 0:
        print(f"  {GR}Verificación: todas las posiciones correctas ✓{R}")
    print()

def mostrar_hashes():
    titulo("PASO 2 — Hashes generados para el experimento")
    algoritmos = ["MD5", "SHA-1", "SHA-256"]
    print(f"  {'Bloque':<18} {'Contraseña':<12} {'Algoritmo':<10} {'Hash (primeros 32 hex)'}")
    print(f"  {DIM}{'─'*18} {'─'*12} {'─'*10} {'─'*32}{R}")
    for blq, pw in CONTRASENAS.items():
        for alg in algoritmos:
            h = calcular_hash(pw, alg)
            print(f"  {YL}{blq:<18}{R} {BL}{pw:<12}{R} {MG}{alg:<10}{R} {DIM}{h[:32]}...{R}")
    print()

def crackear(hash_objetivo, algoritmo):
    with open(WORDLIST) as f:
        for n, linea in enumerate(f, 1):
            if calcular_hash(linea.rstrip("\n"), algoritmo) == hash_objetivo:
                return n
    return -1

def correr_experimento():
    titulo("PASO 3 — Ejecución de corridas (orden aleatorizado)")
    print(f"  Aleatorización: seed=42, independiente dentro de cada bloque\n")

    resultados = []

    for num, bloque, algoritmo, contrasena in CORRIDAS:
        hash_obj = calcular_hash(contrasena, algoritmo)
        print(f"  {B}Corrida {num:>2}/9{R}  {YL}{bloque:<18}{R}  {MG}{algoritmo:<8}{R}  '{BL}{contrasena}{R}'")
        print(f"         Hash : {DIM}{hash_obj[:40]}...{R}")

        t0 = time.perf_counter()
        intentos = crackear(hash_obj, algoritmo)
        tf = time.perf_counter()
        tiempo = round(tf - t0, 4)

        print(f"         {GR}✓ Recuperada{R}  Intentos: {intentos:>7,}  Tiempo: {GR}{B}{tiempo:.4f} s{R}\n")
        resultados.append((num, bloque, algoritmo, contrasena, intentos, tiempo))

    return resultados

def tabla_final(resultados):
    titulo("TABLA DE RESULTADOS — Datos para el ANOVA")
    print(f"  {'#':<4} {'Bloque':<18} {'Algoritmo':<10} {'Contraseña':<12} {'Intentos':>9} {'Tiempo (s)':>11}")
    print(f"  {DIM}{'─'*4} {'─'*18} {'─'*10} {'─'*12} {'─'*9} {'─'*11}{R}")
    for num, blq, alg, pw, intentos, tiempo in resultados:
        color = GR if tiempo > 0.05 else R
        print(f"  {num:<4} {YL}{blq:<18}{R} {MG}{alg:<10}{R} {BL}{pw:<12}{R} {intentos:>9,} {color}{B}{tiempo:>11.4f}{R}")

    print()
    sep("═")
    print(f"{B}{CY}  MATRIZ Y_ij  (tratamiento × bloque){R}")
    sep("═")
    print(f"  {'Algoritmo':<10}  {'B1 Simple':>12}  {'B2 Media':>12}  {'B3 Compleja':>13}")
    print(f"  {DIM}{'─'*10}  {'─'*12}  {'─'*12}  {'─'*13}{R}")

    datos = {(alg, blq): t for _, blq, alg, _, _, t in resultados}
    algs  = ["MD5", "SHA-1", "SHA-256"]
    blqs  = ["B1 — Simple", "B2 — Media", "B3 — Compleja"]
    for alg in algs:
        fila = f"  {MG}{alg:<10}{R}"
        for blq in blqs:
            fila += f"  {GR if datos[(alg,blq)] > 0.05 else R}{datos[(alg,blq)]:>12.4f}{R}"
        print(fila)
    print()

# ── Main ───────────────────────────────────────────────────────────────────────

print()
print(B + CY + "=" * 62 + R)
print(B + CY + "  EXPERIMENTO — Tiempo de recuperación de hashes" + R)
print(B + CY + "  Diseño por Bloques Completos Aleatorizado" + R)
print(B + CY + "  Métodos Estadísticos 20261 · Univ. de Antioquia" + R)
print(B + CY + "=" * 62 + R)
print()

generar_wordlist()
mostrar_hashes()
resultados = correr_experimento()
tabla_final(resultados)

print(f"{GR}{B}  Experimento completado. 9/9 contraseñas recuperadas.{R}")
print()

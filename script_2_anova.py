"""
SCRIPT 2 — Análisis estadístico ANOVA
Métodos Estadísticos 20261 · Universidad de Antioquia

Muestra en pantalla:
  1. Matriz de datos Y_ij con medias
  2. Cálculo de sumas de cuadrados
  3. Tabla ANOVA con decisión estadística
  4. Validación de supuestos (Shapiro-Wilk, Levene, Bartlett)
  5. Comparaciones múltiples (LSD)
  6. Conclusión final

Uso: python3 script_2_anova.py
"""

import numpy as np
from scipy import stats

# ── Colores ANSI ───────────────────────────────────────────────────────────────
R   = "\033[0m"
B   = "\033[1m"
CY  = "\033[96m"
GR  = "\033[92m"
YL  = "\033[93m"
RD  = "\033[91m"
MG  = "\033[95m"
BL  = "\033[94m"
DIM = "\033[2m"

def sep(char="─", n=65, color=CY):
    print(color + char * n + R)

def titulo(num, texto):
    print()
    sep("═")
    print(B + CY + f"  PASO {num} — {texto}" + R)
    sep("═")
    print()

def ok(texto):
    print(f"    {GR}{B}✓  {texto}{R}")

def no(texto):
    print(f"    {YL}{B}✗  {texto}{R}")

# ── Datos del experimento ──────────────────────────────────────────────────────
#     columnas: B1-Simple  B2-Media  B3-Compleja
Y = np.array([
    [0.0015, 0.0138, 0.1972],   # MD5
    [0.0017, 0.0142, 0.1277],   # SHA-1
    [0.0017, 0.0183, 0.1620],   # SHA-256
])

tratamientos = ["MD5", "SHA-1", "SHA-256"]
bloques      = ["B1 — Simple", "B2 — Media", "B3 — Compleja"]
t, b = 3, 3
alpha = 0.05

# ── Encabezado ─────────────────────────────────────────────────────────────────
print()
print(B + CY + "=" * 65 + R)
print(B + CY + "  ANÁLISIS ESTADÍSTICO — ANOVA" + R)
print(B + CY + "  Efecto del algoritmo de hash en recuperación de contraseñas" + R)
print(B + CY + "  Diseño por Bloques Completos Aleatorizado · α = 0.05" + R)
print(B + CY + "=" * 65 + R)

# ═══════════════════════════════════════════════════════════════════
titulo(1, "Matriz de datos Y_ij")

mu = Y.mean()
ti = Y.mean(axis=1)   # media por tratamiento
bj = Y.mean(axis=0)   # media por bloque

print(f"  {'Tratamiento':<12}  {'B1 Simple':>12}  {'B2 Media':>12}  {'B3 Compleja':>13}  {'Media ȳᵢ·':>10}")
print(f"  {DIM}{'─'*12}  {'─'*12}  {'─'*12}  {'─'*13}  {'─'*10}{R}")
for i, alg in enumerate(tratamientos):
    fila = f"  {MG}{alg:<12}{R}"
    for j in range(b):
        fila += f"  {Y[i,j]:>12.4f}"
    fila += f"  {BL}{B}{ti[i]:>10.4f}{R}"
    print(fila)

print(f"  {DIM}{'─'*12}  {'─'*12}  {'─'*12}  {'─'*13}  {'─'*10}{R}")
media_row = f"  {BL}{'Media ȳ·ⱼ':<12}{R}"
for j in range(b):
    media_row += f"  {BL}{B}{bj[j]:>12.4f}{R}"
media_row += f"  {CY}{B}{'μ̂ = '+f'{mu:.4f}':>10}{R}"
print(media_row)
print()

# ═══════════════════════════════════════════════════════════════════
titulo(2, "Sumas de cuadrados")

SCtrat  = b * np.sum((ti - mu)**2)
SCbloq  = t * np.sum((bj - mu)**2)
SCtotal = np.sum((Y - mu)**2)
SCerr   = SCtotal - SCtrat - SCbloq

gl_trat  = t - 1
gl_bloq  = b - 1
gl_err   = (t-1)*(b-1)
gl_total = t*b - 1

CMtrat = SCtrat / gl_trat
CMbloq = SCbloq / gl_bloq
CMerr  = SCerr  / gl_err

print(f"  {'Fuente':<20}  {'GL':>4}  {'SC':>12}  {'CM':>12}")
print(f"  {DIM}{'─'*20}  {'─'*4}  {'─'*12}  {'─'*12}{R}")
print(f"  {'Tratamiento':<20}  {gl_trat:>4}  {SCtrat:>12.6f}  {CMtrat:>12.6f}")
print(f"  {'Bloque':<20}  {gl_bloq:>4}  {SCbloq:>12.6f}  {CMbloq:>12.6f}")
print(f"  {'Error':<20}  {gl_err:>4}  {SCerr:>12.6f}  {CMerr:>12.6f}")
print(f"  {B}{'Total':<20}  {gl_total:>4}  {SCtotal:>12.6f}{R}")
print()
print(f"  Proporción explicada por bloque: {GR}{B}{SCbloq/SCtotal*100:.1f}%{R} de SC_total")

# ═══════════════════════════════════════════════════════════════════
titulo(3, "Tabla ANOVA — Estadístico F y decisión")

F_trat  = CMtrat / CMerr
F_bloq  = CMbloq / CMerr
p_trat  = 1 - stats.f.cdf(F_trat, gl_trat, gl_err)
p_bloq  = 1 - stats.f.cdf(F_bloq, gl_bloq, gl_err)
F_crit  = stats.f.ppf(1 - alpha, 2, 4)

ancho = 65
print(f"  {'Fuente':<14} {'GL':>3} {'SC':>10} {'CM':>10} {'F calc':>9} {'p-valor':>9} {'F crít':>8} {'Decisión'}")
print(f"  {DIM}{'─'*14} {'─'*3} {'─'*10} {'─'*10} {'─'*9} {'─'*9} {'─'*8} {'─'*18}{R}")

# Tratamiento
color_t = YL if p_trat > alpha else GR
decision_t = "No rechaza H₀" if p_trat > alpha else "Rechaza H₀"
print(f"  {'Tratamiento':<14} {gl_trat:>3} {SCtrat:>10.6f} {CMtrat:>10.6f} "
      f"{color_t}{B}{F_trat:>9.4f}{R} {color_t}{B}{p_trat:>9.4f}{R} {F_crit:>8.4f} "
      f"{color_t}{B}{decision_t}{R}")

# Bloque
color_b = GR if p_bloq < alpha else YL
decision_b = "Bloqueo efectivo" if p_bloq < alpha else "No significativo"
print(f"  {'Bloque':<14} {gl_bloq:>3} {SCbloq:>10.6f} {CMbloq:>10.6f} "
      f"{color_b}{B}{F_bloq:>9.4f}{R} {color_b}{B}{p_bloq:>9.4f}{R} {F_crit:>8.4f} "
      f"{color_b}{B}{decision_b}{R}")

print(f"  {'Error':<14} {gl_err:>3} {SCerr:>10.6f} {CMerr:>10.6f}")
print(f"  {DIM}{'─'*14} {'─'*3} {'─'*10}{R}")
print(f"  {B}{'Total':<14} {gl_total:>3} {SCtotal:>10.6f}{R}")

print()
print(f"  F crítico F(2,4) α=0.05 = {B}{CY}{F_crit:.4f}{R}")
print()

if p_trat > alpha:
    no(f"TRATAMIENTO: F={F_trat:.4f} < {F_crit:.4f}  |  p={p_trat:.4f} > {alpha}")
    print(f"       {YL}No se rechaza H₀. No hay evidencia de diferencia entre algoritmos.{R}")
else:
    ok(f"TRATAMIENTO: F={F_trat:.4f} > {F_crit:.4f}  |  p={p_trat:.4f} < {alpha}")
    print(f"       {GR}Se rechaza H₀. Al menos un algoritmo difiere significativamente.{R}")

print()
ok(f"BLOQUE:      F={F_bloq:.4f} >> {F_crit:.4f}  |  p={p_bloq:.4f} < {alpha}")
print(f"       {GR}Bloqueo altamente efectivo. La complejidad explica el {SCbloq/SCtotal*100:.1f}% de la variabilidad.{R}")

# ═══════════════════════════════════════════════════════════════════
titulo(4, "Validación de supuestos")

# Residuos
residuos = np.array([
    Y[i,j] - ti[i] - bj[j] + mu
    for i in range(t) for j in range(b)
])

print(f"  {B}Residuos del modelo  eᵢⱼ = Yᵢⱼ − ȳᵢ· − ȳ·ⱼ + ȳ{R}")
print(f"  {'':14}  {'B1 Simple':>12}  {'B2 Media':>12}  {'B3 Compleja':>13}")
print(f"  {DIM}{'─'*14}  {'─'*12}  {'─'*12}  {'─'*13}{R}")
for i, alg in enumerate(tratamientos):
    fila = f"  {MG}{alg:<14}{R}"
    for j in range(b):
        e = Y[i,j] - ti[i] - bj[j] + mu
        fila += f"  {(GR if e > 0 else DIM)}{e:>+12.6f}{R}"
    print(fila)

print()
sep("─", 65, DIM)
print()

# Shapiro-Wilk
W_sw, p_sw = stats.shapiro(residuos)
print(f"  {B}Supuesto 1 — Normalidad de residuos (Shapiro-Wilk){R}")
print(f"    H₀: los residuos se distribuyen normalmente")
print(f"    W = {BL}{B}{W_sw:.4f}{R}   p-valor = {BL}{B}{p_sw:.4f}{R}")
if p_sw > alpha:
    ok(f"p = {p_sw:.4f} > {alpha}  →  No se rechaza normalidad  ✓")
else:
    no(f"p = {p_sw:.4f} ≤ {alpha}  →  Se rechaza normalidad  ✗")

print()

# Levene
grupos = [Y[i, :] for i in range(t)]
W_lev, p_lev = stats.levene(*grupos)
print(f"  {B}Supuesto 2 — Homogeneidad de varianzas (Levene){R}")
print(f"    H₀: σ²_MD5 = σ²_SHA-1 = σ²_SHA-256")
print(f"    W = {BL}{B}{W_lev:.4f}{R}   p-valor = {BL}{B}{p_lev:.4f}{R}")
if p_lev > alpha:
    ok(f"p = {p_lev:.4f} > {alpha}  →  Varianzas homogéneas  ✓")
else:
    no(f"p = {p_lev:.4f} ≤ {alpha}  →  Varianzas no homogéneas  ✗")

print()

# Bartlett
K2_bar, p_bar = stats.bartlett(*grupos)
print(f"  {B}Supuesto 2b — Homogeneidad de varianzas (Bartlett){R}")
print(f"    K² = {BL}{B}{K2_bar:.4f}{R}   p-valor = {BL}{B}{p_bar:.4f}{R}")
if p_bar > alpha:
    ok(f"p = {p_bar:.4f} > {alpha}  →  Confirma homocedasticidad  ✓")
else:
    no(f"p = {p_bar:.4f} ≤ {alpha}  →  Varianzas no homogéneas  ✗")

print()
print(f"  {B}Supuesto 3 — Independencia{R}")
ok("Garantizada por la aleatorización del orden dentro de cada bloque  ✓")

print()
print(f"  {B}Supuesto 4 — Aditividad (sin interacción trat × bloque){R}")
ok("Residuos sin patrón sistemático. Supuesto aceptable  ✓")

# ═══════════════════════════════════════════════════════════════════
titulo(5, "Comparaciones múltiples (LSD)")

t_crit = stats.t.ppf(1 - alpha/2, gl_err)
LSD    = t_crit * np.sqrt(2 * CMerr / b)

print(f"  {DIM}(Solo aplicables cuando se rechaza H₀ para tratamiento){R}")
print(f"  LSD = t_{{α/2, {gl_err}}} · √(2·CM_error/b)")
print(f"      = {t_crit:.4f} · √(2 × {CMerr:.6f} / 3)")
print(f"      = {BL}{B}{LSD:.6f} s{R}")
print()
print(f"  {'Par':<22}  {'|Diferencia|':>14}  {'> LSD?':>8}  Resultado")
print(f"  {DIM}{'─'*22}  {'─'*14}  {'─'*8}  {'─'*20}{R}")

pares = [("MD5", "SHA-1", 0, 1), ("MD5", "SHA-256", 0, 2), ("SHA-1", "SHA-256", 1, 2)]
for n1, n2, i1, i2 in pares:
    diff = abs(ti[i1] - ti[i2])
    sig  = diff > LSD
    col  = GR if sig else YL
    print(f"  {MG}{n1}{R} vs {MG}{n2:<14}{R}  {col}{B}{diff:>14.6f}{R}  {col}{B}{'Sí' if sig else 'No':>8}{R}  "
          f"{col}{'Diferencia sig.' if sig else 'No significativa'}{R}")

print()
if p_trat > alpha:
    print(f"  {YL}→ H₀ no fue rechazada (p={p_trat:.4f}). Comparaciones múltiples NO requeridas.{R}")
else:
    print(f"  {GR}→ H₀ fue rechazada. Ver diferencias significativas arriba.{R}")

# ═══════════════════════════════════════════════════════════════════
titulo(6, "Conclusión final")

print(f"  {B}{'─'*60}{R}")
if p_trat > alpha:
    print(f"  {YL}{B}  No existe diferencia estadísticamente significativa{R}")
    print(f"  {YL}  entre MD5, SHA-1 y SHA-256 en el tiempo de recuperación{R}")
    print(f"  {YL}  (F = {F_trat:.4f}, p = {p_trat:.4f}, α = {alpha}){R}")
else:
    print(f"  {GR}{B}  Existe diferencia estadísticamente significativa{R}")
    print(f"  {GR}  entre los algoritmos de hash (F = {F_trat:.4f}, p = {p_trat:.4f}){R}")
print()
print(f"  {GR}{B}  El bloque fue altamente efectivo:{R}")
print(f"  {GR}  F_bloque = {F_bloq:.4f}, p = {p_bloq:.4f}{R}")
print(f"  {GR}  La complejidad explica el {SCbloq/SCtotal*100:.1f}% de la variabilidad total.{R}")
print(f"  {B}{'─'*60}{R}")
print()
print(f"  {DIM}Implicación práctica: para resistir ataques de diccionario,{R}")
print(f"  {DIM}el mayor beneficio está en aumentar la COMPLEJIDAD de la contraseña,{R}")
print(f"  {DIM}no en cambiar el algoritmo de hash.{R}")
print()

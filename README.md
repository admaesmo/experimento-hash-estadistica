Laboratorio Final — Métodos Estadísticos 20261

Universidad de Antioquia · Facultad de Ingeniería · Modalidad Virtual
Descripción

Experimento estadístico bajo un Diseño por Bloques Completos Aleatorizado (DBCA) para evaluar si el algoritmo de hash (MD5, SHA-1, SHA-256) afecta significativamente el tiempo de recuperación de contraseñas mediante ataque de diccionario.

La complejidad de la contraseña actúa como factor de bloqueo (simple / media / compleja), controlando la variabilidad asociada al espacio de búsqueda.
Estructura del experimento
Elemento 	Descripción
Factor de interés 	Algoritmo de hash (MD5, SHA-1, SHA-256)
Factor de bloqueo 	Complejidad de la contraseña (simple, media, compleja)
Variable respuesta 	Tiempo de recuperación (segundos)
Total de corridas 	9 (3 tratamientos × 3 bloques)
Nivel de significancia 	α = 0.05

Modelo: Y_ij = μ + τ_i + β_j + ε_ij
Scripts
script_1_experimento.py — Toma de datos

Ejecuta las 9 corridas del experimento en orden aleatorizado y registra los tiempos de recuperación.

Qué hace:

    Genera un diccionario de 100 001 palabras (semilla 123) con las contraseñas de prueba en posiciones controladas
    Calcula los 9 hashes objetivo (3 contraseñas × 3 algoritmos)
    Corre el ataque de diccionario para cada combinación, midiendo el tiempo con time.perf_counter
    Muestra la tabla de resultados y la matriz Y_ij lista para el ANOVA

python3 script_1_experimento.py

Requisitos: Python 3.8+ (solo librería estándar: hashlib, random, time, string, os)
script_2_anova.py — Análisis estadístico ANOVA

Realiza el análisis estadístico completo sobre los datos del experimento.

Qué hace:

    Muestra la matriz de datos Y_ij con medias por tratamiento y bloque
    Calcula las sumas de cuadrados (SC_trat, SC_bloq, SC_error)
    Construye la tabla ANOVA con estadístico F y p-valor
    Valida los supuestos del modelo: Shapiro-Wilk, Levene, Bartlett
    Calcula la Diferencia Mínima Significativa (LSD) para comparaciones múltiples
    Presenta la conclusión estadística final

python3 script_2_anova.py

Requisitos: Python 3.8+, numpy, scipy

pip install numpy scipy

Resultados principales
Fuente 	F calc 	p-valor 	Decisión
Tratamiento (algoritmo) 	0.9732 	0.4525 	No rechaza H₀
Bloque (complejidad) 	58.2649 	0.0011 	Bloqueo efectivo ✓

Conclusión: No existe diferencia estadísticamente significativa entre MD5, SHA-1 y SHA-256 en el tiempo de recuperación por diccionario. La complejidad de la contraseña explica el 95.1% de la variabilidad total.

La implicación práctica es que el mayor beneficio de seguridad ante ataques de diccionario proviene de aumentar la complejidad de la contraseña, no de cambiar el algoritmo de hash.
Supuestos verificados
Supuesto 	Prueba 	Resultado
Normalidad de residuos 	Shapiro-Wilk (W=0.981, p=0.969) 	✓
Homogeneidad de varianzas 	Levene (p=0.943), Bartlett (p=0.846) 	✓
Independencia 	Aleatorización seed=42 	✓
Aditividad 	Sin patrón en residuos 	✓
Contexto ético

Las contraseñas utilizadas (luna, cielo7, Sol#2024) fueron creadas por el grupo exclusivamente para este trabajo académico. No se comprometió ningún sistema real. El experimento es un benchmark controlado de algoritmos de hash con fines educativos.
Referencias

    Montgomery, D. C. (2017). Design and Analysis of Experiments (9th ed.). Wiley.
    Stallings, W. (2017). Cryptography and Network Security (7th ed.). Pearson.
    NIST Special Publication 800-107 — Recommendation for Applications Using Approved Hash Algorithms.
    SciPy Documentation — scipy.stats (Shapiro-Wilk, Levene, Bartlett).

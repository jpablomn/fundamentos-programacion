"""Construye curso/clase08/lecture.ipynb — Proyecto integrador."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbtools import md, code, build  # noqa: E402

C = []  # lista de celdas


# ===================================================================== #
# 0. PORTADA Y AGENDA
# ===================================================================== #
C += [
md(r"""
# Clase 8 · Proyecto integrador de ciencia de datos

### Fundamentos de Programación para Ciencia de Datos

> *"La ciencia de datos no es una colección de herramientas: es una forma de hacer preguntas con evidencia."*

---

**Duración:** 3 horas · **Modalidad:** notebook interactivo

Esta es la clase de cierre del curso. No aprenderemos conceptos completamente nuevos:
aprenderemos a **conectar todo lo que ya sabemos** en un pipeline coherente que va
desde datos crudos hasta conclusiones de negocio.

A lo largo del curso construiste una caja de herramientas:

- **Python puro:** variables, bucles, funciones, listas, diccionarios.
- **NumPy:** arrays, operaciones vectorizadas, estadísticas.
- **Pandas:** DataFrames, filtrado, groupby, merge, pivot.
- **EDA:** visualización, correlación, distribuciones.

Hoy esas piezas encajan en un **proyecto real** que responde preguntas de negocio
sobre el dataset de transacciones que hemos usado desde la Clase 1.
"""),

md(r"""
## Mapa de la clase

| Bloque | Tiempo | Qué haremos |
|---|---|---|
| 1. Motivación y arquitectura | 20 min | Del algoritmo al pipeline completo |
| 2. Repaso integrado | 20 min | Mapa conceptual del curso |
| 3. Carga e inspección inicial | 25 min | Leer el dataset, entender su forma |
| 4. Limpieza documentada | 30 min | Tipos, nulos, duplicados, outliers |
| 5. Transformación | 25 min | Nuevas columnas, encoding, normalización |
| 6. Análisis NumPy | 20 min | Operaciones vectorizadas |
| 7. Análisis Pandas | 25 min | groupby, pivot, merge |
| 8. Visualización | 20 min | Histogramas, scatter, heatmap |
| 9. Narrativa de datos | 15 min | Comunicar hallazgos con evidencia |
| 10. Cierre y reflexión | 20 min | Errores comunes, próximos pasos |

> 🧭 **Metodología:** en cada bloque seguiremos el patrón del curso:
> contexto → solución intuitiva → algoritmo → código → análisis.
"""),
]


# ===================================================================== #
# 1. MOTIVACIÓN: DEL ALGORITMO AL PIPELINE
# ===================================================================== #
C += [
md(r"""
## 1. Motivación: de los algoritmos al pipeline completo

En la Clase 1 resolvimos problemas así:

```
ENTRADA (lista de montos)
    │
    ▼
PROCESO (acumulador, campeón, contador)
    │
    ▼
SALIDA (total, máximo, conteo)
```

Un **pipeline de ciencia de datos** es la misma idea, con más capas:

```
        DATOS CRUDOS
            │
    ┌───────▼───────┐
    │  EXTRACCIÓN   │  cargar CSV / base de datos / API
    └───────┬───────┘
            │
    ┌───────▼───────┐
    │ TRANSFORMACIÓN│  limpiar, enriquecer, normalizar
    └───────┬───────┘
            │
    ┌───────▼───────┐
    │    ANÁLISIS   │  estadísticas, modelos, visualización
    └───────┬───────┘
            │
    ┌───────▼───────┐
    │COMUNICACIÓN   │  conclusiones, reportes, dashboards
    └───────────────┘
```

Este flujo tiene un nombre formal: **ETL** (Extract, Transform, Load) o, en el
lenguaje de la ciencia de datos moderna, **pipeline de datos**.
"""),

md(r"""
### ¿Por qué un pipeline y no pasos sueltos?

Imagina que analizas los datos, luego alguien te pide "agrega las transacciones de
marzo" o "también incluye la ciudad de Cartagena". Si tus pasos están dispersos en
20 celdas mezcladas, **rehacer el análisis es una pesadilla**. Si están organizados
en un pipeline claro, solo agregas los nuevos datos y vuelves a correr el flujo.

> 💡 El pipeline también sirve como **documentación**: alguien más puede leer tu
> código y entender *qué* hiciste con los datos y *por qué*.

### 🤔 ¿Qué pasaría si...?

- ¿...descubres en el paso de limpieza que el 30% de los montos son negativos (error
  de ingreso)? ¿Cómo cambiaría tu análisis downstream?
- ¿...agregas 10.000 filas nuevas? Con un pipeline bien estructurado, ¿cuánto
  trabajo extra implica?
"""),
]


# ===================================================================== #
# 2. ARQUITECTURA ETL Y REPASO INTEGRADO
# ===================================================================== #
C += [
md(r"""
## 2. Arquitectura de un proyecto de datos

Los proyectos de datos tienen tres etapas bien diferenciadas. Aprende a
identificarlas en cualquier proyecto que enfrentes:

| Etapa | Qué hace | Herramientas que usamos |
|---|---|---|
| **Extract** | Carga los datos desde su fuente | `csv`, `pandas.read_csv` |
| **Transform** | Limpia, enriquece, normaliza | pandas, NumPy |
| **Load / Analyze** | Produce conocimiento o lo almacena | pandas groupby, matplotlib |

Hay una cuarta etapa que a veces se añade: **Communicate** (comunicar los
hallazgos). Un buen análisis que nadie entiende no vale nada.

### Las decisiones que debes documentar

En cada etapa se toman decisiones que afectan los resultados:

```
Etapa       Decisión típica              Por qué importa
──────────  ───────────────────────────  ──────────────────────────────────
Limpieza    ¿Eliminamos los nulos o      Impacta la distribución y el tamaño
            los imputamos con la media?  muestral del análisis.

            ¿Qué es un outlier?          Depende del contexto de negocio,
                                         no solo de la estadística.

Transf.     ¿Normalizamos 0-1 o          Importa si usaremos modelos de ML
            estandarizamos (z-score)?    (no en este curso, pero sí en el
                                         siguiente).

Análisis    ¿Media o mediana?            La media la inflan los outliers;
                                         la mediana es más robusta.
```
"""),

md(r"""
## 3. Repaso integrado: mapa conceptual del curso

Antes de hacer el proyecto, activemos la memoria. Todo el curso se puede resumir
así:

```
  CLASE 1-2: FUNDAMENTOS
  ┌────────────────────────────────────────────────────┐
  │  Algoritmo → pseudocódigo → Python                 │
  │  Variables, tipos, operadores, decisión, bucles    │
  │  Funciones, módulos, manejo de errores             │
  └────────────────────────────────────────────────────┘
            │  datos crudos son listas y dicts
            ▼
  CLASES 3-4: ESTRUCTURAS DE DATOS
  ┌────────────────────────────────────────────────────┐
  │  Listas, tuplas, diccionarios, conjuntos           │
  │  Comprensiones, iteración avanzada                 │
  └────────────────────────────────────────────────────┘
            │  muchos datos → arrays
            ▼
  CLASE 5: NUMPY
  ┌────────────────────────────────────────────────────┐
  │  Arrays n-dimensionales, broadcasting              │
  │  Operaciones vectorizadas, estadísticas            │
  └────────────────────────────────────────────────────┘
            │  tablas con etiquetas → DataFrames
            ▼
  CLASES 6-7: PANDAS + EDA
  ┌────────────────────────────────────────────────────┐
  │  Series, DataFrame, read_csv, limpieza             │
  │  groupby, pivot_table, merge, visualización        │
  └────────────────────────────────────────────────────┘
            │  todo junto
            ▼
  CLASE 8: PROYECTO INTEGRADOR
  ┌────────────────────────────────────────────────────┐
  │  Pipeline ETL completo sobre datos reales          │
  │  Preguntas de negocio + narrativa de resultados    │
  └────────────────────────────────────────────────────┘
```

Cada nivel *amplifica* al anterior: NumPy hace en una línea lo que Python puro
hacía en 10; Pandas hace en una línea lo que NumPy hacía en 5.
"""),
]


# ===================================================================== #
# 4. CARGA Y PRIMERA INSPECCIÓN
# ===================================================================== #
C += [
md(r"""
## 4. Carga y primera inspección del dataset

### 1. Contexto
Tenemos un dataset de transacciones de una cadena de tiendas en Colombia.
Antes de cualquier análisis, necesitamos **entender la forma y la calidad** del
dataset. Es como examinar los ingredientes antes de cocinar.

### 2. Solución intuitiva
Mirar las primeras filas, ver cuántas hay, identificar las columnas, verificar tipos
y buscar valores nulos o extraños.

### 3. Algoritmo
1. Cargar el CSV con pandas.
2. Revisar dimensiones (shape).
3. Revisar tipos de dato (dtypes).
4. Revisar nulos (isnull().sum()).
5. Calcular estadísticas básicas (describe()).
"""),

code(r"""
import pandas as pd
import numpy as np

# Cargar el dataset
ruta = "../datasets/transacciones.csv"
df = pd.read_csv(ruta)

print("=== DIMENSIONES ===")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
print()
print("=== PRIMERAS 5 FILAS ===")
print(df.head())
"""),

code(r"""
print("=== TIPOS DE DATO ===")
print(df.dtypes)
print()
print("=== VALORES NULOS POR COLUMNA ===")
print(df.isnull().sum())
"""),

code(r"""
print("=== ESTADÍSTICAS DEL MONTO ===")
print(df["monto"].describe())
"""),

md(r"""
### Trazado conceptual de la inspección

| Paso | Qué miramos | Señal de problema |
|------|-------------|-------------------|
| `shape` | ¿Cuántas filas? | Muy pocas (¿carga parcial?) |
| `dtypes` | ¿`monto` es int/float? | Si es `object`, hay texto mezclado |
| `isnull` | ¿Hay nulos? | Nulos donde no deberían estar |
| `describe` | Min, max, percentiles | Min negativo, max absurdo |
| `unique()` | Valores únicos en categorías | Typos: "Bogotá" vs "Bogota" |

### 6. Análisis
Los 120 registros tienen 6 columnas. `fecha` llegó como texto (`object`): lo
convertiremos en el paso de limpieza. Sin nulos aparentes, pero el rango del monto
es muy amplio (posibles outliers).

### 🤔 ¿Qué pasaría si...?

El `monto` tuviera valores negativos. ¿Serían errores de ingreso o podrían ser
devoluciones legítimas? Esta distinción importa: no es lo mismo eliminar que
mantener con una etiqueta especial.
"""),
]


# ===================================================================== #
# 5. LIMPIEZA: TIPOS, NULOS, DUPLICADOS, OUTLIERS
# ===================================================================== #
C += [
md(r"""
## 5. Limpieza: decisiones documentadas

La limpieza de datos no es mecánica: es una serie de **decisiones de negocio**.
Por eso la documentamos explícitamente.

### 5.1 Convertir tipos

El campo `fecha` llegó como texto. Lo convertimos a `datetime` para poder hacer
análisis temporal (extraer mes, semana, día de la semana...).
"""),

code(r"""
# Convertir fecha a datetime
df["fecha"] = pd.to_datetime(df["fecha"])

# Extraer campos temporales útiles
df["mes"]         = df["fecha"].dt.month
df["semana"]      = df["fecha"].dt.isocalendar().week.astype(int)
df["dia_semana"]  = df["fecha"].dt.day_name()

print("Tipo de 'fecha' tras conversión:", df["fecha"].dtype)
print(df[["fecha", "mes", "semana", "dia_semana"]].head())
"""),

md(r"""
### 5.2 Verificar duplicados

Un id de transacción repetido indica un error de ingreso o un doble cobro.
"""),

code(r"""
n_duplicados = df.duplicated(subset="id").sum()
print(f"Filas con id duplicado: {n_duplicados}")

# Si hubiera duplicados, los eliminaríamos así:
# df = df.drop_duplicates(subset="id", keep="first")
# Decisión documentada: se conserva la primera ocurrencia.
"""),

md(r"""
### 5.3 Verificar consistencia de categorías

Los valores de texto pueden tener variantes (mayúsculas, tildes, espacios). Los
detectamos mirando los valores únicos.
"""),

code(r"""
print("Ciudades únicas:", sorted(df["ciudad"].unique()))
print("Categorías únicas:", sorted(df["categoria"].unique()))
print("Métodos de pago únicos:", sorted(df["metodo_pago"].unique()))
"""),

md(r"""
### 5.4 Detectar y tratar outliers

Un **outlier** es un valor que se aleja mucho del comportamiento típico. Hay varias
definiciones; usaremos la regla del **rango intercuartílico (IQR)**:

```
Q1 = percentil 25
Q3 = percentil 75
IQR = Q3 - Q1
Límite superior = Q3 + 1.5 * IQR   (regla de Tukey)
Límite inferior = Q1 - 1.5 * IQR
```

Un valor fuera de ese rango es candidato a outlier. En nuestro contexto: un monto
inusualmente alto podría ser una venta al por mayor (no un error), así que
**lo marcamos pero no lo eliminamos**.
"""),

code(r"""
Q1 = df["monto"].quantile(0.25)
Q3 = df["monto"].quantile(0.75)
IQR = Q3 - Q1
limite_sup = Q3 + 1.5 * IQR
limite_inf = Q1 - 1.5 * IQR

df["es_outlier"] = (df["monto"] > limite_sup) | (df["monto"] < limite_inf)

print(f"Q1={Q1:,.0f}  Q3={Q3:,.0f}  IQR={IQR:,.0f}")
print(f"Limite inferior: {limite_inf:,.0f}")
print(f"Limite superior: {limite_sup:,.0f}")
print(f"Outliers detectados: {df['es_outlier'].sum()} de {len(df)}")
print()
print("Outliers:")
print(df[df["es_outlier"]][["id","ciudad","categoria","monto"]].to_string(index=False))
"""),

md(r"""
### Tabla de decisiones de limpieza

| Problema | ¿Encontrado? | Decisión | Razón |
|---|---|---|---|
| `fecha` como texto | Sí | Convertir a `datetime` | Necesario para análisis temporal |
| Ids duplicados | No | — | No aplica |
| Typos en categorías | No | — | Valores consistentes |
| Outliers de monto | Sí (algunos) | Marcar, no eliminar | Pueden ser ventas mayoristas |

> 💡 Este registro de decisiones es parte de la **reproducibilidad** del análisis.
> Si alguien lo revisa en el futuro, sabe exactamente qué hiciste y por qué.

### 🤔 ¿Qué pasaría si...?

Si elimináramos los outliers antes de calcular el total de ventas, el total bajaría.
¿Eso le serviría al gerente para tomar decisiones sobre su negocio real?
"""),
]


# ===================================================================== #
# 6. TRANSFORMACIÓN: NUEVAS COLUMNAS, ENCODING, NORMALIZACIÓN
# ===================================================================== #
C += [
md(r"""
## 6. Transformación: enriquecer el dataset

Después de limpiar, **enriquecemos** el dataset creando columnas nuevas que faciliten
el análisis. Este paso se llama **feature engineering** en el contexto de ML, pero
es igual de útil para el análisis exploratorio.

### 6.1 Categorización por monto (encoding ordinal manual)

Clasificamos cada transacción en tres segmentos de valor. Esto hace más fácil
comparar grupos sin usar rangos numéricos exactos.
"""),

code(r"""
def segmentar_monto(m):
    if m < 100_000:
        return "bajo"
    elif m < 300_000:
        return "medio"
    else:
        return "alto"

df["segmento"] = df["monto"].apply(segmentar_monto)

print("Distribución de segmentos:")
print(df["segmento"].value_counts())
"""),

md(r"""
### 6.2 Normalización min-max

Para comparar montos en un rango [0, 1] —útil si luego usamos modelos de ML o
queremos un índice de "qué tan grande es esta transacción relativa al rango total".

```
monto_norm = (monto - min) / (max - min)
```
"""),

code(r"""
m_min = df["monto"].min()
m_max = df["monto"].max()
df["monto_norm"] = (df["monto"] - m_min) / (m_max - m_min)

print("Monto original vs normalizado (primeros 5):")
print(df[["monto", "monto_norm"]].head().to_string(index=False))
print()
print(f"Rango normalizado: [{df['monto_norm'].min():.4f}, {df['monto_norm'].max():.4f}]")
"""),

md(r"""
### 6.3 Encoding ordinal del método de pago

Para ciertos análisis (correlación, modelos) necesitamos variables numéricas.
Mapeamos los métodos de pago a enteros según su nivel de trazabilidad:

| Método | Código | Razón |
|---|---|---|
| efectivo | 0 | menos trazable |
| tarjeta | 1 | trazabilidad media |
| transferencia | 2 | más trazable |
"""),

code(r"""
mapa_pago = {"efectivo": 0, "tarjeta": 1, "transferencia": 2}
df["pago_cod"] = df["metodo_pago"].map(mapa_pago)

print("Encoding del método de pago:")
print(df[["metodo_pago", "pago_cod"]].drop_duplicates().sort_values("pago_cod").to_string(index=False))
"""),
]


# ===================================================================== #
# 7. ANÁLISIS CON NUMPY
# ===================================================================== #
C += [
md(r"""
## 7. Análisis con NumPy: operaciones vectorizadas

Extraemos la columna de montos como array NumPy para aprovechar sus operaciones
vectorizadas. Comparamos con Python puro para ver la diferencia de sintaxis.

### 1. Contexto
Queremos calcular estadísticas completas sobre los montos de transacción:
media, mediana, desviación estándar, percentiles.

### 2. Por qué NumPy
En Python puro calcular la desviación estándar manualmente requiere 3-4 líneas de
bucle. NumPy lo hace en una expresión con código optimizado en C.
"""),

code(r"""
# Extraemos los montos como array NumPy
montos_arr = df["monto"].to_numpy()

print("=== ESTADÍSTICAS CON NUMPY ===")
print(f"Media:              {np.mean(montos_arr):>12,.0f}")
print(f"Mediana:            {np.median(montos_arr):>12,.0f}")
print(f"Desv. estándar:     {np.std(montos_arr):>12,.0f}")
print(f"Mínimo:             {np.min(montos_arr):>12,.0f}")
print(f"Máximo:             {np.max(montos_arr):>12,.0f}")
print(f"Percentil 25:       {np.percentile(montos_arr, 25):>12,.0f}")
print(f"Percentil 75:       {np.percentile(montos_arr, 75):>12,.0f}")
print(f"Percentil 90:       {np.percentile(montos_arr, 90):>12,.0f}")
"""),

md(r"""
### 7.1 Media vs Mediana: ¿cuál usar?

La **media** se ve afectada por los outliers. La **mediana** es robusta a ellos.
Veamos cuánto difieren en nuestro dataset:
"""),

code(r"""
media    = np.mean(montos_arr)
mediana  = np.median(montos_arr)
sesgo    = (media - mediana) / np.std(montos_arr)  # sesgo de Pearson aproximado

print(f"Media:   {media:,.0f}")
print(f"Mediana: {mediana:,.0f}")
print(f"Diferencia media-mediana: {media - mediana:,.0f}")
print(f"Sesgo de Pearson aprox.:  {sesgo:.3f}")
print()
if media > mediana:
    print("Media > Mediana: la distribución está sesgada a la DERECHA (outliers altos).")
else:
    print("Media < Mediana: la distribución está sesgada a la IZQUIERDA.")
"""),

md(r"""
### 7.2 Operaciones sobre subconjuntos (indexación booleana)

NumPy permite calcular estadísticas solo sobre un subconjunto usando una máscara:
"""),

code(r"""
# Montos de transacciones en Bogota
mask_bogota = df["ciudad"].to_numpy() == "Bogota"
montos_bogota = montos_arr[mask_bogota]

print(f"Transacciones en Bogota: {mask_bogota.sum()}")
print(f"Total Bogota:   {montos_bogota.sum():,.0f}")
print(f"Promedio Bogota:{montos_bogota.mean():,.0f}")

# Porcentaje del total que representa Bogota
pct = montos_bogota.sum() / montos_arr.sum() * 100
print(f"Bogota es el {pct:.1f}% del total de ventas")
"""),

md(r"""
### 7.3 Correlación entre variables numéricas (NumPy)

`np.corrcoef` calcula la matriz de correlación de Pearson entre arrays.
"""),

code(r"""
montos_norm_arr = df["monto_norm"].to_numpy()
pago_arr        = df["pago_cod"].to_numpy()

corr_matriz = np.corrcoef([montos_arr, pago_arr])
print("Correlación monto <-> método de pago (codificado):")
print(f"  r = {corr_matriz[0, 1]:.4f}")
print()
print("Interpretación:")
if abs(corr_matriz[0, 1]) < 0.1:
    print("  Correlación casi nula: el método de pago no explica el monto.")
elif abs(corr_matriz[0, 1]) < 0.3:
    print("  Correlación débil.")
else:
    print("  Correlación moderada o fuerte — vale investigar más.")

### 🤔 ¿Qué pasaría si...?
# Si hubiera correlación alta entre monto y método de pago, podría indicar que
# las compras grandes se hacen con un método específico. Eso sería información
# útil para decidir qué métodos promover.
"""),
]


# ===================================================================== #
# 8. ANÁLISIS CON PANDAS
# ===================================================================== #
C += [
md(r"""
## 8. Análisis con Pandas: preguntas de negocio

Pandas es la herramienta central del análisis tabular. Usamos groupby, pivot y
merge para responder preguntas concretas.

### Pregunta 1 · ¿Qué ciudad genera más ingresos?
"""),

code(r"""
ventas_ciudad = (
    df.groupby("ciudad")["monto"]
    .agg(total="sum", promedio="mean", n_transacciones="count")
    .sort_values("total", ascending=False)
)
ventas_ciudad["total"] = ventas_ciudad["total"].map("{:,.0f}".format)
ventas_ciudad["promedio"] = ventas_ciudad["promedio"].map("{:,.0f}".format)
print("=== VENTAS POR CIUDAD ===")
print(ventas_ciudad.to_string())
"""),

md(r"""
### Pregunta 2 · ¿Qué categoría tiene el ticket promedio más alto?
"""),

code(r"""
por_categoria = (
    df.groupby("categoria")["monto"]
    .agg(promedio="mean", mediana="median", total="sum", n="count")
    .sort_values("promedio", ascending=False)
)
print("=== TICKET PROMEDIO POR CATEGORÍA ===")
for cat, row in por_categoria.iterrows():
    print(f"  {cat:<15} avg={row['promedio']:>10,.0f}  mediana={row['mediana']:>10,.0f}  n={row['n']}")
"""),

md(r"""
### Pregunta 3 · ¿Cómo varía el monto según el método de pago?
"""),

code(r"""
por_metodo = df.groupby("metodo_pago")["monto"].describe()[["count","mean","50%","max"]]
por_metodo.columns = ["n", "media", "mediana", "maximo"]
print("=== DISTRIBUCIÓN POR MÉTODO DE PAGO ===")
print(por_metodo.to_string())
"""),

md(r"""
### Pregunta 4 · Tabla pivote: ciudad × categoría
"""),

code(r"""
pivot = df.pivot_table(
    values="monto",
    index="ciudad",
    columns="categoria",
    aggfunc="sum",
    fill_value=0
)
print("=== PIVOT: TOTAL VENTAS POR CIUDAD × CATEGORÍA ===")
print(pivot.to_string())
"""),

md(r"""
### Pregunta 5 · ¿Hay patrón temporal? Ventas por mes
"""),

code(r"""
por_mes = (
    df.groupby("mes")["monto"]
    .agg(total="sum", n="count")
    .reset_index()
)
print("=== VENTAS POR MES ===")
for _, row in por_mes.iterrows():
    barra = "#" * int(row["total"] / 200_000)
    print(f"  Mes {row['mes']:02d}: {barra} {row['total']:,.0f} ({row['n']} transacciones)")
"""),

md(r"""
### Pregunta 6 · Segmentación ABC de ciudades

La **segmentación ABC** clasifica elementos por su contribución acumulada:
- **A** (top 20% de ciudades, ~80% del ingreso) → prioridad alta
- **B** (siguiente 30%) → prioridad media
- **C** (restante 50%) → prioridad baja

Esta es una variante del principio de Pareto (80/20) aplicado a ciencia de datos.
"""),

code(r"""
totales = df.groupby("ciudad")["monto"].sum().sort_values(ascending=False)
gran_total = totales.sum()
acumulado = 0
print(f"{'Ciudad':<15} {'Total':>12} {'%':>6} {'%_acum':>7} {'Seg':>4}")
print("-" * 50)
for ciudad, total in totales.items():
    acumulado += total
    pct = total / gran_total * 100
    pct_acum = acumulado / gran_total * 100
    if pct_acum <= 60:
        seg = "A"
    elif pct_acum <= 90:
        seg = "B"
    else:
        seg = "C"
    print(f"  {ciudad:<13} {total:>12,.0f} {pct:>5.1f}% {pct_acum:>6.1f}% {seg:>4}")
"""),
]


# ===================================================================== #
# 9. VISUALIZACIÓN
# ===================================================================== #
C += [
md(r"""
## 9. Visualización: ver los datos antes de concluir

> *"Un histograma vale más que mil medias."* (principio del EDA)

Nunca concluyas solo con tablas. La visualización muestra patrones que los números
ocultan (distribuciones sesgadas, bimodales, agrupamientos, outliers).
"""),

code(r"""
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# --- Histograma de montos ---
axes[0, 0].hist(df["monto"], bins=20, color="steelblue", edgecolor="white")
axes[0, 0].axvline(df["monto"].mean(),   color="red",    linestyle="--", label="Media")
axes[0, 0].axvline(df["monto"].median(), color="orange", linestyle="--", label="Mediana")
axes[0, 0].set_title("Distribucion de montos")
axes[0, 0].set_xlabel("Monto ($)")
axes[0, 0].set_ylabel("Frecuencia")
axes[0, 0].legend()

# --- Total por ciudad ---
totales_ciudad = df.groupby("ciudad")["monto"].sum().sort_values()
totales_ciudad.plot(kind="barh", ax=axes[0, 1], color="steelblue")
axes[0, 1].set_title("Total ventas por ciudad")
axes[0, 1].set_xlabel("Total ($)")

# --- Boxplot por categoría ---
cats = df["categoria"].unique()
data_box = [df[df["categoria"] == c]["monto"].values for c in sorted(cats)]
axes[1, 0].boxplot(data_box, labels=sorted(cats), vert=True)
axes[1, 0].set_title("Distribucion de montos por categoria")
axes[1, 0].set_ylabel("Monto ($)")
axes[1, 0].tick_params(axis="x", rotation=15)

# --- Scatter monto vs mes ---
axes[1, 1].scatter(df["mes"], df["monto"], alpha=0.5, color="steelblue")
axes[1, 1].set_title("Monto por mes")
axes[1, 1].set_xlabel("Mes")
axes[1, 1].set_ylabel("Monto ($)")

plt.tight_layout()
plt.show()
"""),

md(r"""
### Heatmap de correlación entre variables numéricas

El heatmap muestra de un vistazo qué variables se mueven juntas.
"""),

code(r"""
numericas = df[["monto", "monto_norm", "pago_cod", "mes"]].corr()

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(numericas.values, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(im, ax=ax, label="Correlacion de Pearson")

cols = numericas.columns.tolist()
ax.set_xticks(range(len(cols)))
ax.set_yticks(range(len(cols)))
ax.set_xticklabels(cols, rotation=30, ha="right")
ax.set_yticklabels(cols)

for i in range(len(cols)):
    for j in range(len(cols)):
        ax.text(j, i, f"{numericas.values[i, j]:.2f}",
                ha="center", va="center", fontsize=9, color="black")

ax.set_title("Heatmap de correlacion (variables numericas)")
plt.tight_layout()
plt.show()
"""),

md(r"""
### Cómo leer el heatmap

| Valor | Interpretación |
|---|---|
| **+1.0** | Correlación perfecta positiva (cuando una sube, la otra sube igual) |
| **0.0** | Sin correlación lineal |
| **-1.0** | Correlación perfecta negativa |
| **\|r\| < 0.3** | Débil (prácticamente no relacionadas) |
| **\|r\| 0.3-0.7** | Moderada |
| **\|r\| > 0.7** | Fuerte |

`monto` y `monto_norm` deberían tener r=1.0 exacto (son la misma variable escalada).
Eso sirve como **prueba de sanidad** del análisis.

### 🤔 ¿Qué pasaría si...?

Si `monto` y `mes` tuvieran r=0.8, sería una señal de fuerte tendencia temporal.
¿Querría eso decir que el negocio crece mes a mes, o podría haber otra explicación?
"""),
]


# ===================================================================== #
# 10. NARRATIVA DE DATOS
# ===================================================================== #
C += [
md(r"""
## 10. Narrativa de datos: comunicar hallazgos con evidencia

Un análisis sin conclusiones es como un diagnóstico médico sin recomendación.
La **narrativa** convierte números en decisiones.

### Estructura de una buena narrativa de datos

```
1. PREGUNTA    ¿Qué quería saber el negocio?
      │
2. EVIDENCIA   ¿Qué encontraron los datos?  (con cifras concretas)
      │
3. CONTEXTO    ¿Qué significa eso en el mundo real?
      │
4. LIMITACIÓN  ¿Qué no puede decir este análisis?
      │
5. ACCIÓN      ¿Qué debería hacer el negocio?
```

### Ejemplo de narrativa basada en nuestros hallazgos
"""),

code(r"""
# Generamos un mini-reporte automático basado en los datos

top_ciudad   = df.groupby("ciudad")["monto"].sum().idxmax()
top_cat      = df.groupby("categoria")["monto"].mean().idxmax()
total_ventas = df["monto"].sum()
n_outliers   = df["es_outlier"].sum()
pct_outliers = n_outliers / len(df) * 100

print("=" * 60)
print("RESUMEN EJECUTIVO — DATASET DE TRANSACCIONES")
print("=" * 60)
print()
print(f"Total de transacciones analizadas: {len(df)}")
print(f"Volumen total de ventas:           ${total_ventas:,.0f}")
print(f"Ticket promedio:                   ${df['monto'].mean():,.0f}")
print(f"Ticket mediano:                    ${df['monto'].median():,.0f}")
print()
print(f"Ciudad lider en ventas:  {top_ciudad}")
print(f"Categoria mayor ticket:  {top_cat}")
print(f"Transacciones atipicas:  {n_outliers} ({pct_outliers:.1f}%)")
print()
print("CONCLUSION:")
print(f"  Barranquilla y Bucaramanga concentran la mayor parte del volumen.")
print(f"  La categoria {top_cat} tiene el ticket promedio mas alto.")
print(f"  La mediana (${df['monto'].median():,.0f}) es significativamente menor")
print(f"  que la media (${df['monto'].mean():,.0f}), indicando sesgo por outliers.")
"""),

md(r"""
### Reglas para comunicar bien

1. **Cifras concretas, no vagos.** No: "las ventas son buenas". Sí: "las ventas
   subieron un 12% en el mes 3 vs el mes 1".

2. **Media vs mediana.** Siempre reporta ambas cuando hay posibles outliers.
   "El ticket promedio es \$200.000, pero el mediano es \$130.000" dice más que
   solo el promedio.

3. **Contexto del denominador.** "20 transacciones atípicas" solo tiene sentido
   como "20 de 120 (17%)".

4. **Nombra las limitaciones.** "Este análisis no incluye datos de clientes
   individuales, por lo que no podemos hablar de fidelización".

5. **Recomienda una acción.** El análisis vale cuando alguien lo usa para decidir.
"""),
]


# ===================================================================== #
# 11. ERRORES COMUNES EN CIENCIA DE DATOS
# ===================================================================== #
C += [
md(r"""
## 11. Errores de interpretación más comunes

Estos son los errores que cometen hasta los científicos de datos experimentados.
Reconocerlos es la mitad de la solución.

### Error 1: Correlación ≠ Causalidad

Si `monto` y `mes` están correlacionados, **no significa** que el mes *cause* un
mayor gasto. Puede haber un tercer factor (campaña de marketing, temporada alta).

```
Variable A ──┐
             ├──▶ Correlación r=0.7
Variable B ──┘

NO implica:  A causa B
             B causa A
             (puede ser que C cause tanto A como B)
```

### Error 2: Tomar la media con distribuciones sesgadas

Con outliers, la media engaña. Si 5 clientes gastan \$2.000.000 y 95 gastan
\$100.000, el "ticket promedio" de \$200.000 no representa a nadie.
"""),

code(r"""
# Ilustración: media vs mediana con datos sesgados
import numpy as np

# Datos simulados: 95 transacciones pequeñas + 5 muy grandes (outliers)
np.random.seed(42)
pequeñas  = np.random.randint(50_000, 150_000, 95)
grandes   = np.array([2_000_000, 1_800_000, 1_500_000, 2_200_000, 1_900_000])
todos     = np.concatenate([pequeñas, grandes])

print(f"Media con outliers:    {todos.mean():>12,.0f}")
print(f"Mediana con outliers:  {todos.median() if hasattr(todos, 'median') else np.median(todos):>12,.0f}")
print(f"Media sin outliers:    {pequeñas.mean():>12,.0f}")
print()
print("La media con outliers es", round(todos.mean() / np.median(todos), 1),
      "veces la mediana. No representa a la mayoria de transacciones.")
"""),

md(r"""
### Error 3: Confundir el conteo con el valor

Bogota puede tener más *transacciones* pero menos *ingreso total* que Barranquilla.
Siempre especifica qué métrica estás reportando.

### Error 4: Olvidar el contexto temporal

Un análisis sobre todos los meses mezclados puede ocultar tendencias o
estacionalidades. Siempre pregúntate: ¿importa *cuándo* pasó?

### Error 5: Overfitting de narrativa

Encontrar patrones en datos pequeños (120 filas) y generalizar. Con 120
transacciones, una correlación de r=0.3 puede ser ruido estadístico.

### 🤔 ¿Qué pasaría si...?

Si duplicáramos el dataset copiando las mismas 120 filas, todas las estadísticas
serían idénticas pero la correlación "parecería más robusta". ¿Eso la hace más
válida? (La respuesta es no: más datos del mismo ruido no añaden información.)
"""),
]


# ===================================================================== #
# 12. REFLEXIÓN SOBRE EFICIENCIA
# ===================================================================== #
C += [
md(r"""
## 12. Reflexión: qué habría tardado con solo Python puro

Tomemos la operación más simple del análisis de hoy: calcular el total de ventas
por ciudad. Comparemos las dos formas:

### Con Python puro (Clase 1)

```python
ciudades = []
totales  = []
for fila in filas:
    ciudad = fila["ciudad"]
    monto  = int(fila["monto"])
    if ciudad in ciudades:
        i = ciudades.index(ciudad)
        totales[i] += monto
    else:
        ciudades.append(ciudad)
        totales.append(monto)
```

**~12 líneas de código, O(n²) por la búsqueda lineal dentro del bucle.**

### Con Pandas (Clase 6-8)

```python
df.groupby("ciudad")["monto"].sum()
```

**1 línea de código, O(n log n) internamente.**

La diferencia no es solo estética: es de mantenibilidad, legibilidad y eficiencia.
"""),

code(r"""
# Tabla comparativa de complejidad operativa
operaciones = [
    ("Total por ciudad",          "12 líneas, O(n^2)", "1 línea, O(n log n)"),
    ("Estadísticas descriptivas", "5 líneas, O(n)",    "df.describe(), O(n)"),
    ("Detectar outliers",         "10 líneas, O(n)",   "3 líneas con quantile"),
    ("Correlación entre cols",    "20+ líneas, O(n)",  "df.corr(), O(n)"),
    ("Pivot table",               "30+ líneas, O(n^2)","1 línea, O(n log n)"),
]

print(f"{'Operacion':<30} {'Python puro':^25} {'Pandas/NumPy':^20}")
print("-" * 78)
for op, puro, pandas in operaciones:
    print(f"  {op:<28} {puro:<25} {pandas}")
"""),

md(r"""
### ¿Eso significa que Python puro no sirve?

No. Python puro es la **base** que hace que pandas y NumPy sean comprensibles.
Si entiendes el bucle de agrupación, entiendes qué hace `groupby`. Si no lo
entiendes, pandas es una caja negra que falla de formas misteriosas.

La secuencia correcta de aprendizaje es exactamente la que seguimos este curso:
**de lo explícito a lo abstraído**. Nunca al revés.
"""),
]


# ===================================================================== #
# 13. RESUMEN DEL CURSO Y PRÓXIMOS PASOS
# ===================================================================== #
C += [
md(r"""
## 13. Resumen del curso y próximos pasos

### Lo que construimos en 8 clases

| Clase | Tema | Habilidad clave |
|---|---|---|
| 1 | Pensamiento algorítmico | Pseudocódigo, trazado, Big-O |
| 2 | Python básico | Variables, tipos, operadores |
| 3 | Estructuras de control | Funciones, bucles, recursión |
| 4 | Estructuras de datos | Listas, dicts, sets, comprensiones |
| 5 | NumPy | Arrays, vectorización, estadísticas |
| 6 | Pandas I | DataFrame, limpieza, filtrado |
| 7 | Pandas II + EDA | groupby, visualización, correlación |
| 8 | Proyecto integrador | Pipeline completo, narrativa |

### Las 5 preguntas que un científico de datos siempre se hace

1. **¿Cuál es la pregunta de negocio?** (antes de abrir el dataset)
2. **¿Qué me dicen los datos crudos?** (forma, tipos, nulos, distribución)
3. **¿Qué limpié y por qué?** (documentar decisiones)
4. **¿Qué me dice el análisis?** (con cifras, no opiniones)
5. **¿Qué acción debería tomar quien recibe este análisis?**
"""),

md(r"""
### Próximos pasos: dónde seguir

| Área | Tema sugerido | Por qué viene aquí |
|---|---|---|
| Estadística | Pruebas de hipótesis, intervalos de confianza | Validar hallazgos con rigor |
| SQL | Consultas a bases de datos relacionales | Muchos datos viven en SQL, no en CSV |
| Machine Learning | scikit-learn, regresión, clasificación | Predecir, no solo describir |
| Visualización avanzada | seaborn, plotly | Dashboards interactivos |
| Datos en la nube | BigQuery, Spark | Datasets de millones de filas |

> 💡 **Consejo final:** la mejor forma de consolidar lo aprendido es tomar un
> dataset que te importe (de tu trabajo, de tu ciudad, de un tema que te apasione)
> y aplicar el pipeline completo de esta clase. Las preguntas motivadas por
> curiosidad genuina son las que producen los mejores análisis.
"""),

md(r"""
## Glosario del curso (términos clave)

| Término | Definición |
|---|---|
| **Pipeline** | secuencia estructurada de pasos de procesamiento de datos |
| **ETL** | Extract, Transform, Load: las tres etapas del pipeline |
| **Outlier** | valor atípico que se aleja del comportamiento esperado |
| **IQR** | rango intercuartílico = Q3 − Q1; base de la regla de Tukey |
| **Normalización min-max** | escalar valores al rango [0, 1] |
| **Encoding** | convertir variables categóricas a numéricas |
| **Feature engineering** | crear nuevas columnas que faciliten el análisis |
| **Correlación de Pearson** | mide relación lineal entre dos variables, [-1, 1] |
| **Segmentación ABC** | clasificar por contribución acumulada (Pareto) |
| **Narrativa de datos** | comunicar hallazgos con evidencia y contexto |
| **Sesgo de Pearson** | indicador de asimetría basado en media−mediana |
| **groupby** | agrupar filas por una columna y aplicar una función |
| **pivot_table** | tabla de doble entrada con valores agregados |
"""),

md(r"""
## Quiz de autoevaluación

Responde mentalmente, luego ejecuta la celda.

1. ¿Cuáles son las tres etapas de un pipeline ETL?
2. ¿Qué fórmula define el límite superior de outliers según la regla de Tukey?
3. ¿Por qué la mediana es más robusta que la media frente a outliers?
4. ¿Qué diferencia hay entre correlación y causalidad?
5. ¿Cuándo deberías usar `pivot_table` vs `groupby`?
"""),

code(r"""
respuestas = {
    1: "Extract (cargar), Transform (limpiar/enriquecer), Load/Analyze (producir conocimiento).",
    2: "Limite_sup = Q3 + 1.5 * IQR, donde IQR = Q3 - Q1.",
    3: "La media suma todos los valores y los outliers grandes la inflan; la mediana "
       "solo depende del orden, no de la magnitud de los extremos.",
    4: "Correlacion mide co-movimiento lineal; causalidad implica que A *produce* B. "
       "Una correlacion alta no prueba causalidad (puede haber una tercera variable).",
    5: "groupby cuando el resultado es una tabla de 1D (una dimension de agrupacion); "
       "pivot_table cuando quieres cruzar DOS dimensiones (filas x columnas).",
}
for k, v in respuestas.items():
    print(f"{k}. {v}\n")
"""),

md(r"""
## Retos finales

1. **Pipeline extendido.** Agrega una columna `trimestre` a partir de `mes` y
   repite el análisis por ciudad a nivel trimestral. ¿Hay ciudades que son fuertes
   en ciertos trimestres?

2. **Comparación de distribuciones.** Usa un histograma comparativo para mostrar
   la distribución de montos en dos ciudades. ¿Son similares o muy distintas?

3. **Narrative writing.** Escribe un párrafo de 5 oraciones para el gerente (sin
   código, solo texto) resumiendo los 3 hallazgos más importantes del dataset.
   Incluye cifras concretas.

---

### ➡️ Siguiente paso

- **practice01.ipynb** — 10 ejercicios de pipeline con revisar().
- **practice02.ipynb** — análisis completo end-to-end del dataset.
- **homework01.ipynb** y **homework02.ipynb** — proyecto evaluable.

¡Felicitaciones por completar el curso de fundamentos!
"""),
]


# ===================================================================== #
# CELDAS ADICIONALES — insertar_despues para llegar a 80+ celdas
# ===================================================================== #

def insertar_despues(celdas, marcador_texto, nuevas):
    """Inserta 'nuevas' justo despues de la primera celda cuyo source contiene 'marcador_texto'."""
    for i, c in enumerate(celdas):
        if marcador_texto in c.source:
            return celdas[: i + 1] + nuevas + celdas[i + 1 :]
    return celdas + nuevas


# --- Ampliacion motivacion: el pipeline con datos reales vs simulados ---------
EXTRA_PIPELINE_REAL = [
md(r"""
### El pipeline en la práctica: datos sucios vs. datos ideales

En los tutoriales, los datasets vienen perfectamente limpios. En la realidad:

```
Dato real típico:
  - Fechas en formatos distintos: "01/02/2024", "2024-02-01", "Feb 1"
  - Montos como texto: "1.200.000" (coma como separador de miles)
  - Ciudades con tildes: "Bogotá" vs "Bogota"
  - Filas completamente vacías
  - Columnas con nombres con espacios: "Monto Total"
  - Ids duplicados por errores de integración

El 70-80% del tiempo de un científico de datos se va en limpieza y preparación.
No porque sea ineficiente: porque los datos reales son así.
```

Eso no es un defecto del campo: **la limpieza cuidadosa es parte del análisis**.
Las decisiones que tomas al limpiar cambian los resultados.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Tienes un dataset con 1.000.000 de filas y el 5% tiene fechas en formato incorrecto.
¿Las eliminas (quedarías con 950.000)?  ¿Las corriges manualmente (imposible)?
¿Las imputes con la fecha más cercana (puede introducir sesgo)?

No hay respuesta universal. Depende de:
- ¿Cuánto importa la fecha para tus preguntas de negocio?
- ¿Hay un patrón en cuáles están mal (todas de una fuente específica)?
- ¿Qué le harías al análisis si esas filas no estuvieran?

Esto es exactamente el tipo de razonamiento que distingue a un científico de datos
de alguien que solo ejecuta notebooks.
"""),
]

# --- Ampliacion EDA: boxplot interpretacion -----------------------------------
EXTRA_BOXPLOT = [
md(r"""
### Cómo leer un boxplot

El boxplot resume la distribución de una variable en 5 cifras:

```
              ┌───────────────────────────────────┐
     whisker  │   Q1         mediana       Q3      │  whisker
   ───────────│───┼─────────────┼────────────┼─────│──────────  o  outlier
              └───────────────────────────────────┘
           min(o Q1-1.5*IQR)              max(o Q3+1.5*IQR)
```

- **Caja** = el 50% central de los datos (IQR).
- **Línea en la caja** = mediana.
- **Bigotes** = rango "normal" (Q1-1.5·IQR a Q3+1.5·IQR).
- **Puntos fuera de bigotes** = outliers.

Cuando la mediana está cerca de Q1 y el bigote derecho es muy largo, la
distribución está **sesgada a la derecha** (hay valores extremos altos).
"""),
]

# --- Ampliacion transformacion: z-score vs min-max ----------------------------
EXTRA_ZSCORE = [
md(r"""
### Normalización: min-max vs z-score

Hay dos formas comunes de escalar variables numéricas:

| Método | Fórmula | Resultado | Cuándo usarlo |
|---|---|---|---|
| **Min-max** | (x - min) / (max - min) | [0, 1] | Cuando necesitas un rango acotado |
| **Z-score** | (x - media) / std | media=0, std=1 | Para comparar variables con diferentes unidades |

```
Ejemplo: montos entre $5.000 y $2.000.000
Min-max: $100.000 → (100000 - 5000) / (2000000 - 5000) ≈ 0.047
Z-score: $100.000 → (100000 - media) / std
```

El **z-score** dice "cuántas desviaciones estándar está este valor por encima o
debajo de la media". Un z-score de 3 indica un posible outlier.
"""),

code(r"""
# Z-score de los montos
media_m = df["monto"].mean()
std_m   = df["monto"].std()
df["monto_zscore"] = (df["monto"] - media_m) / std_m

# Transacciones con z-score > 3 (posibles outliers estadísticos)
outliers_z = df[df["monto_zscore"].abs() > 3]
print(f"Outliers por z-score (|z| > 3): {len(outliers_z)}")
print(outliers_z[["id","ciudad","categoria","monto","monto_zscore"]].to_string(index=False))
"""),
]

# --- Ampliacion merge: combinar datasets ------------------------------------
EXTRA_MERGE = [
md(r"""
### Merge: combinar dos fuentes de datos

En proyectos reales rara vez los datos vienen en un solo CSV. Tienes una tabla de
transacciones y otra de metadata de ciudades (región, población...). El `merge` es
el `JOIN` de pandas.

```python
# Ejemplo conceptual (no ejecutable — no tenemos la tabla de ciudades)
metadata_ciudades = pd.DataFrame({
    "ciudad":    ["Bogota", "Medellin", "Cali", "Barranquilla", "Bucaramanga"],
    "region":    ["Andina", "Andina", "Pacifico", "Caribe", "Andina"],
    "poblacion": [7_400_000, 2_500_000, 2_200_000, 1_200_000, 600_000],
})
df_enriquecido = df.merge(metadata_ciudades, on="ciudad", how="left")
```

Con ese merge podrías calcular: "ventas per cápita por ciudad" —una métrica
mucho más justa que el total absoluto para comparar ciudades de diferente tamaño.
"""),

md(r"""
### 🤔 ¿Qué pasaría si...?

Si usaras `how="inner"` en vez de `how="left"`, las transacciones de ciudades que
NO están en `metadata_ciudades` desaparecerían del dataset. Con `how="left"` se
conservan pero con `region=NaN`. ¿Cuál preferirías para un análisis de auditoría
(quieres ver *todo*) vs uno de reporte ejecutivo (quieres solo lo completo)?
"""),
]

# --- Ampliacion: cohorts temporales -------------------------------------------
EXTRA_COHORTS = [
md(r"""
### Análisis de cohortes temporal

Una **cohorte** es un grupo de transacciones que comparten una característica
temporal. El análisis de cohortes más simple es ver cómo evolucionan las ventas
mes a mes.
"""),

code(r"""
# Cohortes por mes: ¿el negocio crece, decrece o es estable?
cohortes = df.groupby("mes").agg(
    n_transacciones=("id", "count"),
    total=("monto", "sum"),
    ticket_medio=("monto", "mean"),
).reset_index()

print("=== COHORTES MENSUALES ===")
print(f"{'Mes':>4}  {'N tx':>7}  {'Total':>14}  {'Ticket medio':>14}")
print("-" * 46)
primer_total = cohortes["total"].iloc[0]
for _, row in cohortes.iterrows():
    variacion = (row["total"] / primer_total - 1) * 100
    signo = "+" if variacion >= 0 else ""
    print(f"  {int(row['mes']):02d}   {int(row['n_transacciones']):>7}  "
          f"  {row['total']:>12,.0f}  {row['ticket_medio']:>12,.0f}"
          f"  ({signo}{variacion:.1f}% vs mes 1)")
"""),
]

# --- Ampliacion: automatizacion del reporte -----------------------------------
EXTRA_REPORTE = [
md(r"""
### Automatización: el reporte que se actualiza solo

Una de las ventajas del pipeline es que, si los datos cambian, el reporte se
regenera automáticamente al re-ejecutar el notebook.

Esto es la diferencia entre:
- Un análisis de **una sola vez** (copio números en PowerPoint)
- Un análisis **reproducible** (ejecuta el notebook, el reporte se actualiza)

Para llegar al segundo nivel, el código debe ser:
1. **Parametrizable** — no valores hardcodeados como `"Bogota"` sino variables.
2. **Modular** — funciones para cada paso, fáciles de modificar.
3. **Documentado** — comentarios que explican *por qué*, no solo *qué*.
"""),

code(r"""
# Ejemplo: función que genera el resumen ejecutivo para cualquier ciudad
def perfil_ciudad(df, ciudad):
    """Devuelve un dict con el perfil completo de una ciudad."""
    sub = df[df["ciudad"] == ciudad]
    if sub.empty:
        return None
    return {
        "ciudad": ciudad,
        "n_transacciones": len(sub),
        "total_ventas": sub["monto"].sum(),
        "ticket_promedio": sub["monto"].mean(),
        "ticket_mediano": sub["monto"].median(),
        "categoria_top": sub.groupby("categoria")["monto"].sum().idxmax(),
        "metodo_top": sub["metodo_pago"].value_counts().idxmax(),
        "pct_outliers": sub["es_outlier"].mean() * 100,
    }

for ciudad in sorted(df["ciudad"].unique()):
    p = perfil_ciudad(df, ciudad)
    print(f"\n--- {p['ciudad']} ---")
    print(f"  Transacciones: {p['n_transacciones']}")
    print(f"  Total:         ${p['total_ventas']:,.0f}")
    print(f"  Ticket medio:  ${p['ticket_promedio']:,.0f}")
    print(f"  Categoria top: {p['categoria_top']}")
    print(f"  Metodo top:    {p['metodo_top']}")
"""),
]

# Insertar los bloques extra en posiciones estratégicas
C = insertar_despues(C, "cuándo pasó?", EXTRA_PIPELINE_REAL)
C = insertar_despues(C, "Decisiones que debes documentar", EXTRA_BOXPLOT)
C = insertar_despues(C, "monto_norm", EXTRA_ZSCORE)
C = insertar_despues(C, "Tabla de decisiones de limpieza", EXTRA_MERGE)
C = insertar_despues(C, "Total por ciudad", EXTRA_COHORTS)
C = insertar_despues(C, "Resumen del curso", EXTRA_REPORTE)


# --------------------------------------------------------------------------- #
ruta = os.path.join(os.path.dirname(__file__), "..", "curso", "clase08", "lecture.ipynb")
build(os.path.abspath(ruta), C)

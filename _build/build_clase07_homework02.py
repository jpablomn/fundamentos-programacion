"""Construye curso/clase07/homework02.ipynb — mini proyecto: reporte EDA automatizado.

Proyecto: dado un DataFrame cualquiera, generar un reporte EDA completo con:
- perfilado
- estadísticas
- detección de outliers
- visualización de distribuciones (guardada como imagen)

Las funciones se construyen parte a parte y la última las integra todas.
compartir_ns=True porque cada parte usa funciones de la anterior.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "perfil_dataset(df)",
        "enunciado": (
            "Implementa `perfil_dataset(df)` que reciba cualquier DataFrame y "
            "devuelva un **diccionario** con:\n\n"
            "- `'filas'`: número de filas\n"
            "- `'columnas'`: número de columnas\n"
            "- `'duplicados'`: número de filas duplicadas\n"
            "- `'nulos_total'`: total de valores nulos en todo el DataFrame\n"
            "- `'nulos_por_columna'`: dict `{columna: n_nulos}` solo para columnas con nulos\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "import pandas as pd, numpy as np\n"
            "df = pd.DataFrame({'a': [1, np.nan, 1], 'b': ['x', 'y', 'x']})\n"
            "r = perfil_dataset(df)\n"
            "# r['filas'] == 3, r['columnas'] == 2, r['nulos_total'] == 1\n"
            "# r['nulos_por_columna'] == {'a': 1}\n"
            "# r['duplicados'] == 1 (la fila 0 y la fila 2 son iguales)\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def perfil_dataset(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import numpy as np\nimport pandas as pd\n\n"
            "def perfil_dataset(df):\n"
            "    nulos = df.isnull().sum()\n"
            "    nulos_por_col = nulos[nulos > 0].to_dict()\n"
            "    return {\n"
            "        'filas':            len(df),\n"
            "        'columnas':         len(df.columns),\n"
            "        'duplicados':       int(df.duplicated().sum()),\n"
            "        'nulos_total':      int(df.isnull().sum().sum()),\n"
            "        'nulos_por_columna': nulos_por_col,\n"
            "    }"
        ),
        "visibles": [
            "import numpy as np, pandas as pd",
            "_df = pd.DataFrame({'a': [1.0, np.nan, 1.0], 'b': ['x', 'y', 'x']})",
            "_r = perfil_dataset(_df)",
            "assert _r['filas'] == 3",
            "assert _r['columnas'] == 2",
            "assert _r['nulos_total'] == 1",
            "assert _r['nulos_por_columna'] == {'a': 1}",
        ],
        "ocultos": [
            "_df2 = pd.DataFrame({'x': [1, 1, 2], 'y': [3, 3, 4]})",
            "_r2 = perfil_dataset(_df2)",
            "assert _r2['duplicados'] == 1",
            "assert _r2['nulos_total'] == 0",
            "assert _r2['nulos_por_columna'] == {}",
        ],
    },
    {
        "n": 2,
        "titulo": "estadisticas_numericas(df)",
        "enunciado": (
            "Implementa `estadisticas_numericas(df)` que devuelva un **DataFrame** "
            "con una fila por columna numérica y las siguientes columnas:\n"
            "`media`, `mediana`, `std`, `minimo`, `maximo`, `skewness`.\n\n"
            "Usa `round(2)` en todo el DataFrame resultado.\n\n"
            "**Ejemplo:** para un DataFrame con columnas `monto` e `id`, "
            "el resultado tendrá índice `['monto', 'id']` y columnas "
            "`['media', 'mediana', 'std', 'minimo', 'maximo', 'skewness']`."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def estadisticas_numericas(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def estadisticas_numericas(df):\n"
            "    num = df.select_dtypes(include='number')\n"
            "    resultado = pd.DataFrame({\n"
            "        'media':    num.mean(),\n"
            "        'mediana':  num.median(),\n"
            "        'std':      num.std(),\n"
            "        'minimo':   num.min(),\n"
            "        'maximo':   num.max(),\n"
            "        'skewness': num.skew(),\n"
            "    })\n"
            "    return resultado.round(2)"
        ),
        "visibles": [
            "import pandas as pd",
            "_df = pd.DataFrame({'x': [1.0, 2.0, 3.0], 'y': [10.0, 20.0, 30.0], 'z': ['a','b','c']})",
            "_r = estadisticas_numericas(_df)",
            "assert isinstance(_r, pd.DataFrame)",
            "assert 'media' in _r.columns and 'skewness' in _r.columns",
            "assert set(_r.index) == {'x', 'y'}",
        ],
        "ocultos": [
            "assert abs(_r.loc['x', 'media'] - 2.0) < 1e-3",
            "assert abs(_r.loc['y', 'mediana'] - 20.0) < 1e-3",
            "_df2 = pd.DataFrame({'a': [1.0, 1.0, 1.0]})",
            "_r2 = estadisticas_numericas(_df2)",
            "assert _r2.loc['a', 'minimo'] == _r2.loc['a', 'maximo']",
        ],
    },
    {
        "n": 3,
        "titulo": "reporte_outliers(df)",
        "enunciado": (
            "Implementa `reporte_outliers(df)` que devuelva un **diccionario** donde "
            "cada clave es el nombre de una columna numérica y el valor es un "
            "sub-diccionario con:\n\n"
            "- `'n_outliers'`: cantidad de outliers por IQR\n"
            "- `'pct_outliers'`: porcentaje (redondeado a 2 decimales)\n"
            "- `'lim_inf'`: límite inferior IQR\n"
            "- `'lim_sup'`: límite superior IQR\n\n"
            "Solo incluye columnas numéricas."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def reporte_outliers(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def reporte_outliers(df):\n"
            "    resultado = {}\n"
            "    for col in df.select_dtypes(include='number').columns:\n"
            "        s = df[col].dropna()\n"
            "        q1 = s.quantile(0.25)\n"
            "        q3 = s.quantile(0.75)\n"
            "        iqr = q3 - q1\n"
            "        lim_inf = q1 - 1.5 * iqr\n"
            "        lim_sup = q3 + 1.5 * iqr\n"
            "        n_out = int(((s < lim_inf) | (s > lim_sup)).sum())\n"
            "        resultado[col] = {\n"
            "            'n_outliers':   n_out,\n"
            "            'pct_outliers': round(100 * n_out / len(s), 2),\n"
            "            'lim_inf':      round(lim_inf, 2),\n"
            "            'lim_sup':      round(lim_sup, 2),\n"
            "        }\n"
            "    return resultado"
        ),
        "visibles": [
            "import pandas as pd",
            "_df = pd.DataFrame({'monto': [10.0, 11.0, 12.0, 10.0, 11.0, 500.0]})",
            "_r = reporte_outliers(_df)",
            "assert 'monto' in _r",
            "assert _r['monto']['n_outliers'] == 1",
            "assert _r['monto']['pct_outliers'] > 0",
        ],
        "ocultos": [
            "_df2 = pd.DataFrame({'a': [1.0,2.0,3.0,4.0,5.0], 'b': ['x','y','z','w','v']})",
            "_r2 = reporte_outliers(_df2)",
            "assert 'b' not in _r2",
            "assert _r2['a']['n_outliers'] == 0",
        ],
    },
    {
        "n": 4,
        "titulo": "guardar_histogramas(df, ruta_imagen)",
        "enunciado": (
            "Implementa `guardar_histogramas(df, ruta_imagen)` que cree una figura "
            "con **un histograma por cada columna numérica** (en una sola figura con "
            "subplots en una fila) y la guarde en `ruta_imagen` usando "
            "`plt.savefig(ruta_imagen, bbox_inches='tight')`.\n\n"
            "- Usa `figsize=(5 * n_cols, 4)` donde `n_cols` es el número de columnas numéricas.\n"
            "- Cada subplot debe tener título con el nombre de la columna.\n"
            "- La función no devuelve nada, solo guarda la imagen.\n\n"
            "**Pista:** usa `df.select_dtypes(include='number')` para obtener las columnas."
        ),
        "plantilla": (
            "import pandas as pd\nimport matplotlib.pyplot as plt\n\n"
            "def guardar_histogramas(df, ruta_imagen):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\nimport matplotlib.pyplot as plt\n\n"
            "def guardar_histogramas(df, ruta_imagen):\n"
            "    cols = df.select_dtypes(include='number').columns.tolist()\n"
            "    n = len(cols)\n"
            "    if n == 0:\n"
            "        return\n"
            "    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))\n"
            "    if n == 1:\n"
            "        axes = [axes]\n"
            "    for ax, col in zip(axes, cols):\n"
            "        ax.hist(df[col].dropna(), bins=20, color='#4C72B0',\n"
            "                edgecolor='white', alpha=0.85)\n"
            "        ax.set_title(col)\n"
            "        ax.set_xlabel(col)\n"
            "        ax.set_ylabel('Frecuencia')\n"
            "    plt.tight_layout()\n"
            "    plt.savefig(ruta_imagen, bbox_inches='tight')\n"
            "    plt.close()"
        ),
        "visibles": [
            "import pandas as pd, os",
            "_df = pd.DataFrame({'monto': [100.0,200.0,300.0,150.0,250.0], 'id': [1,2,3,4,5]})",
            "_ruta = '/tmp/test_histogramas_c7hw2.png'",
            "guardar_histogramas(_df, _ruta)",
            "assert os.path.exists(_ruta), 'La imagen no fue creada en la ruta esperada'",
        ],
        "ocultos": [
            "import os",
            "_df2 = pd.DataFrame({'cat': ['a','b','c'], 'val': [1.0, 2.0, 3.0]})",
            "_ruta2 = '/tmp/test_hist2_c7hw2.png'",
            "guardar_histogramas(_df2, _ruta2)",
            "assert os.path.exists(_ruta2)",
        ],
    },
    {
        "n": 5,
        "titulo": "resumen_categoricas(df)",
        "enunciado": (
            "Implementa `resumen_categoricas(df)` que devuelva un **diccionario** donde "
            "cada clave es el nombre de una columna **no numérica** (object o category) "
            "y el valor es un sub-diccionario con:\n\n"
            "- `'n_categorias'`: número de valores únicos\n"
            "- `'categoria_mas_frecuente'`: el valor más común\n"
            "- `'pct_mas_frecuente'`: su porcentaje (redondeado a 2 decimales)\n\n"
            "**Ejemplo:** para `metodo_pago` con 3 valores donde 'efectivo' aparece el 40%,\n"
            "devuelve `{'n_categorias': 3, 'categoria_mas_frecuente': 'efectivo', 'pct_mas_frecuente': 40.0}`."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def resumen_categoricas(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def resumen_categoricas(df):\n"
            "    resultado = {}\n"
            "    for col in df.select_dtypes(include=['object', 'category']).columns:\n"
            "        vc = df[col].value_counts(normalize=True)\n"
            "        resultado[col] = {\n"
            "            'n_categorias':           df[col].nunique(),\n"
            "            'categoria_mas_frecuente': vc.index[0],\n"
            "            'pct_mas_frecuente':       round(vc.iloc[0] * 100, 2),\n"
            "        }\n"
            "    return resultado"
        ),
        "visibles": [
            "import pandas as pd",
            "_df = pd.DataFrame({'ciudad': ['Bogota','Bogota','Cali','Bogota'], 'monto': [1.0,2.0,3.0,4.0]})",
            "_r = resumen_categoricas(_df)",
            "assert 'ciudad' in _r",
            "assert 'monto' not in _r",
            "assert _r['ciudad']['n_categorias'] == 2",
            "assert _r['ciudad']['categoria_mas_frecuente'] == 'Bogota'",
        ],
        "ocultos": [
            "assert abs(_r['ciudad']['pct_mas_frecuente'] - 75.0) < 0.1",
            "_df2 = pd.DataFrame({'a': [1.0, 2.0]})",
            "assert resumen_categoricas(_df2) == {}",
        ],
    },
    {
        "n": 6,
        "titulo": "reporte_eda(df, ruta_imagen)",
        "enunciado": (
            "¡La pieza final! Implementa `reporte_eda(df, ruta_imagen)` que integre "
            "todas las funciones anteriores y devuelva un **diccionario** con el "
            "reporte completo:\n\n"
            "```python\n"
            "{\n"
            "    'perfil':        perfil_dataset(df),\n"
            "    'estadisticas':  estadisticas_numericas(df),\n"
            "    'outliers':      reporte_outliers(df),\n"
            "    'categoricas':   resumen_categoricas(df),\n"
            "    'imagen_guardada': ruta_imagen,\n"
            "}\n"
            "```\n\n"
            "Además, llama a `guardar_histogramas(df, ruta_imagen)` para guardar la imagen.\n\n"
            "Esta función demuestra el poder de la **descomposición**: ya tienes todas "
            "las piezas; solo las ensamblas."
        ),
        "plantilla": (
            "def reporte_eda(df, ruta_imagen):\n"
            "    # ✏️ TU CÓDIGO AQUÍ (usa perfil_dataset, estadisticas_numericas,\n"
            "    #   reporte_outliers, resumen_categoricas, guardar_histogramas)\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "def reporte_eda(df, ruta_imagen):\n"
            "    guardar_histogramas(df, ruta_imagen)\n"
            "    return {\n"
            "        'perfil':          perfil_dataset(df),\n"
            "        'estadisticas':    estadisticas_numericas(df),\n"
            "        'outliers':        reporte_outliers(df),\n"
            "        'categoricas':     resumen_categoricas(df),\n"
            "        'imagen_guardada': ruta_imagen,\n"
            "    }"
        ),
        "visibles": [
            "import pandas as pd, os",
            "_df = pd.DataFrame({"
            "'ciudad': ['Bogota','Cali','Bogota','Medellin'], "
            "'monto': [100.0, 200.0, 150.0, 500.0]})",
            "_ruta = '/tmp/reporte_eda_c7hw2.png'",
            "_r = reporte_eda(_df, _ruta)",
            "assert 'perfil' in _r",
            "assert 'estadisticas' in _r",
            "assert 'outliers' in _r",
            "assert 'categoricas' in _r",
            "assert os.path.exists(_ruta)",
        ],
        "ocultos": [
            "assert _r['perfil']['filas'] == 4",
            "assert _r['imagen_guardada'] == _ruta",
            "assert 'ciudad' in _r['categoricas']",
            "assert 'monto' in _r['outliers']",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 7 · Tarea 02 — Mini proyecto: reporte EDA automatizado

### EDA y transformación de datos

En esta tarea construirás, parte por parte, un **generador automático de reportes EDA**.
Dado cualquier DataFrame, tu sistema producirá:
- Un perfil completo (forma, nulos, duplicados).
- Estadísticas descriptivas de todas las columnas numéricas.
- Un reporte de outliers por columna.
- Un resumen de las variables categóricas.
- Una imagen con histogramas de todas las variables numéricas.

```
  DataFrame de entrada
        │
        ▼
  perfil_dataset      estadisticas_numericas
        │                      │
        ▼                      ▼
  reporte_outliers   resumen_categoricas   guardar_histogramas
        │                      │                    │
        └──────────────────────┴────────────────────┘
                               │
                               ▼
                         reporte_eda (integrador)
```

**Instrucciones**

1. Implementa cada función **en orden**: la Parte 6 usa todas las anteriores.
2. No cambies nombres ni parámetros.
3. Ejecuta los tests tras cada función.

> Las funciones se llaman entre sí (compartir_ns=True), así que el namespace
> es compartido: una vez definida `perfil_dataset`, está disponible para `reporte_eda`.
""",
    "cierre_md": r"""
---
## ¡Proyecto terminado!

Si todos los tests pasan, construiste un generador de reportes EDA reutilizable.

| Parte | Patrón / concepto |
|---|---|
| 1 perfil_dataset | diagnóstico inicial (shape, nulos, duplicados) |
| 2 estadisticas_numericas | agregación con pandas (mean, median, std, skew) |
| 3 reporte_outliers | método IQR aplicado a todas las numéricas |
| 4 guardar_histogramas | visualización programática con matplotlib |
| 5 resumen_categoricas | frecuencias y cardinalidad de categóricas |
| 6 reporte_eda | **integración** (descomposición en subproblemas) |

### Reto opcional (sin calificar)

- Añade a `reporte_eda` una clave `'correlaciones'` con la matriz de correlación
  como DataFrame.
- Extiende `guardar_histogramas` para que también guarde un heatmap de correlaciones
  en la misma figura.
- Prueba tu `reporte_eda` sobre el dataset de transacciones completo:
  `pd.read_csv('../datasets/transacciones.csv')`.

> En producción, herramientas como `ydata-profiling` (antes pandas-profiling)
> hacen exactamente esto — pero ahora entiendes cada pieza que las compone.
""",
}

validar(ejercicios, compartir_ns=True)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase07", "homework02.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase07_homework02_solved.ipynb"),
)

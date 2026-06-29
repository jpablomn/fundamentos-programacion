"""Construye curso/clase06/homework02.ipynb — mini proyecto: reporte ejecutivo de ventas.

Proyecto: construir un DataFrame de resumen por ciudad con métricas clave y exportarlo.
Los ejercicios se apoyan entre sí (compartir_ns=True).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    # ---- 1 ---------------------------------------------------------------- #
    {
        "n": 1,
        "titulo": "Cargar y validar el dataset",
        "enunciado": (
            "Implementa `cargar_dataset(ruta)` que:\n"
            "1. Lea el CSV desde `ruta` con `pd.read_csv`, parseando la columna\n"
            "   `'fecha'` como datetime.\n"
            "2. Verifique que las columnas esperadas existen:\n"
            "   `['id', 'fecha', 'ciudad', 'categoria', 'metodo_pago', 'monto']`.\n"
            "3. Devuelva el DataFrame si todo está bien.\n"
            "4. Lanza `ValueError('columnas faltantes')` si falta alguna columna.\n\n"
            "**Esta función es la base del proyecto**: las siguientes la usan."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def cargar_dataset(ruta):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def cargar_dataset(ruta):\n"
            "    df = pd.read_csv(ruta, parse_dates=['fecha'])\n"
            "    esperadas = ['id', 'fecha', 'ciudad', 'categoria', 'metodo_pago', 'monto']\n"
            "    faltantes = [c for c in esperadas if c not in df.columns]\n"
            "    if faltantes:\n"
            "        raise ValueError('columnas faltantes')\n"
            "    return df"
        ),
        "visibles": [
            "import os",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = cargar_dataset(ruta)",
            "assert _df.shape[0] == 120",
            "assert _df.shape[1] == 6",
            "assert str(_df['fecha'].dtype).startswith('datetime')",
        ],
        "ocultos": [
            "import tempfile, os, pandas as pd",
            "_df_malo = _df.drop(columns=['monto'])",
            "_ruta_mala = tempfile.mktemp(suffix='.csv')",
            "_df_malo.to_csv(_ruta_mala, index=False)",
            "_raised = False",
            "try: cargar_dataset(_ruta_mala)",
            "except ValueError: _raised = True",
            "assert _raised, 'debio lanzar ValueError'",
            "os.unlink(_ruta_mala)",
        ],
    },
    # ---- 2 ---------------------------------------------------------------- #
    {
        "n": 2,
        "titulo": "Calcular métricas por ciudad",
        "enunciado": (
            "Implementa `metricas_ciudad(df)` que reciba el DataFrame (devuelto\n"
            "por `cargar_dataset`) y devuelva un **DataFrame** con una fila por ciudad\n"
            "y las siguientes columnas:\n"
            "- `'ciudad'`\n"
            "- `'n_transacciones'`: número de transacciones\n"
            "- `'total'`: suma de montos\n"
            "- `'promedio'`: promedio de monto (float)\n"
            "- `'maximo'`: monto máximo\n\n"
            "Ordenado de mayor a menor por `'total'`.\n\n"
            "**Usa `cargar_dataset` para obtener el DataFrame en tus tests.**"
        ),
        "plantilla": (
            "def metricas_ciudad(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def metricas_ciudad(df):\n"
            "    return (\n"
            "        df.groupby('ciudad')['monto']\n"
            "          .agg(\n"
            "              n_transacciones='count',\n"
            "              total='sum',\n"
            "              promedio='mean',\n"
            "              maximo='max'\n"
            "          )\n"
            "          .reset_index()\n"
            "          .sort_values('total', ascending=False)\n"
            "          .reset_index(drop=True)\n"
            "    )"
        ),
        "visibles": [
            "import os",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = cargar_dataset(ruta)",
            "_met = metricas_ciudad(_df)",
            "assert 'ciudad' in _met.columns",
            "assert 'n_transacciones' in _met.columns",
            "assert 'total' in _met.columns",
            "assert len(_met) == 5",
        ],
        "ocultos": [
            "assert _met.iloc[0]['total'] >= _met.iloc[-1]['total']",
            "assert _met['n_transacciones'].sum() == 120",
            "assert abs(_met['total'].sum() - _df['monto'].sum()) < 1",
        ],
    },
    # ---- 3 ---------------------------------------------------------------- #
    {
        "n": 3,
        "titulo": "Agregar porcentaje del total",
        "enunciado": (
            "Implementa `agregar_porcentaje(metricas)` que reciba el DataFrame\n"
            "devuelto por `metricas_ciudad` y devuelva una **copia** con una columna\n"
            "adicional `'pct_total'`: el porcentaje de cada ciudad sobre el total\n"
            "global, redondeado a 2 decimales.\n\n"
            "**Ejemplo:** si el total global es 1000 y Bogota tiene 250,\n"
            "`pct_total` de Bogota = 25.0"
        ),
        "plantilla": (
            "def agregar_porcentaje(metricas):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def agregar_porcentaje(metricas):\n"
            "    copia = metricas.copy()\n"
            "    total_global = copia['total'].sum()\n"
            "    copia['pct_total'] = (copia['total'] / total_global * 100).round(2)\n"
            "    return copia"
        ),
        "visibles": [
            "import os",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = cargar_dataset(ruta)",
            "_met = metricas_ciudad(_df)",
            "_met_pct = agregar_porcentaje(_met)",
            "assert 'pct_total' in _met_pct.columns",
            "assert abs(_met_pct['pct_total'].sum() - 100.0) < 0.1",
        ],
        "ocultos": [
            "assert 'pct_total' not in _met.columns",
            "assert (_met_pct['pct_total'] > 0).all()",
        ],
    },
    # ---- 4 ---------------------------------------------------------------- #
    {
        "n": 4,
        "titulo": "Agregar la categoría más vendida por ciudad",
        "enunciado": (
            "Implementa `agregar_top_categoria(metricas, df)` que reciba el DataFrame\n"
            "de métricas y el DataFrame original, y devuelva una **copia** de metricas\n"
            "con una columna adicional `'top_categoria'`: el nombre de la categoría\n"
            "con mayor suma de monto para cada ciudad.\n\n"
            "**Pista:** calcula un groupby por `['ciudad', 'categoria']`, toma el\n"
            "máximo por ciudad, y haz un merge con metricas."
        ),
        "plantilla": (
            "def agregar_top_categoria(metricas, df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def agregar_top_categoria(metricas, df):\n"
            "    por_ciudad_cat = (\n"
            "        df.groupby(['ciudad', 'categoria'])['monto']\n"
            "          .sum()\n"
            "          .reset_index()\n"
            "    )\n"
            "    idx = por_ciudad_cat.groupby('ciudad')['monto'].idxmax()\n"
            "    top_cat = por_ciudad_cat.loc[idx, ['ciudad', 'categoria']].rename(\n"
            "        columns={'categoria': 'top_categoria'}\n"
            "    )\n"
            "    return metricas.merge(top_cat, on='ciudad', how='left')"
        ),
        "visibles": [
            "import os",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = cargar_dataset(ruta)",
            "_met = metricas_ciudad(_df)",
            "_met_top = agregar_top_categoria(_met, _df)",
            "assert 'top_categoria' in _met_top.columns",
            "assert len(_met_top) == 5",
            "assert _met_top['top_categoria'].notna().all()",
        ],
        "ocultos": [
            "cats_validas = _df['categoria'].unique().tolist()",
            "assert _met_top['top_categoria'].isin(cats_validas).all()",
        ],
    },
    # ---- 5 ---------------------------------------------------------------- #
    {
        "n": 5,
        "titulo": "Construir el reporte ejecutivo completo",
        "enunciado": (
            "Implementa `reporte_ejecutivo(df)` que **integre** las funciones\n"
            "anteriores para producir el DataFrame de reporte completo:\n\n"
            "1. Llama a `metricas_ciudad(df)` para obtener las métricas base.\n"
            "2. Llama a `agregar_porcentaje(metricas)` para agregar `pct_total`.\n"
            "3. Llama a `agregar_top_categoria(metricas, df)` para agregar `top_categoria`.\n"
            "4. Devuelve el DataFrame final con columnas:\n"
            "   `ciudad, n_transacciones, total, promedio, maximo, pct_total, top_categoria`\n\n"
            "Este es el patrón de **integración**: ensamblar piezas que ya funcionan."
        ),
        "plantilla": (
            "def reporte_ejecutivo(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ (usa metricas_ciudad, agregar_porcentaje, agregar_top_categoria)\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def reporte_ejecutivo(df):\n"
            "    met = metricas_ciudad(df)\n"
            "    met = agregar_porcentaje(met)\n"
            "    met = agregar_top_categoria(met, df)\n"
            "    return met"
        ),
        "visibles": [
            "import os",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = cargar_dataset(ruta)",
            "_rep = reporte_ejecutivo(_df)",
            "assert 'ciudad' in _rep.columns",
            "assert 'pct_total' in _rep.columns",
            "assert 'top_categoria' in _rep.columns",
            "assert len(_rep) == 5",
        ],
        "ocultos": [
            "assert abs(_rep['pct_total'].sum() - 100.0) < 0.1",
            "assert _rep['n_transacciones'].sum() == 120",
            "assert _rep.iloc[0]['total'] >= _rep.iloc[-1]['total']",
        ],
    },
    # ---- 6 ---------------------------------------------------------------- #
    {
        "n": 6,
        "titulo": "Exportar el reporte a CSV",
        "enunciado": (
            "Implementa `exportar_reporte(df, ruta_salida)` que:\n"
            "1. Genere el reporte ejecutivo usando `reporte_ejecutivo(df)`.\n"
            "2. Redondee `promedio` a 2 decimales.\n"
            "3. Exporte el resultado a `ruta_salida` como CSV (sin índice).\n"
            "4. Imprima un mensaje: `'Reporte exportado: N ciudades'` donde N es el\n"
            "   número de filas.\n"
            "5. Devuelva el DataFrame exportado.\n\n"
            "**Esta es la pieza final del proyecto**: produce el entregable."
        ),
        "plantilla": (
            "def exportar_reporte(df, ruta_salida):\n"
            "    # ✏️ TU CÓDIGO AQUÍ (usa reporte_ejecutivo)\n"
            "    {NI}"
        ).format(NI=NI),
        "solucion": (
            "def exportar_reporte(df, ruta_salida):\n"
            "    rep = reporte_ejecutivo(df)\n"
            "    rep['promedio'] = rep['promedio'].round(2)\n"
            "    rep.to_csv(ruta_salida, index=False)\n"
            "    print('Reporte exportado: {} ciudades'.format(len(rep)))\n"
            "    return rep"
        ),
        "visibles": [
            "import os, tempfile, pandas as pd",
            "ruta = os.path.join('..', 'datasets', 'transacciones.csv')",
            "_df = cargar_dataset(ruta)",
            "_ruta_out = tempfile.mktemp(suffix='.csv')",
            "_rep = exportar_reporte(_df, _ruta_out)",
            "assert _rep is not None",
            "assert len(_rep) == 5",
        ],
        "ocultos": [
            "_leido = pd.read_csv(_ruta_out)",
            "assert len(_leido) == 5",
            "assert 'pct_total' in _leido.columns",
            "assert 'top_categoria' in _leido.columns",
            "os.unlink(_ruta_out)",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 6 · Tarea 02 — Mini proyecto: reporte ejecutivo de ventas

### pandas aplicado a un caso de negocio real

En esta tarea construirás, **pieza por pieza**, un sistema de reporte de ventas.
Dado el dataset de transacciones, producirás un DataFrame resumen exportable
a CSV, listo para entregar a un equipo directivo.

```
  transacciones.csv
         │
         ▼
  cargar_dataset()          ← validación y carga
         │
         ▼
  metricas_ciudad()         ← groupby + agregaciones
         │
         ▼
  agregar_porcentaje()      ← cálculo de pct_total
         │
         ▼
  agregar_top_categoria()   ← join con categoría dominante
         │
         ▼
  reporte_ejecutivo()       ← integración de todo
         │
         ▼
  exportar_reporte()        ← CSV listo para entregar
```

**Instrucciones**

1. Implementa cada función reemplazando `raise NotImplementedError`.
2. **Sigue el orden**: cada parte usa las anteriores.
3. **No cambies nombres ni parámetros**.
4. Ejecuta los tests de cada parte hasta ver ✅.

> 🧠 Este es el patrón de **descomposición**: el problema grande (reporte de ventas)
> se divide en subproblemas pequeños que ya sabemos resolver.
""",
    "cierre_md": r"""
---
## ¡Proyecto terminado!

Si todos los tests pasan, has construido un pipeline completo de análisis:

| Parte | Concepto pandas |
|---|---|
| 1 Cargar y validar | `pd.read_csv` + validación de columnas |
| 2 Métricas por ciudad | `groupby` + `agg` múltiple |
| 3 Porcentaje del total | operación vectorizada sobre columna |
| 4 Top categoría | `groupby` anidado + `idxmax` + `merge` |
| 5 Reporte ejecutivo | **integración** de funciones anteriores |
| 6 Exportar a CSV | `to_csv` + retorno del DataFrame |

### Reto opcional (sin calificar)

- Añade una columna `'metodo_pago_principal'`: el método de pago más usado
  por ciudad (similar a `top_categoria` pero para `metodo_pago`).
- Modifica `exportar_reporte` para que también exporte un segundo CSV con el
  resumen por categoría.
- ¿Cómo añadirías una fila "TOTAL" al final del reporte con las sumas globales?

> 💡 Este tipo de pipeline —carga → transformación → agregación → exportación—
> es el corazón de cualquier proyecto ETL (Extract, Transform, Load) en
> ingeniería de datos.
""",
}

# Cambiamos al directorio de un notebook para que los paths relativos funcionen
_orig_dir = os.getcwd()
_notebook_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "curso", "clase06")
os.chdir(os.path.abspath(_notebook_dir))
try:
    validar(ejercicios, compartir_ns=True)
finally:
    os.chdir(_orig_dir)

construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase06", "homework02.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase06_homework02_solved.ipynb"),
)

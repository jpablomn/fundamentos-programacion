"""Construye curso/clase05/homework02.ipynb — mini proyecto: simulación financiera.

Proyecto: "Simulación financiera con NumPy".
El estudiante genera retornos diarios con distribución normal, calcula
retorno acumulado, drawdown máximo y Sharpe ratio. Los ejercicios se construyen
uno sobre otro (compartir_ns=True).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Generar retornos diarios",
        "enunciado": (
            "El primer paso de la simulación es generar `n` retornos diarios de un\n"
            "activo financiero. Los retornos se modelan como distribución normal con\n"
            "media `mu` (rendimiento diario esperado) y desviación `sigma` (volatilidad).\n\n"
            "Implementa `generar_retornos(n, mu, sigma, seed)` que:\n"
            "1. Use `np.random.default_rng(seed)` para reproducibilidad.\n"
            "2. Genere `n` retornos con `rng.normal(loc=mu, scale=sigma, size=n)`.\n"
            "3. Devuelva el array de retornos.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "r = generar_retornos(252, mu=0.001, sigma=0.02, seed=42)\n"
            "# 252 retornos diarios (un año bursátil)\n"
            "# media ≈ 0.001, std ≈ 0.02\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def generar_retornos(n, mu=0.001, sigma=0.02, seed=42):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def generar_retornos(n, mu=0.001, sigma=0.02, seed=42):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    return rng.normal(loc=mu, scale=sigma, size=n)"
        ),
        "visibles": [
            "import numpy as np",
            "r = generar_retornos(252, mu=0.001, sigma=0.02, seed=42)",
            "assert isinstance(r, np.ndarray)",
            "assert len(r) == 252",
            "assert abs(r.mean() - 0.001) < 0.005",  # within 5 sigma for n=252
            "assert abs(r.std() - 0.02) < 0.005",
        ],
        "ocultos": [
            "import numpy as np",
            "# Reproducibilidad: misma semilla, mismo resultado",
            "r1 = generar_retornos(100, seed=0)",
            "r2 = generar_retornos(100, seed=0)",
            "assert np.array_equal(r1, r2)",
            "# Semillas distintas dan resultados distintos",
            "r3 = generar_retornos(100, seed=1)",
            "assert not np.array_equal(r1, r3)",
        ],
    },
    {
        "n": 2,
        "titulo": "Retorno acumulado",
        "enunciado": (
            "Dado un array de retornos diarios, el **retorno acumulado** en el\n"
            "día `t` es el producto de `(1 + r[i])` para `i` desde 0 hasta t.\n\n"
            "Implementa `retorno_acumulado(retornos)` que:\n"
            "1. Calcule el producto acumulado de `(1 + retornos)`.\n"
            "2. Devuelva un array de la misma longitud donde cada elemento es\n"
            "   el valor de la cartera (empezando desde 1.0).\n\n"
            "Usa `np.cumprod`.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "r = np.array([0.05, -0.02, 0.03])\n"
            "retorno_acumulado(r)\n"
            "# → array([1.05, 1.029, 1.05987])\n"
            "# dia 0: 1 * 1.05 = 1.05\n"
            "# dia 1: 1.05 * 0.98 = 1.029\n"
            "# dia 2: 1.029 * 1.03 = 1.05987\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def retorno_acumulado(retornos):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa np.cumprod\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def retorno_acumulado(retornos):\n"
            "    return np.cumprod(1 + retornos)"
        ),
        "visibles": [
            "import numpy as np",
            "r = np.array([0.05, -0.02, 0.03])",
            "ac = retorno_acumulado(r)",
            "assert len(ac) == 3",
            "assert abs(ac[0] - 1.05) < 1e-9",
            "assert abs(ac[1] - 1.05 * 0.98) < 1e-9",
        ],
        "ocultos": [
            "import numpy as np",
            "# Con retornos cero: la cartera no cambia",
            "assert np.allclose(retorno_acumulado(np.zeros(5)), np.ones(5))",
            "# Verificar que el ultimo valor es el producto total de (1+r)",
            "_r = generar_retornos(252, seed=42)",
            "_ac = retorno_acumulado(_r)",
            "assert abs(_ac[-1] - np.prod(1 + _r)) < 1e-9",
        ],
    },
    {
        "n": 3,
        "titulo": "Drawdown máximo",
        "enunciado": (
            "El **drawdown** en un día `t` es la caída relativa desde el máximo\n"
            "histórico hasta ese día:\n\n"
            "```\n"
            "drawdown[t] = (maximo_historico[t] - valor[t]) / maximo_historico[t]\n"
            "```\n\n"
            "El **drawdown máximo** es el mayor drawdown de toda la serie.\n\n"
            "Implementa `drawdown_maximo(acumulado)` que:\n"
            "1. Calcule el máximo histórico en cada día: `np.maximum.accumulate`.\n"
            "2. Calcule el drawdown en cada día.\n"
            "3. Devuelva el drawdown máximo (valor escalar).\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "ac = np.array([1.0, 1.1, 0.9, 1.05, 0.85, 1.2])\n"
            "drawdown_maximo(ac)  # → 0.2272... (caída de 1.1 a 0.85)\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def drawdown_maximo(acumulado):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa np.maximum.accumulate\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def drawdown_maximo(acumulado):\n"
            "    maximo_hist = np.maximum.accumulate(acumulado)\n"
            "    drawdowns = (maximo_hist - acumulado) / maximo_hist\n"
            "    return float(drawdowns.max())"
        ),
        "visibles": [
            "import numpy as np",
            "ac = np.array([1.0, 1.1, 0.9, 1.05, 0.85, 1.2])",
            "dd = drawdown_maximo(ac)",
            "assert abs(dd - (1.1 - 0.85) / 1.1) < 1e-9",
        ],
        "ocultos": [
            "import numpy as np",
            "# Si la cartera solo sube, el drawdown es 0",
            "subida = np.array([1.0, 1.1, 1.2, 1.3])",
            "assert drawdown_maximo(subida) == 0.0",
            "# Verificar usando retornos generados",
            "_r = generar_retornos(252, seed=42)",
            "_ac = retorno_acumulado(_r)",
            "_dd = drawdown_maximo(_ac)",
            "assert 0.0 <= _dd < 1.0",
        ],
    },
    {
        "n": 4,
        "titulo": "Sharpe Ratio aproximado",
        "enunciado": (
            "El **Sharpe Ratio** mide el rendimiento ajustado por riesgo:\n\n"
            "```\n"
            "sharpe = (media_retornos - tasa_libre_riesgo) / std_retornos\n"
            "         * sqrt(252)   ← anualizar (252 días bursátiles)\n"
            "```\n\n"
            "Implementa `sharpe_ratio(retornos, tasa_libre=0.0)` que:\n"
            "1. Calcule la media y desviación estándar del array de retornos.\n"
            "2. Aplique la fórmula y anualice multiplicando por `np.sqrt(252)`.\n"
            "3. Devuelva el Sharpe Ratio como float.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "r = np.array([0.01, 0.005, -0.003, 0.008])\n"
            "sharpe_ratio(r)  # → algún valor > 0 si media > 0\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def sharpe_ratio(retornos, tasa_libre=0.0):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def sharpe_ratio(retornos, tasa_libre=0.0):\n"
            "    exceso = retornos.mean() - tasa_libre\n"
            "    return float(exceso / retornos.std() * np.sqrt(252))"
        ),
        "visibles": [
            "import numpy as np",
            "r = np.array([0.01, 0.005, -0.003, 0.008])",
            "sr = sharpe_ratio(r)",
            "assert isinstance(sr, float)",
            "# Con media positiva y tasa libre 0, el Sharpe debe ser positivo",
            "assert sr > 0",
        ],
        "ocultos": [
            "import numpy as np",
            "# Retornos constantes: Sharpe indefinido (std=0), no lo testamos",
            "# Retornos negativos: Sharpe < 0",
            "_r_neg = np.full(100, -0.001)",
            "_r_neg = _r_neg + np.random.default_rng(5).normal(0, 0.0001, 100)",
            "# media negativa => sharpe negativo",
            "assert sharpe_ratio(_r_neg) < 0",
            "# Verificar formula manualmente",
            "_r2 = generar_retornos(252, mu=0.001, sigma=0.02, seed=42)",
            "_sr = sharpe_ratio(_r2)",
            "_expected = float((_r2.mean() - 0.0) / _r2.std() * np.sqrt(252))",
            "assert abs(_sr - _expected) < 1e-9",
        ],
    },
    {
        "n": 5,
        "titulo": "Simulación de múltiples carteras (Monte Carlo)",
        "enunciado": (
            "Implementa `simular_carteras(n_carteras, n_dias, mu, sigma, seed)` que:\n"
            "1. Genere una matriz `(n_carteras, n_dias)` de retornos usando\n"
            "   `rng.normal(mu, sigma, size=(n_carteras, n_dias))`.\n"
            "2. Calcule el retorno final de cada cartera (último valor del\n"
            "   retorno acumulado) usando `np.cumprod` con `axis=1`.\n"
            "3. Devuelva un array de `n_carteras` retornos finales.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "finales = simular_carteras(1000, 252, 0.001, 0.02, seed=0)\n"
            "# array de 1000 valores: retorno final de cada cartera simulada\n"
            "```\n\n"
            "Pista: `np.cumprod(1 + M, axis=1)[:, -1]` da el último valor de cada fila."
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def simular_carteras(n_carteras, n_dias, mu=0.001, sigma=0.02, seed=42):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def simular_carteras(n_carteras, n_dias, mu=0.001, sigma=0.02, seed=42):\n"
            "    rng = np.random.default_rng(seed)\n"
            "    retornos = rng.normal(mu, sigma, size=(n_carteras, n_dias))\n"
            "    acumulados = np.cumprod(1 + retornos, axis=1)\n"
            "    return acumulados[:, -1]"
        ),
        "visibles": [
            "import numpy as np",
            "finales = simular_carteras(1000, 252, seed=0)",
            "assert isinstance(finales, np.ndarray)",
            "assert len(finales) == 1000",
            "# Con mu=0.001 diario y 252 días, la media debe estar por encima de 1",
            "assert finales.mean() > 1.0",
        ],
        "ocultos": [
            "import numpy as np",
            "# Reproducibilidad",
            "f1 = simular_carteras(100, 50, seed=7)",
            "f2 = simular_carteras(100, 50, seed=7)",
            "assert np.array_equal(f1, f2)",
            "# Cada retorno final es > 0 (no puede ser negativo, la cartera no puede valer < 0)",
            "assert (finales > 0).all()",
        ],
    },
    {
        "n": 6,
        "titulo": "Análisis completo: reporte de riesgo",
        "enunciado": (
            "Integra las funciones anteriores en un reporte completo.\n\n"
            "Implementa `reporte_riesgo(n_dias, mu, sigma, seed)` que:\n"
            "1. Genere retornos con `generar_retornos`.\n"
            "2. Calcule el retorno acumulado con `retorno_acumulado`.\n"
            "3. Devuelva un diccionario con las siguientes métricas:\n"
            "   - `'retorno_total'`: retorno final - 1 (ganancia porcentual).\n"
            "   - `'drawdown_maximo'`: valor del drawdown máximo.\n"
            "   - `'sharpe_ratio'`: Sharpe ratio anualizado.\n"
            "   - `'volatilidad'`: desviación estándar de los retornos.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "r = reporte_riesgo(252, 0.001, 0.02, seed=42)\n"
            "# {'retorno_total': 0.xx, 'drawdown_maximo': 0.xx,\n"
            "#  'sharpe_ratio': 0.xx, 'volatilidad': 0.02x}\n"
            "```"
        ),
        "plantilla": (
            "import numpy as np\n\n"
            "def reporte_riesgo(n_dias=252, mu=0.001, sigma=0.02, seed=42):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa generar_retornos, retorno_acumulado,\n"
            "    # drawdown_maximo y sharpe_ratio\n"
            "    " + NI
        ),
        "solucion": (
            "import numpy as np\n\n"
            "def reporte_riesgo(n_dias=252, mu=0.001, sigma=0.02, seed=42):\n"
            "    retornos = generar_retornos(n_dias, mu, sigma, seed)\n"
            "    acumulado = retorno_acumulado(retornos)\n"
            "    return {\n"
            "        'retorno_total':   float(acumulado[-1] - 1),\n"
            "        'drawdown_maximo': drawdown_maximo(acumulado),\n"
            "        'sharpe_ratio':    sharpe_ratio(retornos),\n"
            "        'volatilidad':     float(retornos.std()),\n"
            "    }"
        ),
        "visibles": [
            "import numpy as np",
            "rep = reporte_riesgo(252, 0.001, 0.02, seed=42)",
            "assert set(rep.keys()) == {'retorno_total', 'drawdown_maximo', 'sharpe_ratio', 'volatilidad'}",
            "assert isinstance(rep['retorno_total'], float)",
            "assert 0.0 <= rep['drawdown_maximo'] < 1.0",
        ],
        "ocultos": [
            "import numpy as np",
            "# Verificar que las metricas son consistentes con las funciones individuales",
            "_r = generar_retornos(252, 0.001, 0.02, seed=42)",
            "_ac = retorno_acumulado(_r)",
            "_rep = reporte_riesgo(252, 0.001, 0.02, seed=42)",
            "assert abs(_rep['retorno_total'] - float(_ac[-1] - 1)) < 1e-9",
            "assert abs(_rep['drawdown_maximo'] - drawdown_maximo(_ac)) < 1e-9",
            "assert abs(_rep['sharpe_ratio'] - sharpe_ratio(_r)) < 1e-9",
            "assert abs(_rep['volatilidad'] - float(_r.std())) < 1e-9",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 5 · Tarea 02 — Mini proyecto: simulación financiera con NumPy

### Análisis cuantitativo de carteras de inversión

En este proyecto construirás, pieza por pieza, un simulador de carteras
financieras usando **exclusivamente NumPy**. Al final tendrás un reporte
completo de riesgo y rendimiento.

```
generar_retornos()
       │
       ▼
retorno_acumulado()
       │
       ├──▶ drawdown_maximo()
       │
       └──▶ sharpe_ratio()
                    │
                    ▼
             reporte_riesgo()   ← integra todo
```

**Instrucciones**

1. Implementa cada función reemplazando `raise NotImplementedError`.
2. **Resuélvelas en orden**: las partes 3-6 usan las anteriores.
3. **No cambies nombres ni parámetros**: las funciones se llaman entre sí.
4. Ejecuta los tests de cada parte hasta ver ✅.

> 🧠 Antes de programar cada función, dibuja el shape de entrada y salida.

| Parte | Función | Patrón NumPy |
|---|---|---|
| 1 | `generar_retornos` | `default_rng`, distribución normal |
| 2 | `retorno_acumulado` | `np.cumprod` |
| 3 | `drawdown_maximo` | `np.maximum.accumulate` |
| 4 | `sharpe_ratio` | reducción + escalar |
| 5 | `simular_carteras` | arrays 2-D, cumprod axis=1 |
| 6 | `reporte_riesgo` | integración |
""",
    "cierre_md": r"""
---
## ¡Proyecto terminado!

Si todos los tests pasan, construiste un simulador financiero funcional.

### Lo que aprendiste con este proyecto

- **`np.cumprod`** para acumular multiplicaciones (retornos compuestos).
- **`np.maximum.accumulate`** para calcular el máximo histórico de una serie.
- **Arrays 2-D** para simular múltiples escenarios en paralelo (sin bucles).
- **Composición de funciones** NumPy para construir análisis complejos.

### Reto opcional (sin calificar)

1. Usa `simular_carteras` para generar 10.000 carteras durante 252 días
   y calcula:
   - ¿Qué porcentaje termina con ganancia?
   - ¿Cuál es el percentil 5 del retorno final (VaR al 95%)?
   - Grafica el histograma de retornos finales con `matplotlib`.

2. ¿Cómo cambiaría el Sharpe Ratio si la tasa libre de riesgo fuera 0.04%
   diario (≈10% anual)? Modifica `sharpe_ratio` para incluirla.

> 💡 En finanzas cuantitativas, este tipo de simulación se usa para
> calcular el **Value at Risk (VaR)** y el **Expected Shortfall (ES)**,
> que son las métricas estándar de gestión de riesgo.
""",
}

validar(ejercicios, compartir_ns=True)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase05", "homework02.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase05_homework02_solved.ipynb"),
)

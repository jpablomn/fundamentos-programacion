"""Construye curso/clase02/homework01.ipynb — 8 ejercicios autocalificables.

Clase 2: Variables, tipos de datos, operadores y condicionales.
Contexto: finanzas, negocios, matemáticas aplicadas.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Días entre dos años",
        "enunciado": (
            "Implementa `dias_entre_anios(anio_inicio, anio_fin)` que devuelva el número "
            "total de días entre el 1 de enero de `anio_inicio` y el 1 de enero de `anio_fin`.\n\n"
            "**Sin librerías de fecha.** Usa aritmética: recorre cada año y suma 366 si es "
            "bisiesto, 365 si no.\n\n"
            "Un año es bisiesto si: `(anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)`.\n\n"
            "**Ejemplo:** `dias_entre_anios(2020, 2023)` → `1096`\n"
            "(2020 tiene 366 días + 2021 tiene 365 + 2022 tiene 365 = 1096)."
        ),
        "plantilla": "def dias_entre_anios(anio_inicio, anio_fin):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def dias_entre_anios(anio_inicio, anio_fin):\n"
            "    total = 0\n"
            "    for a in range(anio_inicio, anio_fin):\n"
            "        bisiesto = (a % 4 == 0 and a % 100 != 0) or (a % 400 == 0)\n"
            "        total += 366 if bisiesto else 365\n"
            "    return total"
        ),
        "visibles": [
            "assert dias_entre_anios(2020, 2023) == 1096",
            "assert dias_entre_anios(2023, 2024) == 365",
        ],
        "ocultos": [
            "assert dias_entre_anios(2000, 2001) == 366",   # 2000 es bisiesto
            "assert dias_entre_anios(1900, 1901) == 365",   # 1900 no es bisiesto
            "assert dias_entre_anios(2024, 2024) == 0",     # mismo año
        ],
    },
    {
        "n": 2,
        "titulo": "Tipo de triángulo",
        "enunciado": (
            "Implementa `tipo_triangulo(a, b, c)` que clasifique el triángulo según sus lados:\n"
            "- `'equilatero'` si los tres lados son iguales.\n"
            "- `'isosceles'` si exactamente dos lados son iguales.\n"
            "- `'escaleno'` si ningún lado es igual a otro.\n"
            "- `'invalido'` si los lados no forman un triángulo "
            "(la suma de dos lados cualquiera debe ser mayor al tercero).\n\n"
            "**Ejemplos:** `tipo_triangulo(5, 5, 5)` → `'equilatero'`; "
            "`tipo_triangulo(3, 3, 5)` → `'isosceles'`; "
            "`tipo_triangulo(3, 4, 5)` → `'escaleno'`; "
            "`tipo_triangulo(1, 2, 10)` → `'invalido'`."
        ),
        "plantilla": "def tipo_triangulo(a, b, c):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def tipo_triangulo(a, b, c):\n"
            "    if a + b <= c or a + c <= b or b + c <= a:\n"
            "        return 'invalido'\n"
            "    if a == b == c:\n"
            "        return 'equilatero'\n"
            "    elif a == b or b == c or a == c:\n"
            "        return 'isosceles'\n"
            "    else:\n"
            "        return 'escaleno'"
        ),
        "visibles": [
            "assert tipo_triangulo(5, 5, 5) == 'equilatero'",
            "assert tipo_triangulo(3, 3, 5) == 'isosceles'",
            "assert tipo_triangulo(3, 4, 5) == 'escaleno'",
            "assert tipo_triangulo(1, 2, 10) == 'invalido'",
        ],
        "ocultos": [
            "assert tipo_triangulo(0, 0, 0) == 'invalido'",
            "assert tipo_triangulo(7, 7, 9) == 'isosceles'",
            "assert tipo_triangulo(6, 8, 10) == 'escaleno'",
            "assert tipo_triangulo(1, 1, 2) == 'invalido'",   # 1+1 <= 2: no válido
        ],
    },
    {
        "n": 3,
        "titulo": "Índice de rentabilidad",
        "enunciado": (
            "Implementa `rentabilidad(precio_compra, precio_venta)` que devuelva:\n"
            "- El **porcentaje de ganancia o pérdida** sobre el precio de compra,\n"
            "  redondeado a 4 decimales.\n"
            "- Formula: `(precio_venta - precio_compra) / precio_compra`\n\n"
            "- Si `precio_compra <= 0`, devuelve `None`.\n\n"
            "**Ejemplos:** `rentabilidad(1000000, 1200000)` → `0.2` (ganancia 20%);\n"
            "`rentabilidad(1000000, 800000)` → `-0.2` (pérdida 20%)."
        ),
        "plantilla": "def rentabilidad(precio_compra, precio_venta):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def rentabilidad(precio_compra, precio_venta):\n"
            "    if precio_compra <= 0:\n"
            "        return None\n"
            "    return round((precio_venta - precio_compra) / precio_compra, 4)"
        ),
        "visibles": [
            "assert rentabilidad(1000000, 1200000) == 0.2",
            "assert rentabilidad(1000000, 800000) == -0.2",
        ],
        "ocultos": [
            "assert rentabilidad(500000, 500000) == 0.0",
            "assert rentabilidad(0, 100000) is None",
            "assert rentabilidad(200000, 250000) == 0.25",
        ],
    },
    {
        "n": 4,
        "titulo": "Clasificar nota universitaria",
        "enunciado": (
            "Implementa `clasificar_nota(nota)` que devuelva la clasificación de una nota:\n"
            "- `'reprobado'` si `nota < 3.0`\n"
            "- `'aprobado'` si `3.0 <= nota < 4.0`\n"
            "- `'bueno'` si `4.0 <= nota < 4.5`\n"
            "- `'excelente'` si `nota >= 4.5`\n\n"
            "**Nota:** la escala es de 0 a 5. Si la nota está fuera de `[0, 5]`, "
            "devuelve `'fuera de rango'`.\n\n"
            "**Ejemplos:** `clasificar_nota(2.5)` → `'reprobado'`; "
            "`clasificar_nota(3.8)` → `'aprobado'`; "
            "`clasificar_nota(4.7)` → `'excelente'`."
        ),
        "plantilla": "def clasificar_nota(nota):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def clasificar_nota(nota):\n"
            "    if nota < 0 or nota > 5:\n"
            "        return 'fuera de rango'\n"
            "    if nota < 3.0:\n"
            "        return 'reprobado'\n"
            "    elif nota < 4.0:\n"
            "        return 'aprobado'\n"
            "    elif nota < 4.5:\n"
            "        return 'bueno'\n"
            "    else:\n"
            "        return 'excelente'"
        ),
        "visibles": [
            "assert clasificar_nota(2.5) == 'reprobado'",
            "assert clasificar_nota(3.8) == 'aprobado'",
            "assert clasificar_nota(4.7) == 'excelente'",
        ],
        "ocultos": [
            "assert clasificar_nota(0.0) == 'reprobado'",
            "assert clasificar_nota(3.0) == 'aprobado'",
            "assert clasificar_nota(4.0) == 'bueno'",
            "assert clasificar_nota(4.5) == 'excelente'",
            "assert clasificar_nota(5.0) == 'excelente'",
            "assert clasificar_nota(-1) == 'fuera de rango'",
            "assert clasificar_nota(6) == 'fuera de rango'",
        ],
    },
    {
        "n": 5,
        "titulo": "Interés simple",
        "enunciado": (
            "Implementa `interes_simple(capital, tasa, tiempo)` que devuelva una tupla "
            "`(interes, monto_total)` donde:\n"
            "- `interes = capital * tasa * tiempo`\n"
            "- `monto_total = capital + interes`\n\n"
            "Los valores se redondean a 2 decimales.\n\n"
            "Si `capital <= 0`, `tasa < 0` o `tiempo < 0`, devuelve `(None, None)`.\n\n"
            "**Ejemplo:** `interes_simple(1000000, 0.05, 3)` → `(150000.0, 1150000.0)`\n"
            "(capital de 1M, tasa 5% anual, 3 años)."
        ),
        "plantilla": "def interes_simple(capital, tasa, tiempo):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def interes_simple(capital, tasa, tiempo):\n"
            "    if capital <= 0 or tasa < 0 or tiempo < 0:\n"
            "        return (None, None)\n"
            "    interes = round(capital * tasa * tiempo, 2)\n"
            "    return (interes, round(capital + interes, 2))"
        ),
        "visibles": [
            "assert interes_simple(1000000, 0.05, 3) == (150000.0, 1150000.0)",
            "assert interes_simple(500000, 0.10, 1) == (50000.0, 550000.0)",
        ],
        "ocultos": [
            "assert interes_simple(0, 0.05, 3) == (None, None)",
            "assert interes_simple(1000000, 0, 3) == (0.0, 1000000.0)",
            "assert interes_simple(1000000, 0.05, 0) == (0.0, 1000000.0)",
            "assert interes_simple(-1000, 0.05, 3) == (None, None)",
        ],
    },
    {
        "n": 6,
        "titulo": "Divisible por 3 y por 5",
        "enunciado": (
            "Implementa `divisible_3_y_5(n)` que devuelva `True` si `n` es divisible "
            "**simultáneamente** por 3 y por 5; `False` en caso contrario.\n\n"
            "**Ejemplos:** `divisible_3_y_5(15)` → `True`; "
            "`divisible_3_y_5(9)` → `False`; "
            "`divisible_3_y_5(30)` → `True`."
        ),
        "plantilla": "def divisible_3_y_5(n):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def divisible_3_y_5(n):\n"
            "    return n % 3 == 0 and n % 5 == 0"
        ),
        "visibles": [
            "assert divisible_3_y_5(15) is True",
            "assert divisible_3_y_5(9) is False",
            "assert divisible_3_y_5(30) is True",
        ],
        "ocultos": [
            "assert divisible_3_y_5(0) is True",     # 0 es divisible por cualquier número
            "assert divisible_3_y_5(1) is False",
            "assert divisible_3_y_5(45) is True",
            "assert divisible_3_y_5(10) is False",
            "assert divisible_3_y_5(6) is False",
        ],
    },
    {
        "n": 7,
        "titulo": "Precio con descuento e IVA encadenados",
        "enunciado": (
            "Implementa `precio_final(precio_original, descuento, tasa_iva)` que:\n"
            "1. Aplica el descuento al precio original: `precio_desc = precio_original * (1 - descuento)`\n"
            "2. Aplica el IVA sobre el precio con descuento: `final = precio_desc * (1 + tasa_iva)`\n"
            "3. Devuelve una tupla `(precio_desc, final)` redondeada a 2 decimales.\n\n"
            "Si `precio_original <= 0` o `descuento < 0` o `descuento > 1` o "
            "`tasa_iva < 0`, devuelve `(None, None)`.\n\n"
            "**Ejemplo:** `precio_final(100000, 0.10, 0.19)` → `(90000.0, 107100.0)`."
        ),
        "plantilla": "def precio_final(precio_original, descuento, tasa_iva):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def precio_final(precio_original, descuento, tasa_iva):\n"
            "    if precio_original <= 0 or descuento < 0 or descuento > 1 or tasa_iva < 0:\n"
            "        return (None, None)\n"
            "    precio_desc = round(precio_original * (1 - descuento), 2)\n"
            "    final = round(precio_desc * (1 + tasa_iva), 2)\n"
            "    return (precio_desc, final)"
        ),
        "visibles": [
            "assert precio_final(100000, 0.10, 0.19) == (90000.0, 107100.0)",
            "assert precio_final(50000, 0, 0.19) == (50000.0, 59500.0)",
        ],
        "ocultos": [
            "assert precio_final(0, 0.10, 0.19) == (None, None)",
            "assert precio_final(100000, -0.1, 0.19) == (None, None)",
            "assert precio_final(100000, 1.5, 0.19) == (None, None)",
            "assert precio_final(200000, 0.15, 0.08) == (170000.0, 183600.0)",
        ],
    },
    {
        "n": 8,
        "titulo": "Convertir segundos a horas, minutos y segundos",
        "enunciado": (
            "Implementa `segundos_a_hms(total_segundos)` que convierta un número de "
            "segundos a una tupla `(horas, minutos, segundos)`.\n\n"
            "Usa solo división entera `//` y módulo `%`. "
            "Si `total_segundos < 0`, devuelve `(None, None, None)`.\n\n"
            "**Ejemplos:**\n"
            "- `segundos_a_hms(3661)` → `(1, 1, 1)` (1h 1m 1s)\n"
            "- `segundos_a_hms(90)` → `(0, 1, 30)` (0h 1m 30s)\n"
            "- `segundos_a_hms(0)` → `(0, 0, 0)`"
        ),
        "plantilla": "def segundos_a_hms(total_segundos):\n    # ✏️ TU CÓDIGO AQUÍ\n    " + NI,
        "solucion": (
            "def segundos_a_hms(total_segundos):\n"
            "    if total_segundos < 0:\n"
            "        return (None, None, None)\n"
            "    horas   = total_segundos // 3600\n"
            "    resto   = total_segundos % 3600\n"
            "    minutos = resto // 60\n"
            "    segs    = resto % 60\n"
            "    return (horas, minutos, segs)"
        ),
        "visibles": [
            "assert segundos_a_hms(3661) == (1, 1, 1)",
            "assert segundos_a_hms(90)   == (0, 1, 30)",
            "assert segundos_a_hms(0)    == (0, 0, 0)",
        ],
        "ocultos": [
            "assert segundos_a_hms(3600) == (1, 0, 0)",
            "assert segundos_a_hms(86399) == (23, 59, 59)",
            "assert segundos_a_hms(-1) == (None, None, None)",
            "assert segundos_a_hms(9753) == (2, 42, 33)",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 2 · Tarea 01 — 8 ejercicios autocalificables

### Variables, tipos de datos, operadores y condicionales

**Instrucciones**

1. Implementa cada función en la celda `# ✏️ TU CÓDIGO AQUÍ`
   (reemplaza la línea `raise NotImplementedError`).
2. **No cambies el nombre ni los parámetros** de las funciones.
3. Ejecuta las celdas de tests visibles y adicionales. Deben pasar sin error.
4. Tu objetivo: que **todas** las celdas de tests muestren ✅.

> 🔎 Antes de programar, escribe el pseudocódigo y traza un ejemplo a mano.

> ⚠️ Esta tarea **no** corre de principio a fin hasta que implementes cada función.

**Conceptos ejercitados:** operadores `//` y `%`, condicionales escalonados,
type casting, operadores lógicos, validación de casos borde.
""",
    "cierre_md": r"""
---
## Entrega

Cuando todas las celdas de tests muestren ✅, has completado la tarea.

| Ejercicio | Patrón principal |
|---|---|
| 1 Días entre años | bucle + operador % + condicional bisiesto |
| 2 Tipo triángulo | múltiples condicionales + operadores lógicos |
| 3 Índice de rentabilidad | operadores aritméticos + validación |
| 4 Clasificar nota | condicional escalonado + caso borde |
| 5 Interés simple | aritmética básica + validación de entradas |
| 6 Divisible por 3 y 5 | operador % + and lógico |
| 7 Descuento + IVA | aritmética encadenada + validación |
| 8 Segundos a HH:MM:SS | operadores // y % anidados |

> 💭 **Reflexión:** los ejercicios 6, 7 y 8 ilustran que la mayoría de
> los problemas "de negocios" son, en el fondo, problemas de aritmética
> y lógica booleana. La próxima clase añadiremos bucles para manejar
> *colecciones* de datos.
""",
}

validar(ejercicios)
construir_homework(
    meta,
    ejercicios,
    os.path.join(os.path.dirname(__file__), "..", "curso", "clase02", "homework01.ipynb"),
    os.path.join(os.path.dirname(__file__), "solved", "clase02_homework01_solved.ipynb"),
)

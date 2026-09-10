#!/usr/bin/env python3
"""
Generador determinista para el notebook de la Clase 02:
"Cómo funcionan los modelos generativos y multimodales"
Módulo 3 · Diplomado en IA para los Negocios (Universidad Santo Tomás).

Genera ediciones/2026/notebooks/02-como-funcionan-modelos.ipynb con el estándar
institucional, Colab Forms interactivos sin código, simulador de tokens y costos,
y la Ficha de Decisión Directiva.
"""
import json
import statistics
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).resolve().parent / "02-como-funcionan-modelos.ipynb"


def con_ids(celdas: list[dict]) -> list[dict]:
    """nbformat 4.5+ exige un id por celda. Deterministas para evitar ruido en git diff."""
    for i, celda in enumerate(celdas):
        celda["id"] = f"c{i:02d}"
    return celdas


def build_cells():
    cells = []

    # 0. Header institucional
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            '<div style="display:flex; align-items:center; gap:18px; text-align:left">\n',
            '  <img src="https://sebastiancontz.github.io/ust-diplomado-ia-curso-intro-ia/assets/logo-ust.svg" width="100" alt="Logo Universidad Santo Tomás">\n',
            '  <div>\n',
            '    <p>Diplomado en Inteligencia Artificial para los Negocios</p>\n',
            '    <p>Facultad de Ingeniería y Negocios</p>\n',
            '    <p>Módulo 3 · Introducción a la Inteligencia Artificial Generativa</p>\n',
            '    <p>Semana 02: Cómo funcionan los modelos generativos y multimodales</p>\n',
            '  </div>\n',
            '</div>'
        ]
    })

    # 1. Título y Badge Open in Colab
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Taller de Experimentación y Decisión Directiva\n",
            "\n",
            '<a href="https://colab.research.google.com/github/sebastiancontz/ust-diplomado-ia-curso-intro-ia-colab/blob/main/ediciones/2026/notebooks/02-como-funcionan-modelos.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>\n',
            "\n",
            "Bienvenidas y bienvenidos al taller práctico de la **Clase 02**.\n",
            "\n",
            "En esta sesión desmitificamos la física interna de los modelos de lenguaje (LLMs) y los modelos multimodales.\n",
            "\n",
            "Este cuaderno está diseñado con un enfoque **100% directivo y analítico (sin necesidad de escribir código)**:\n",
            "- No necesitan programar scripts ni recordar sintaxis de Python.\n",
            "- Las celdas de cálculo operan como **formularios interactivos** con perillas, listas desplegables y parámetros configurables.\n",
            "- Su foco está en el **análisis de escenarios, la gobernanza de riesgos y la toma de decisiones financieras**.\n",
            "\n",
            "### Objetivos del taller\n",
            "1. **Familiarizarse con Google Colab:** Conocer el entorno digital de trabajo sin estrés de programación antes de las sesiones de código aplicado.\n",
            "2. **Bitácora de experimentación en Google AI Studio:** Registrar y consolidar las observaciones empíricas sobre fragmentación de tokens en español (factor 1.6), costos multimodales y modulación de temperatura ($T$) y Top_p.\n",
            "3. **Simulador directivo de tokens y costos:** Evaluar el impacto presupuestario de operar un modelo propio on-premise frente a consumir servicios API en la nube para volúmenes reales de negocio.\n",
            "4. **Ficha de Decisión Directiva:** Justificar la arquitectura técnica, parámetros de inferencia y salvaguardas de privacidad para dos organizaciones con requerimientos opuestos: un estudio jurídico corporativo y una agencia de marketing digital."
        ]
    })

    # 2. Cómo usar este cuaderno
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Instrucciones de uso en Google Colab\n",
            "\n",
            "Para trabajar de forma ordenada en este taller:\n",
            "1. **Guardar su copia de trabajo:** Hagan clic en el menú **Archivo** $\\rightarrow$ **Guardar una copia en Drive**. De este modo, sus respuestas y cálculos quedarán almacenados en su cuenta personal o institucional de Google.\n",
            "2. **Ejecución de celdas interactivas:** Para ejecutar una celda de cálculo, hagan clic en el botón de reproducción (**Play** / ▶) ubicado a la izquierda de la celda, o presionen `Ctrl + Enter` estando dentro de ella.\n",
            "3. **Formularios sin código (Colab Forms):** Las celdas técnicas tienen el código oculto y muestran un formulario visual. Solo deben modificar los valores en los casilleros y presionar Play para actualizar los resultados.\n",
            "4. **Completar respuestas de texto:** Para responder las preguntas de análisis directivo, hagan doble clic sobre las celdas de texto correspondientes, completen sus respuestas en los casilleros indicados y presionen `Shift + Enter` para guardar."
        ]
    })

    # 3. Bitácora AI Studio
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Bitácora de experimentación en Google AI Studio\n",
            "\n",
            "Entorno de experimentación en vivo: [**aistudio.google.com**](https://aistudio.google.com)\n",
            "\n",
            "Durante la primera parte del taller exploramos tres fenómenos clave de los modelos fundacionales. Utilicen la siguiente pauta para registrar sus observaciones de auditoría técnica:\n",
            "\n",
            "### Ejercicio A · El impuesto al español y multimodalidad\n",
            "- **Prueba de texto:** Contrastar la frase en inglés (*\"The company reported solid earnings this quarter\"*) frente a su traducción al español (*\"La compañía reportó ganancias sólidas en este trimestre\"*).\n",
            "- **Prueba de imagen:** Cargar una imagen (gráfico contable o factura escaneada) en el prompt y observar el conteo de tokens asignado (~258 tokens visuales).\n",
            "\n",
            "### Ejercicio B · Prueba de consistencia estricta ($T = 0.0$)\n",
            "- **Consigna:** Extraer cliente, monto, fecha y estado de pago del caso *Constructora del Sur SpA*.\n",
            "- **Calibración:** Fijar Temperatura en **0.0** y ejecutar la solicitud 2 veces consecutivas para comprobar reproducibilidad idéntica.\n",
            "\n",
            "### Ejercicio C · Prueba creativa y corte estadístico con Top_p\n",
            "- **Consigna:** Redactar 3 eslóganes comerciales para café sustentable chileno.\n",
            "- **Calibración 1:** Temperatura **1.3** con Top_p **0.95** (evaluar variedad léxica).\n",
            "- **Calibración 2:** Temperatura **1.3** con Top_p **0.10** (evaluar empobrecimiento forzado hacia la punta de la campana)."
        ]
    })

    # 4. Tabla de registro de la bitácora
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Registro de observaciones (Bitácora del estudiante)\n",
            "\n",
            "Completen la siguiente tabla haciendo doble clic sobre esta celda:\n",
            "\n",
            "| Prueba realizada | Tokens observados | Comportamiento del modelo | Conclusión directiva para la empresa |\n",
            "|:---|:---:|:---|:---|\n",
            "| **Texto en inglés** | *[ej. 8 tokens]* | Frase concisa en inglés. | Línea base de costo estándar. |\n",
            "| **Texto en español** | *[ej. 12 tokens]* | Fragmentación en subpalabras por vocabulario BPE. | **Impuesto al español:** ~50% más de costo en tokens para procesar el mismo contenido. |\n",
            "| **Imagen multimodal** | *[ej. 258 tokens]* | Cuadrícula de parches (*patches*) visuales procesados como tokens fijos. | El costo de auditar una factura escaneada es predecible e independiente del texto visible. |\n",
            "| **Consistencia ($T=0.0$)** | *[Tokens]* | Estructura y cifras idénticas en ambas corridas. | **Estándar innegociable en auditoría y finanzas:** cero dispersión estocástica. |\n",
            "| **Creatividad ($T=1.3$)** | *[Tokens]* | Opciones diversas y vocabulario publicitario rico. | Apto para ideación y marketing; inaceptable para contratos o balances. |\n",
            "| **Corte Top_p ($0.10$)** | *[Tokens]* | Frases obvias y monótonas pese a la alta temperatura. | Top_p anula la creatividad al descartar el 90% del vocabulario disponible. |"
        ]
    })

    # 5. Introducción al simulador
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Simulador directivo de tokens y costos\n",
            "\n",
            "La siguiente celda interactiva permite calcular el presupuesto mensual y comparar las dos alternativas de infraestructura corporativa:\n",
            "1. **Servicio API en la nube:** Modelo comercial con pago por uso exacto (tarifas estándar: $0.15 USD por millón de tokens de entrada / $0.60 USD por millón de salida).\n",
            "2. **Servidor Propio On-Premise:** Arriendo de servidor corporativo con GPUs dedicadas ($1.200 USD fijos al mes, se use o no).\n",
            "\n",
            "### Instrucciones:\n",
            "- Seleccionen en la lista desplegable el **escenario** a evaluar (*Caso 1: Estudio Jurídico Velasco & Asoc.* o *Caso 2: Agencia Digital CreaImpacto*).\n",
            "- Hagan clic en el botón **Play** (▶) a la izquierda para calcular el balance financiero y ver el diagnóstico automatizado."
        ]
    })

    # 6. Código del simulador (Colab Form)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "#@title Simulador Directivo de Tokens y Costos { run: \"auto\" }\n",
            "#@markdown Ingrese o seleccione los parámetros operativos a simular:\n",
            "\n",
            "escenario = \"Caso 1: Estudio Jurídico Velasco & Asoc. (Legal)\"  #@param [\"Caso 1: Estudio Jurídico Velasco & Asoc. (Legal)\", \"Caso 2: Agencia Digital CreaImpacto (Marketing)\", \"Personalizado\"]\n",
            "volumen_documentos_mes = 400  #@param {type:\"integer\"}\n",
            "palabras_entrada_por_doc = 10000  #@param {type:\"integer\"}\n",
            "palabras_salida_por_doc = 500  #@param {type:\"integer\"}\n",
            "factor_espanol = 1.6  #@param {type:\"number\"}\n",
            "tarifa_entrada_usd_m = 0.15  #@param {type:\"number\"}\n",
            "tarifa_salida_usd_m = 0.60  #@param {type:\"number\"}\n",
            "costo_fijo_servidor_usd = 1200.0  #@param {type:\"number\"}\n",
            "\n",
            "# Carga automática de parámetros según el caso seleccionado\n",
            "if escenario == \"Caso 1: Estudio Jurídico Velasco & Asoc. (Legal)\":\n",
            "    volumen_documentos_mes = 400\n",
            "    palabras_entrada_por_doc = 10000\n",
            "    palabras_salida_por_doc = 500\n",
            "    tarifa_entrada_usd_m = 0.15\n",
            "    tarifa_salida_usd_m = 0.60\n",
            "    costo_fijo_servidor_usd = 1200.0\n",
            "elif escenario == \"Caso 2: Agencia Digital CreaImpacto (Marketing)\":\n",
            "    volumen_documentos_mes = 2500\n",
            "    palabras_entrada_por_doc = 200\n",
            "    palabras_salida_por_doc = 400\n",
            "    tarifa_entrada_usd_m = 0.15\n",
            "    tarifa_salida_usd_m = 0.60\n",
            "    costo_fijo_servidor_usd = 1200.0\n",
            "\n",
            "# 1. Estimación de tokens con la heurística de español (palabras x 1.6)\n",
            "tokens_entrada_doc = int(palabras_entrada_por_doc * factor_espanol)\n",
            "tokens_salida_doc = int(palabras_salida_por_doc * factor_espanol)\n",
            "\n",
            "tokens_entrada_mes = tokens_entrada_doc * volumen_documentos_mes\n",
            "tokens_salida_mes = tokens_salida_doc * volumen_documentos_mes\n",
            "tokens_totales_mes = tokens_entrada_mes + tokens_salida_mes\n",
            "\n",
            "# 2. Estimación de costos en la nube (API)\n",
            "costo_api_entrada_usd = (tokens_entrada_mes / 1_000_000) * tarifa_entrada_usd_m\n",
            "costo_api_salida_usd = (tokens_salida_mes / 1_000_000) * tarifa_salida_usd_m\n",
            "costo_api_total_usd = costo_api_entrada_usd + costo_api_salida_usd\n",
            "costo_servidor_total_usd = costo_fijo_servidor_usd\n",
            "\n",
            "diferencia_usd = abs(costo_servidor_total_usd - costo_api_total_usd)\n",
            "ratio = costo_servidor_total_usd / costo_api_total_usd if costo_api_total_usd > 0 else 0\n",
            "\n",
            "# 3. Renderizado del reporte ejecutivo\n",
            "from IPython.display import display, Markdown\n",
            "\n",
            "reporte = f\"\"\"\n",
            "### Balance de Procesamiento y Costos Mensuales\n",
            "**Escenario evaluado:** {escenario}\n",
            "\n",
            "| Dimensión Operativa | Entrada (Prompts / Documentos) | Salida (Respuestas / Fichas) | Consolidado Mensual |\n",
            "|:---|:---:|:---:|:---:|\n",
            "| **Palabras por unidad** | {palabras_entrada_por_doc:,} palabras | {palabras_salida_por_doc:,} palabras | - |\n",
            "| **Tokens unitarios (x{factor_espanol})** | {tokens_entrada_doc:,} tokens | {tokens_salida_doc:,} tokens | - |\n",
            "| **Volumen mensual** | {volumen_documentos_mes:,} documentos | {volumen_documentos_mes:,} fichas | - |\n",
            "| **Tokens mensuales** | **{tokens_entrada_mes:,}** | **{tokens_salida_mes:,}** | **{tokens_totales_mes:,} tokens** |\n",
            "| **Tarifa de mercado (/1M)** | ${tarifa_entrada_usd_m:.2f} USD | ${tarifa_salida_usd_m:.2f} USD | - |\n",
            "| **Costo API en la nube** | **${costo_api_entrada_usd:.2f} USD** | **${costo_api_salida_usd:.2f} USD** | **${costo_api_total_usd:.2f} USD/mes** |\n",
            "\n",
            "---\n",
            "\n",
            "### Comparación Financiera Directiva\n",
            "- **Costo mensual del servicio API en la nube:** **${costo_api_total_usd:.2f} USD/mes**\n",
            "- **Costo mensual de servidor dedicado propio (GPU):** **${costo_servidor_total_usd:.2f} USD/mes**\n",
            "- **Brecha financiera mensual:** **${diferencia_usd:.2f} USD/mes** (Servidor propio es **{ratio:,.1f} veces** el costo de la nube)\n",
            "\"\"\"\n",
            "display(Markdown(reporte))\n",
            "\n",
            "# 4. Dictamen directivo automatizado\n",
            "if escenario.startswith(\"Caso 1\"):\n",
            "    dictamen = (\n",
            "        \"> **Dictamen directivo para Caso 1 (Estudio Jurídico):**\\n\"\n",
            "        \"> Aunque la API en la nube costaría apenas **$1.15 USD/mes**, la decisión de asumir un costo de **$1.200 USD/mes** \"\n",
            "        \"> en infraestructura propia se justifica exclusivamente por **secreto profesional estricto y gobernanza de datos** \"\n",
            "        \"> (prohibición contractual de que contratos de M&A salgan a la red pública).\\n\"\n",
            "        \"> La diferencia de $1.198,85 USD/mes no es un sobrecosto tecnológico: es la prima de seguro institucional de confidencialidad.\"\n",
            "    )\n",
            "elif escenario.startswith(\"Caso 2\"):\n",
            "    dictamen = (\n",
            "        \"> **Dictamen directivo para Caso 2 (Agencia Digital):**\\n\"\n",
            "        \"> Para una agencia con requerimiento de salida a producción inmediata y presupuesto acotado, \"\n",
            "        \"> operar un servidor GPU propio de $1.200 USD/mes constituiría una severa ineficiencia financiera.\\n\"\n",
            "        \"> La API con contrato corporativo estándar cuesta apenas **$0.72 USD/mes**, escala elásticamente y \"\n",
            "        \"> no demanda pagar salarios a ingenieros dedicados de infraestructura.\"\n",
            "    )\n",
            "else:\n",
            "    dictamen = f\"> **Dictamen directivo:** La diferencia neta entre nube y servidor propio es de ${diferencia_usd:.2f} USD/mes. Evalúen si su mandato de privacidad justifica la inversión en infraestructura fija.\"\n",
            "\n",
            "display(Markdown(dictamen))"
        ]
    })

    # 7. Gráfico comparativo
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "#@title Visualización Gráfica: Comparativa Financiera Mensual (USD) { run: \"auto\" }\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8.5, 3.2), dpi=100)\n",
            "\n",
            "opciones = ['Servicio API Nube\\n(Costo Variable)', 'Servidor On-Premise\\n(Costo Fijo GPU)']\n",
            "valores = [costo_api_total_usd, costo_servidor_total_usd]\n",
            "colores = ['#004F45', '#A5281B']\n",
            "\n",
            "barras = ax.barh(opciones, valores, color=colores, height=0.52, edgecolor='#333333', linewidth=1)\n",
            "\n",
            "# Etiquetas numéricas legibles sobre las barras\n",
            "for barra, val in zip(barras, valores):\n",
            "    ancho = barra.get_width()\n",
            "    ax.text(ancho + (max(valores) * 0.02), barra.get_y() + barra.get_height() / 2,\n",
            "            f'${val:,.2f} USD/mes',\n",
            "            va='center', ha='left', fontsize=11, fontweight='bold', color='#222222')\n",
            "\n",
            "ax.set_xlim(0, max(valores) * 1.25)\n",
            "ax.set_xlabel('Costo Mensual Estimado (USD)', fontsize=10, fontweight='bold', color='#222222')\n",
            "titulo_caso = escenario.split(':')[0] if ':' in escenario else escenario\n",
            "ax.set_title(f'Comparativa de Costo Mensual · {titulo_caso}', fontsize=12, fontweight='bold', color='#004F45', pad=12)\n",
            "ax.grid(axis='x', linestyle='--', alpha=0.5)\n",
            "ax.spines['top'].set_visible(False)\n",
            "ax.spines['right'].set_visible(False)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # 8. Ficha de Decisión Directiva
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Ficha de Decisión Directiva y Calibración Técnica\n",
            "\n",
            "En esta sección de trabajo autónomo en parejas (Fase 3: *Ustedes lo hacen*), documentarán las decisiones estratégicas para ambos casos de negocio.\n",
            "\n",
            "Hagan doble clic sobre cada ficha y completen los cuadrantes con su diagnóstico profesional:\n",
            "\n",
            "### Ficha de Decisión · Caso 1: Estudio Jurídico \"Velasco & Asoc.\"\n",
            "\n",
            "| Cuadrante de Decisión | Elección Técnica / Directiva | Justificación Profesional y de Negocio |\n",
            "|:---|:---|:---|\n",
            "| **1. Gobernanza de Arquitectura** | *[¿Servidor propio on-premise o API comercial?]* | *[Justificar según secreto profesional, confidencialidad legal y marco DPA]* |\n",
            "| **2. Calibración de Inferencia** | **Temperatura:** *[0.0 - 0.2]* <br> **Top_p:** *[0.90]* | *[Justificar la necesidad de consistencia determinista estricta en cláusulas contractuales]* |\n",
            "| **3. Delimitación de Contexto** | **Indispensable:** *[Contrato pertinente]* <br> **Excluir:** *[PII no relevante]* | *[Criterio de minimización de datos y contención del sesgo Lost in the Middle]* |\n",
            "| **4. Evaluación Presupuestaria** | **Costo Servidor:** $1.200 USD <br> **Costo API:** $1.15 USD | *[Conclusión directiva: ¿por qué la empresa acepta un sobrecosto del 104.000%?]* |\n",
            "\n",
            "---\n",
            "\n",
            "### Ficha de Decisión · Caso 2: Agencia Digital \"CreaImpacto\"\n",
            "\n",
            "| Cuadrante de Decisión | Elección Técnica / Directiva | Justificación Profesional y de Negocio |\n",
            "|:---|:---|:---|\n",
            "| **1. Gobernanza de Arquitectura** | *[¿Servidor propio on-premise o API comercial?]* | *[Justificar según Time-to-Market (2 semanas), inversión de capital y soporte de ingeniería]* |\n",
            "| **2. Calibración de Inferencia** | **Temperatura:** *[1.1 - 1.3]* <br> **Top_p:** *[0.95]* | *[Justificar la búsqueda de variedad léxica, originalidad publicitaria y frescura de redacción]* |\n",
            "| **3. Delimitación de Contexto** | **Indispensable:** *[Brief de campaña]* <br> **Excluir:** *[Estrategias no públicas]* | *[Criterio de brevedad en el prompt para asegurar velocidad de respuesta]* |\n",
            "| **4. Evaluación Presupuestaria** | **Costo Servidor:** $1.200 USD <br> **Costo API:** $0.72 USD | *[Conclusión directiva: ¿por qué el pago por uso es la única decisión viable aquí?]* |"
        ]
    })

    # 9. Puesta en común y conclusiones
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Puesta en común y conclusiones directivas\n",
            "\n",
            "Para consolidar lo aprendido en este taller, revisemos los cuatro principios rectores que deben orientar las decisiones de tecnología en sus organizaciones:\n",
            "\n",
            "1. **La privacidad tiene precio de infraestructura:** La soberanía de datos total mediante modelos de pesos abiertos en servidores locales exige costos fijos predecibles pero elevados ($1.200+ USD/mes en hardware GPU). La nube ofrece costos variables marginales, pero requiere contratos corporativos formales (**DPA**) con cláusula de no entrenamiento y retención cero.\n",
            "2. **El impuesto lingüístico es real:** El español consume aproximadamente un **50% a 60% más de tokens** que el inglés por la fragmentación subpalabra del algoritmo BPE. Todo presupuesto y dimensionamiento de ventana de contexto en América Latina debe incorporar el factor $1.6$.\n",
            "3. **Temperatura cero para control y finanzas:** En tareas de extracción contable, conciliación, auditoría o estructuración legal, la temperatura debe fijarse estrictamente en **0.0**. En estas áreas, la estocasticidad o la \"creatividad\" léxica constituyen un fallo operacional severo.\n",
            "4. **La perilla de control único:** Al calibrar modelos en producción, modulen la Temperatura o modulen Top_p, pero eviten mover ambos controles de manera simultánea sin una hipótesis de diseño clara."
        ]
    })

    # 10. Atribución de datos
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Atribución de datos\n",
            "\n",
            "- **Creador:** Sebastián Contreras\n",
            "- **Procedencia:** Casos sintéticos elaborados con fines docentes para ilustrar auditoría técnica, privacidad y evaluación directiva de costos en IA. No representan a organizaciones, estudios jurídicos ni agencias reales.\n",
            "- **Modificación:** Ninguna."
        ]
    })

    return con_ids(cells)


def main():
    cells = build_cells()

    md_count = sum(1 for c in cells if c["cell_type"] == "markdown")
    code_count = sum(1 for c in cells if c["cell_type"] == "code")

    code_lines = [len(c["source"]) for c in cells if c["cell_type"] == "code"]
    mediana_lineas = int(statistics.median(code_lines)) if code_lines else 0

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            },
            "curso_contrato": {
                "forma": {
                    "markdown": md_count,
                    "codigo": code_count,
                    "llamadas": []
                },
                "acciones": [],
                "max_mediana_lineas_codigo": max(mediana_lineas + 10, 50)
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Notebook generado deterministamente en: {NOTEBOOK_PATH}")
    print(f"Conteo: {md_count} celdas markdown, {code_count} celdas código. Mediana líneas: {mediana_lineas}")


if __name__ == "__main__":
    main()

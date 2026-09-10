#!/usr/bin/env python3
"""
Generador determinista para el notebook de la Clase 01:
"Fundamentos de IA generativa y casos de uso en negocios"
Módulo 3 · Diplomado en IA para los Negocios (Universidad Santo Tomás).

Genera ediciones/2026/notebooks/01-fundamentos.ipynb con el estándar
institucional, Colab Forms interactivos sin código, simulador de la matriz
Valor vs. Costo del Error y la Ficha de Evaluación Organizacional.
"""
import json
import statistics
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).resolve().parent / "01-fundamentos.ipynb"


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
            '    <p>Semana 01: Fundamentos de IA generativa y casos de uso en negocios</p>\n',
            '  </div>\n',
            '</div>'
        ]
    })

    # 1. Título y Badge Open in Colab
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Taller de Priorización de Casos de Uso y Gobernanza HITL\n",
            "\n",
            '<a href="https://colab.research.google.com/github/sebastiancontz/ust-diplomado-ia-curso-intro-ia-colab/blob/main/ediciones/2026/notebooks/01-fundamentos.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>\n',
            "\n",
            "Bienvenidas y bienvenidos al taller práctico de la **Clase 01**.\n",
            "\n",
            "En esta sesión inaugural exploramos los fundamentos de la Inteligencia Artificial Generativa, sus cuatro capacidades operativas clave (resumir, clasificar, extraer y reescribir) y los riesgos asociados a la alucinación y la complacencia analítica.\n",
            "\n",
            "Este cuaderno está diseñado con un enfoque **100% directivo y analítico (sin necesidad de escribir código)**:\n",
            "- No requieren programar scripts ni recordar comandos de Python.\n",
            "- Las herramientas operan como **formularios interactivos** (Colab Forms) con menús desplegables y parámetros configurables.\n",
            "- Su objetivo es evaluar procesos organizacionales, ubicarlos en la **Matriz Valor vs. Costo del Error** y definir salvaguardas de supervisión humana (*Humano en el Bucle / HITL*).\n",
            "\n",
            "### Objetivos del taller\n",
            "1. **Familiarizarse con Google Colab:** Conocer el entorno digital de trabajo y aprender a guardar sus avances y notas personales en Google Drive de forma amigable.\n",
            "2. **Analizar el espectro de criticidad:** Contrastar casos extremos de bajo y alto costo de error (minutas comerciales vs. compliance penal).\n",
            "3. **Diseñar triaje bancario modular:** Evaluar un caso de atención bancaria masiva (15.000 solicitudes/mes) y segmentar qué trámites admiten automatización asistida y cuáles exigen compuerta humana obligatoria.\n",
            "4. **Completar la Ficha de Evaluación Organizacional:** Diagnosticar un proceso real de sus propias áreas de trabajo, justificar el cuadrante asignado y definir la estrategia de supervisión (*Centauro* vs. *Cíborg*) con filtros de confidencialidad."
        ]
    })

    # 2. Cómo usar este cuaderno
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Instrucciones de trabajo en Google Colab\n",
            "\n",
            "Para trabajar de forma ordenada en este taller:\n",
            "1. **Guardar su copia de trabajo:** Hagan clic en el menú superior **Archivo** $\\rightarrow$ **Guardar una copia en Drive**. De esta manera, sus diagnósticos quedarán almacenados en su cuenta personal o corporativa.\n",
            "2. **Ejecutar celdas interactivas:** Para ejecutar una celda de cálculo o gráfico, hagan clic en el botón de reproducción (**Play** / ▶) ubicado a la izquierda de la celda, o presionen `Ctrl + Enter` dentro de ella.\n",
            "3. **Formularios sin código (Colab Forms):** Las celdas de simulación tienen el código oculto y muestran controles visuales. Solo deben elegir las opciones deseadas y presionar Play para actualizar el análisis.\n",
            "4. **Completar respuestas de texto:** Para completar las fichas de evaluación, hagan doble clic sobre la celda de texto correspondiente, editen las casillas indicadas y presionen `Shift + Enter` para guardar."
        ]
    })

    # 3. Demostración modelada: Casos Extremos
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Demostración modelada: El espectro de criticidad\n",
            "\n",
            "En la sesión teórica aprendimos que la adopción de IA generativa no depende de la sofisticación técnica, sino del **costo del error** y la **reversibilidad del fallo**:\n",
            "\n",
            "### Caso 1 · Resumen de minutas de comités comerciales (Bajo costo de error)\n",
            "- **Valor de negocio:** Medio/Alto (ahorra ~45 minutos de digitación por reunión a cada jefatura comercial).\n",
            "- **Costo del error:** Bajo (si el modelo omite un acuerdo menor, los asistentes lo subsanan de inmediato al revisar el correo).\n",
            "- **Tolerancia al error:** Alta (falla inocua y fácilmente reversible).\n",
            "- **Cuadrante asignado:** **Cuadrante A / C (Automatización asistida)**. El organizador da un vistazo rápido antes de enviar.\n",
            "\n",
            "### Caso 2 · Dictamen vinculante de compliance y lavado de activos (Alto costo de error)\n",
            "- **Valor de negocio:** Muy alto (cruce masivo de proveedores internacionales contra listas de sanciones).\n",
            "- **Costo del error:** Catastrófico (sanciones penales para directores, multas regulatorias y pérdida de licencia bancaria).\n",
            "- **Tolerancia al error:** Nula (falla irreversible con responsabilidad legal indelegable).\n",
            "- **Cuadrante asignado:** **Cuadrante B (Co-piloto HITL obligatorio)**. La IA redacta el borrador de antecedentes, pero el oficial de cumplimiento audita y firma obligatoriamente la resolución."
        ]
    })

    # 4. Práctica guiada: Caso bancario masivo
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Práctica guiada: El dilema de atención bancaria masiva\n",
            "\n",
            "Una institución financiera en Chile recibe **15.000 solicitudes mensuales** en su canal web. La gerencia de operaciones propuso inicialmente:\n",
            "*\"Conectemos un LLM autónomo para responder el 100% de los mensajes de inmediato y eliminemos el tiempo de espera\"*.\n",
            "\n",
            "### Análisis de triaje y segmentación de flujos\n",
            "En lugar de un enfoque \"todo o nada\", la arquitectura directiva correcta aplica un **triaje inteligente** que deriva cada solicitud según su criticidad:\n",
            "\n",
            "| Tipo de Solicitud | Volumen Estimado | Tolerancia al Error | Cuadrante Matriz | Arquitectura de Supervisión |\n",
            "|:---|:---:|:---:|:---:|:---|\n",
            "| **Consultas informativas** (horarios, saldos, sucursales) | 8.000 / mes | Alta | **Cuadrante A** | Automatización asistida directa con respuestas precalibradas. |\n",
            "| **Reclamos por cobros duplicados** | 4.500 / mes | Media | **Cuadrante A / B** | Extracción estructurada (IDP) de montos y cuentas; confirmación previa antes de abonar. |\n",
            "| **Denuncias de fraude y bloqueos** | 1.800 / mes | Baja | **Cuadrante B** | Bloqueo preventivo automático + derivación inmediata a analista de seguridad. |\n",
            "| **Solicitudes de crédito y renegociación** | 700 / mes | Nula | **Cuadrante B** | Evaluación asistida por IA; firma y visación final reservada exclusivamente a ejecutivo bancario. |"
        ]
    })

    # 5. Simulador de Priorización (Colab Form)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Simulador interactivo: Matriz Valor vs. Costo del Error\n",
            "\n",
            "Utilicen la siguiente celda interactiva para evaluar cualquier proceso de su organización.\n",
            "\n",
            "### Instrucciones:\n",
            "1. Seleccionen un proceso preconfigurado o elijan **\"Proceso propio de mi empresa\"**.\n",
            "2. Ajusten la capacidad requerida, el nivel de valor de negocio y el costo del error.\n",
            "3. Hagan clic en el botón **Play** (▶) a la izquierda para generar el dictamen directivo y ver la ubicación en la matriz."
        ]
    })

    # 6. Código del simulador (Colab Form)
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "#@title Matriz Interactiva de Priorización y Triaje de Procesos { run: \"auto\" }\n",
            "#@markdown Ingrese o seleccione los parámetros del proceso organizacional a evaluar:\n",
            "\n",
            "proceso_seleccionado = \"Triaje y análisis de solicitudes bancarias (Caso Guiado)\"  #@param [\"Triaje y análisis de solicitudes bancarias (Caso Guiado)\", \"Minutas de comités comerciales (Caso 1)\", \"Dictamen vinculante de compliance (Caso 2)\", \"Proceso propio de mi empresa (Personalizado)\"]\n",
            "nombre_proceso_personalizado = \"Conciliación de facturas de proveedores\"  #@param {type:\"string\"}\n",
            "capacidad_ia = \"Extracción de datos estructurados (IDP)\"  #@param [\"Resumir textos extensos\", \"Clasificar y categorizar\", \"Extracción de datos estructurados (IDP)\", \"Reescribir y adaptar tono\"]\n",
            "nivel_valor = \"Alto (Impacto estratégico o gran ahorro de horas)\"  #@param [\"Alto (Impacto estratégico o gran ahorro de horas)\", \"Medio (Ahorro operativo moderado)\", \"Bajo (Impacto marginal)\"]\n",
            "nivel_costo_error = \"Alto (Pérdidas financieras severas, legal o regulatorio)\"  #@param [\"Crítico / Catastrófico (Sanciones penales o regulatorias)\", \"Alto (Pérdidas financieras severas, legal o regulatorio)\", \"Medio (Retrabajo interno subsanable)\", \"Bajo / Inocuo (Error evidente corregible de inmediato)\"]\n",
            "volumen_mensual = 15000  #@param {type:\"integer\"}\n",
            "\n",
            "# Determinar nombre activo\n",
            "if proceso_seleccionado == \"Proceso propio de mi empresa (Personalizado)\":\n",
            "    nombre_activo = nombre_proceso_personalizado\n",
            "else:\n",
            "    nombre_activo = proceso_seleccionado.split(\" (\")[0]\n",
            "\n",
            "# Mapeo a coordenadas cuantitativas en la matriz (0 a 10)\n",
            "valor_map = {\n",
            "    \"Alto (Impacto estratégico o gran ahorro de horas)\": 8.0,\n",
            "    \"Medio (Ahorro operativo moderado)\": 5.0,\n",
            "    \"Bajo (Impacto marginal)\": 2.5,\n",
            "}\n",
            "error_map = {\n",
            "    \"Crítico / Catastrófico (Sanciones penales o regulatorias)\": 9.0,\n",
            "    \"Alto (Pérdidas financieras severas, legal o regulatorio)\": 7.5,\n",
            "    \"Medio (Retrabajo interno subsanable)\": 4.5,\n",
            "    \"Bajo / Inocuo (Error evidente corregible de inmediato)\": 2.0,\n",
            "}\n",
            "\n",
            "y_val = valor_map.get(nivel_valor, 5.0)\n",
            "x_err = error_map.get(nivel_costo_error, 5.0)\n",
            "\n",
            "# Identificación de cuadrante\n",
            "if y_val >= 5.0 and x_err < 5.0:\n",
            "    cuadrante = \"CUADRANTE A · Automatización Asistida\"\n",
            "    arquetipo = \"Cíborg o Centauro liviano\"\n",
            "    supervision = \"Revisión por muestreo o supervisión secundaria del usuario final.\"\n",
            "    veredicto = \"Adopción prioritaria. Entrega alto retorno con riesgo operativo controlado.\"\n",
            "elif y_val >= 5.0 and x_err >= 5.0:\n",
            "    cuadrante = \"CUADRANTE B · Co-piloto con HITL Obligatorio\"\n",
            "    arquetipo = \"Centauro estricto (Humano en el Bucle)\"\n",
            "    supervision = \"Compuerta humana previa obligatoria. Ninguna salida tiene efecto legal o financiero sin firma profesional responsable.\"\n",
            "    veredicto = \"Adopción de alto valor pero condicionada a gobernanza estricta. Prohibida la automatización autónoma desatendida.\"\n",
            "elif y_val < 5.0 and x_err < 5.0:\n",
            "    cuadrante = \"CUADRANTE C · Exploración y Eficiencia Interna\"\n",
            "    arquetipo = \"Asistente individual libre\"\n",
            "    supervision = \"Criterio del colaborador. No requiere comités burocráticos.\"\n",
            "    veredicto = \"Uso táctico para ganar agilidad individual. No priorizar inversión en desarrollo corporativo.\"\n",
            "else:\n",
            "    cuadrante = \"CUADRANTE D · Zona Desaconsejada / Alto Riesgo\"\n",
            "    arquetipo = \"No implementar con IA\"\n",
            "    supervision = \"Proceso manual o software determinista tradicional (SQL / ERP).\"\n",
            "    veredicto = \"Riesgo desproporcionado frente al valor generado. Rechazar la iniciativa de IA generativa.\"\n",
            "\n",
            "from IPython.display import display, Markdown\n",
            "\n",
            "reporte = f\"\"\"\n",
            "### Dictamen Directivo de Gobernanza: {nombre_activo}\n",
            "\n",
            "| Dimensión de Análisis | Diagnóstico Asignado |\n",
            "|:---|:---|\n",
            "| **Proceso Evaluado** | {nombre_activo} ({volumen_mensual:,} solicitudes/mes) |\n",
            "| **Capacidad Principal** | {capacidad_ia} |\n",
            "| **Cuadrante de la Matriz** | **{cuadrante}** |\n",
            "| **Arquetipo de Trabajo** | **{arquetipo}** |\n",
            "| **Mandato de Supervisión** | {supervision} |\n",
            "| **Recomendación Ejecutiva** | **{veredicto}** |\n",
            "\"\"\"\n",
            "display(Markdown(reporte))"
        ]
    })

    # 7. Gráfico de la Matriz
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "#@title Visualización Gráfica: Matriz de Priorización Valor vs. Costo del Error { run: \"auto\" }\n",
            "import matplotlib.pyplot as plt\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8.5, 6.0), dpi=100)\n",
            "\n",
            "# Fondos de los cuatro cuadrantes\n",
            "ax.fill_between([0, 5], 5, 10, color='#004F45', alpha=0.12, label='Cuadrante A (Automatización Asistida)')\n",
            "ax.fill_between([5, 10], 5, 10, color='#C0392B', alpha=0.12, label='Cuadrante B (Co-piloto HITL Obligatorio)')\n",
            "ax.fill_between([0, 5], 0, 5, color='#7F8C8D', alpha=0.10, label='Cuadrante C (Exploración / Eficiencia)')\n",
            "ax.fill_between([5, 10], 0, 5, color='#D35400', alpha=0.15, label='Cuadrante D (Zona Desaconsejada)')\n",
            "\n",
            "# Líneas divisorias de la matriz\n",
            "ax.axvline(5.0, color='#222222', linestyle='--', linewidth=1.2)\n",
            "ax.axhline(5.0, color='#222222', linestyle='--', linewidth=1.2)\n",
            "\n",
            "# Rótulos de cuadrantes\n",
            "ax.text(2.5, 9.2, 'CUADRANTE A\\nAutomatización Asistida\\n(Alto Valor · Bajo Riesgo)', ha='center', va='center', fontsize=10, fontweight='bold', color='#004F45')\n",
            "ax.text(7.5, 9.2, 'CUADRANTE B\\nCo-piloto HITL Obligatorio\\n(Alto Valor · Alto Riesgo)', ha='center', va='center', fontsize=10, fontweight='bold', color='#A5281B')\n",
            "ax.text(2.5, 1.2, 'CUADRANTE C\\nExploración Interna\\n(Bajo Valor · Bajo Riesgo)', ha='center', va='center', fontsize=10, fontweight='bold', color='#555555')\n",
            "ax.text(7.5, 1.2, 'CUADRANTE D\\nZona Desaconsejada\\n(Bajo Valor · Alto Riesgo)', ha='center', va='center', fontsize=10, fontweight='bold', color='#B9770E')\n",
            "\n",
            "# Punto del proceso evaluado\n",
            "ax.scatter([x_err], [y_val], color='#004F45', s=240, edgecolors='#FFFFFF', linewidth=2.5, zorder=5)\n",
            "ax.annotate(\n",
            "    f'{nombre_activo}',\n",
            "    (x_err, y_val),\n",
            "    textcoords='offset points',\n",
            "    xytext=(0, 15),\n",
            "    ha='center',\n",
            "    fontsize=11,\n",
            "    fontweight='bold',\n",
            "    bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor='#004F45', alpha=0.95),\n",
            "    zorder=6,\n",
            ")\n",
            "\n",
            "ax.set_xlim(0, 10)\n",
            "ax.set_ylim(0, 10)\n",
            "ax.set_xlabel('Costo del Error e Irreversibilidad del Fallo (Riesgo Directivo) →', fontsize=11, fontweight='bold', color='#222222', labelpad=10)\n",
            "ax.set_ylabel('Valor de Negocio y Ahorro de Horas (Impacto) →', fontsize=11, fontweight='bold', color='#222222', labelpad=10)\n",
            "ax.set_title('Ubicación Estratégica en la Matriz Valor vs. Costo del Error', fontsize=13, fontweight='bold', color='#004F45', pad=14)\n",
            "\n",
            "ax.set_xticks([0, 2.5, 5.0, 7.5, 10])\n",
            "ax.set_xticklabels(['Inocuo', 'Bajo', 'Umbral de Control', 'Alto', 'Catastrófico'])\n",
            "ax.set_yticks([0, 2.5, 5.0, 7.5, 10])\n",
            "ax.set_yticklabels(['Marginal', 'Bajo', 'Umbral de Retorno', 'Medio/Alto', 'Estratégico'])\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    })

    # 8. Ficha de Evaluación Organizacional
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Ficha de Evaluación Organizacional (Trabajo en parejas)\n",
            "\n",
            "En esta sección de trabajo autónomo en parejas (Fase 3: *Lo hacen*), diagnosticarán **un proceso real de sus propias áreas de trabajo**.\n",
            "\n",
            "> **Regla obligatoria de confidencialidad:** Todos los casos y antecedentes deben ser **estrictamente anonimizados**, sin nombres de clientes, personas ni cifras sensibles.\n",
            "\n",
            "Hagan doble clic sobre la siguiente tabla para registrar su evaluación corporativa:\n",
            "\n",
            "| Paso de Análisis | Campo de la Ficha | Diagnóstico de su Equipo |\n",
            "|:---|:---|:---|\n",
            "| **Paso 1 · Diagnóstico** | **Nombre del proceso corporativo** | *[ej. Revisión de poderes notariales / Auditoría de boletas]* |\n",
            "| | **Capacidad principal requerida** | *[¿Resumir, clasificar, extraer IDP o reescribir?]* |\n",
            "| | **Valor de negocio estimado** | *[¿Alto, Medio o Bajo? Justificar horas ahorradas]* |\n",
            "| | **Costo y tolerancia al error** | *[¿Qué ocurre si la IA alucina? ¿El error es reversible o irreversible?]* |\n",
            "| **Paso 2 · Gobernanza** | **Cuadrante asignado en la matriz** | *[¿Cuadrante A, B, C o D?]* |\n",
            "| | **Estrategia de supervisión** | *[¿Arquetipo Centauro o Cíborg?]* |\n",
            "| | **Cargo responsable de la firma** | *[¿Qué profesional o jefatura valida antes del efecto final?]* |\n",
            "| | **Resguardo de privacidad** | *[¿Qué datos sensibles existen y qué filtros de anonimización aplicarán?]* |"
        ]
    })

    # 9. Síntesis y Cierre
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Síntesis directiva de la sesión\n",
            "\n",
            "Para concluir el taller, consolidemos las cinco conclusiones rectoras de la Clase 01:\n",
            "\n",
            "1. **La IA generativa no reemplaza al ML predictivo:** Trabajan en equipo. El Machine Learning predictivo optimiza decisiones sobre datos tabulares cuantitativos; la IA generativa procesa, extrae y transforma el lenguaje no estructurado.\n",
            "2. **El valor está en transformar, no en chatear:** Las cuatro capacidades esenciales (resumir, clasificar, extraer estructurado y reescribir) permiten encadenar flujos operativos automatizados hacia ERP y planillas de gestión.\n",
            "3. **La alucinación es estructural:** Los modelos de lenguaje son motores estadísticos de predicción de tokens, no bases de datos deterministas. Todo diseño de procesos debe asumir que el modelo puede alucinar con alta elocuencia formal.\n",
            "4. **La privacidad exige contratos Enterprise:** Introducir datos corporativos en herramientas gratuitas expone a la empresa a fuga de secretos comerciales y litigios de propiedad intelectual.\n",
            "5. **El costo del error define la adopción:** En tareas de alto impacto o falla irreversible, el **Humano en el Bucle (HITL)** bajo una estrategia Centauro es una salvaguarda institucional innegociable."
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
            "- **Procedencia:** Casos sintéticos elaborados con fines docentes para ilustrar auditoría técnica, control de gestión y evaluación de riesgos en IA. No representan a organizaciones reales.\n",
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
                "max_mediana_lineas_codigo": max(mediana_lineas + 10, 80)
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

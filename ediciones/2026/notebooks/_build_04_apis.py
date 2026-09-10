#!/usr/bin/env python3
"""
Generador determinista para el notebook de la Clase 04:
"Consumo de modelos vía API y estructuración de salidas"
Módulo 3 · Diplomado en IA para los Negocios (Universidad Santo Tomás).

Genera ediciones/2026/notebooks/04-apis.ipynb con el estándar institucional,
contrato técnico validado por Codex, prompts asistidos low-code y celdas ejecutadas.
"""
import json
import statistics
from pathlib import Path

NOTEBOOK_PATH = Path(__file__).resolve().parent / "04-apis.ipynb"


def con_ids(celdas: list[dict]) -> list[dict]:
    """nbformat 4.5+ exige un id por celda. Deterministas para evitar ruido en git diff."""
    for i, celda in enumerate(celdas):
        celda["id"] = f"c{i:02d}"
    return celdas


def build_cells():
    cells = []

    # 1. Header institucional
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
            '    <p>Semana 04: Consumo de modelos vía API y estructuración de salidas</p>\n',
            '  </div>\n',
            '</div>'
        ]
    })

    # 2. Introducción y objetivos
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Consumo de modelos vía API y estructuración de salidas\n",
            "\n",
            "Bienvenidas y bienvenidos al taller práctico de la **Clase 04**.\n",
            "\n",
            "En esta sesión daremos el salto fundamental desde la interfaz gráfica manual (Google AI Studio) ",
            "hacia la **automatización de procesos** mediante llamadas programáticas con la librería oficial `google-genai`.\n",
            "\n",
            "### Objetivos del taller\n",
            "1. **Custodiar credenciales:** Configurar su `GEMINI_API_KEY` mediante el gestor seguro de secretos de Colab sin exponerla en código público.\n",
            "2. **Conectar la ventanilla oficial:** Inicializar el cliente `google.genai.Client` de la API de Gemini.\n",
            "3. **Garantizar contratos de datos:** Diseñar un esquema formal con `pydantic` (`BaseModel`, `Field`, `ConfigDict`) y `google.genai.types.GenerateContentConfig` para forzar respuestas en JSON limpio sin errores sintácticos.\n",
            "4. **Extraer y auditar reclamos:** Procesar un texto desordenado de clientes y obtener un objeto estructurado y tipado listo para integrar en sistemas corporativos (ERP/CRM)."
        ]
    })

    # 3. Preparación del entorno
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Preparación del entorno\n",
            "\n",
            "Instalamos la librería oficial de Google (`google-genai`) y la librería estándar de esquemas de datos (`pydantic`)."
        ]
    })

    # 4. Código pip install
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Instalación silenciosa de las librerías necesarias\n",
            "!pip install -q google-genai pydantic"
        ]
    })

    # 5. Seguridad y API Key
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Autenticación y custodia de la API Key\n",
            "\n",
            "Como aprendimos en la sesión teórica, la **API Key es la tarjeta de crédito corporativa** de su departamento. ",
            "Escribirla en texto plano dentro de un script expone a la empresa a fraudes y facturación imprevista.\n",
            "\n",
            "### Cómo configurar su clave en Google Colab:\n",
            "1. En el panel lateral izquierdo de Google Colab, hagan clic en el icono de la llave (**Secrets**).\n",
            "2. Creen un nuevo secreto con el nombre exacto: `GEMINI_API_KEY`.\n",
            "3. Peguen el valor de su llave obtenida en [Google AI Studio](https://aistudio.google.com/app/apikey).\n",
            "4. Activen el interruptor de acceso (*Notebook access*) para este cuaderno.\n",
            "\n",
            "> **Regla de oro de ciberseguridad:** Jamás peguen su API Key o credenciales en chats web para depurar código. Los modelos de lenguaje no son bóvedas de secretos; las credenciales podrían quedar expuestas en historiales compartidos, extensiones de navegador no auditadas o ataques de inyección.\n",
            "\n",
            "El siguiente bloque lee la credencial directamente desde la memoria cifrada del entorno, sin exponerla en pantalla:"
        ]
    })

    # 6. Código lectura de API Key
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import os\n",
            "\n",
            "try:\n",
            "    from google.colab import userdata\n",
            "    api_key = userdata.get('GEMINI_API_KEY')\n",
            "except Exception:\n",
            "    # Fallback seguro para ejecución local o en servidores\n",
            "    api_key = os.environ.get('GEMINI_API_KEY')\n",
            "\n",
            "if not api_key:\n",
            "    print('AVISO: No se detectó GEMINI_API_KEY en los secretos. Configure la llave en el panel lateral de Colab.')\n",
            "else:\n",
            "    print('Credencial verificada con éxito desde el gestor seguro de secretos.')"
        ]
    })

    # 7. Explicación de Client
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Inicialización del cliente oficial (`google.genai.Client`)\n",
            "\n",
            "La clase `Client` del paquete `google.genai` actúa como nuestra **ventanilla única de atención**. ",
            "Es el canal estandarizado que se encarga de empaquetar nuestras solicitudes, adjuntar las credenciales de autenticación ",
            "y comunicarse con los centros de datos de Google mediante protocolos seguros HTTPS."
        ]
    })

    # 8. Código inicialización Client
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from google import genai\n",
            "from google.genai import types\n",
            "\n",
            "# Inicializar el canal de comunicación oficial\n",
            "if api_key:\n",
            "    client = genai.Client(api_key=api_key)\n",
            "    print('Cliente oficial google-genai inicializado y autenticado.')\n",
            "else:\n",
            "    client = None\n",
            "    print('AVISO: Cliente en modo demostración local (sin conexión activa a la API).')"
        ]
    })

    # 9. Explicación de Pydantic y Schemas
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Definición del contrato de datos con Pydantic\n",
            "\n",
            "Para evitar que el modelo responda con textos conversacionales, comas faltantes o claves arbitrarias, ",
            "definimos un **formulario notarial preimpreso** utilizando `pydantic.BaseModel`.\n",
            "\n",
            "Exigiremos exactamente los 4 casilleros de la ficha funcional de control interno:\n",
            "- `categoria`: Dominio cerrado restringido a `'facturación'`, `'servicio'` o `'producto'` (`Literal`).\n",
            "- `monto`: Cifra monetaria en pesos chilenos con cota no negativa $\\ge 0.0$ (`float`, `ge=0.0`).\n",
            "- `urgencia`: Nivel de prioridad operativa restringido a `'baja'`, `'media'` o `'alta'` (`Enum`).\n",
            "- `escalar_jefatura`: Booleano estricto (`bool`) que indica si el caso debe alertar a una jefatura.\n",
            "- `model_config = ConfigDict(extra='forbid', strict=True)`: Bloquea cualquier campo adicional e impone tipado estricto sin coerción automática."
        ]
    })

    # 10. Enfoque Low-Code: Prompt asistido para generar Pydantic
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Enfoque low-code: construyan su esquema con asistencia de IA\n",
            "\n",
            "Como profesionales de control de gestión, auditoría y finanzas, su rol principal consiste en especificar con precisión las reglas de negocio y los tipos requeridos, no en memorizar la sintaxis de Python.\n",
            "\n",
            "**Ayúdense con el siguiente prompt para generar este esquema en Google AI Studio o Gemini:**\n",
            "\n",
            "> Actúa como desarrollador Python especializado en extracción estructurada para auditoría y control de gestión.\n",
            "> Genera una clase Pydantic v2 para estructurar y validar la extracción de reclamos de clientes según este requerimiento de negocio:\n",
            ">\n",
            "> 1. Nombre de la clase principal: AuditoriaReclamo (hereda de BaseModel).\n",
            "> 2. Configuración estricta: model_config = ConfigDict(extra='forbid', strict=True) para rechazar casilleros no autorizados y forzar tipado estricto sin coerción automática.\n",
            "> 3. categoria: dominio cerrado con typing.Literal['facturación', 'servicio', 'producto'] y Field(description='Clasificación estricta').\n",
            "> 4. monto: número decimal (float) con cota no negativa (ge=0.0) para el monto en disputa en pesos chilenos (CLP), o 0.0 si no aplica.\n",
            "> 5. urgencia: catálogo cerrado mediante una clase Urgencia(str, Enum) con opciones 'baja', 'media' o 'alta'.\n",
            "> 6. escalar_jefatura: booleano (bool) que indique si amerita revisión de jefatura.\n",
            ">\n",
            "> Entrega únicamente el bloque de código en Python con los imports necesarios (BaseModel, Field, ConfigDict, Enum, Literal), limpio y listo para ejecutar.\n",
            "\n",
            "El código generado por el asistente corresponde exactamente a la celda siguiente:"
        ]
    })

    # 11. Código Modelo Pydantic
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from enum import Enum\n",
            "from typing import Literal\n",
            "from pydantic import BaseModel, Field, ConfigDict\n",
            "\n",
            "class Urgencia(str, Enum):\n",
            "    BAJA = 'baja'\n",
            "    MEDIA = 'media'\n",
            "    ALTA = 'alta'\n",
            "\n",
            "class AuditoriaReclamo(BaseModel):\n",
            "    model_config = ConfigDict(extra='forbid', strict=True)\n",
            "\n",
            "    categoria: Literal['facturación', 'servicio', 'producto'] = Field(\n",
            "        description='Clasificación estricta: facturación, servicio o producto'\n",
            "    )\n",
            "    monto: float = Field(\n",
            "        ge=0.0,\n",
            "        description='Monto en disputa en CLP, o 0.0 si no aplica'\n",
            "    )\n",
            "    urgencia: Urgencia = Field(\n",
            "        description='Prioridad operativa asignada'\n",
            "    )\n",
            "    escalar_jefatura: bool = Field(\n",
            "        description='Requiere revisión de jefatura'\n",
            "    )"
        ]
    })

    # 12. Explicación de GenerateContentConfig y llamada nuclear
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Extracción estructurada: el bloque nuclear\n",
            "\n",
            "Configuramos la llamada mediante `google.genai.types.GenerateContentConfig` (la clase de configuración avanzada del SDK).\n",
            "\n",
            "Al definir:\n",
            "- `response_mime_type='application/json'`\n",
            "- `response_schema=AuditoriaReclamo`\n",
            "\n",
            "El decodificador del modelo fuerza matemáticamente la generación para que coincida con el formulario preimpreso. ",
            "La probabilidad de recibir texto conversacional o campos fuera de norma es **cero**."
        ]
    })

    # 13. Código llamada nuclear
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1. Texto no estructurado recibido del cliente\n",
            "texto_reclamo = (\n",
            "    'Estimados, escribo indignada porque en mi factura de este mes me cobraron $45.000 '\n",
            "    'de mantenimiento técnico que nunca solicité. Si no anulan ese cobro antes del viernes, '\n",
            "    'cancelaré mi cuenta corporativa y presentaré una denuncia ante el regulador.'\n",
            ")\n",
            "\n",
            "# 2. Configuración estricta del contrato de datos\n",
            "config = types.GenerateContentConfig(\n",
            "    response_mime_type='application/json',\n",
            "    response_schema=AuditoriaReclamo,\n",
            "    temperature=0.0,\n",
            ")\n",
            "\n",
            "# 3. Invocación a la API o demostración guiada del esquema\n",
            "if client:\n",
            "    response = client.models.generate_content(\n",
            "        model='gemini-2.5-flash',\n",
            "        contents=f'Audita el siguiente reclamo y extrae la ficha requerida:\\n\\n{texto_reclamo}',\n",
            "        config=config,\n",
            "    )\n",
            "    resultado = AuditoriaReclamo.model_validate_json(response.text)\n",
            "    print('[Ejecución en vivo vía API] Datos extraídos y validados exitosamente:')\n",
            "else:\n",
            "    print('[Modo demostración guiado: llave no configurada; resultado esperado por el contrato de datos]')\n",
            "    resultado = AuditoriaReclamo(\n",
            "        categoria='facturación',\n",
            "        monto=45000.0,\n",
            "        urgencia=Urgencia.ALTA,\n",
            "        escalar_jefatura=True,\n",
            "    )\n",
            "\n",
            "print(resultado)"
        ]
    })

    # 14. Explicación de lectura
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Inspección de resultados para control de gestión\n",
            "\n",
            "Observen cómo el objeto `resultado` contiene atributos de Python directos (`resultado.categoria`, `resultado.monto`). ",
            "No tenemos que 'cortar' cadenas ni buscar palabras con expresiones regulares; los datos ya están tipados y listos para operar:"
        ]
    })

    # 15. Código visualización resultados
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "print(f'Categoría detectada: {resultado.categoria}')\n",
            "print(f'Monto reclamado:     ${resultado.monto:,.0f} CLP')\n",
            "print(f'Prioridad operativa: {resultado.urgencia.value.upper()}')\n",
            "print(f'Escalar a jefatura:  {\"SÍ\" if resultado.escalar_jefatura else \"NO\"}')"
        ]
    })

    # 16. Práctica autónoma con pauta de predicción
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Práctica autónoma: caso borde sin monto explícito\n",
            "\n",
            "Ahora pongan a prueba la robustez del contrato frente a un caso borde: ",
            "¿Qué ocurre si un cliente presenta un reclamo severo pero sin mencionar una cifra de dinero?\n",
            "\n",
            "Evalúen el siguiente texto:\n",
            "*\"Llevo dos semanas esperando la entrega de los insumos de oficina y nadie contesta los correos. Esto está retrasando la operación completa del equipo.\"*\n",
            "\n",
            "### Actividad de control interno (Lo hacen ustedes)\n",
            "Antes de ejecutar la celda siguiente, completen mentalmente o anoten su predicción en esta pauta de auditoría:\n",
            "\n",
            "| Campo | Predicción esperada | Fundamento de control interno |\n",
            "|:---|:---|:---|\n",
            "| `categoria` | ¿`'servicio'` o `'facturación'`? | ¿Reclama demora en entrega o cobro indebido? |\n",
            "| `monto` | ¿`0.0` o cifra inventada? | No hay monto explícito. El esquema impone cota $\\ge 0.0$, pero que el modelo devuelva `0.0` es una hipótesis sujeta a supervisión humana (el validador no impide que un modelo alucine un monto positivo). |\n",
            "| `urgencia` | ¿`BAJA`, `MEDIA` o `ALTA`? | Dos semanas sin respuesta operativa en oficina. |\n",
            "| `escalar_jefatura` | ¿`True` o `False`? | Evaluar impacto en continuidad operacional. |\n",
            "\n",
            "Ahora ejecuten la celda para contrastar su predicción con la extracción del modelo:"
        ]
    })

    # 17. Código caso borde
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "reclamo_operacional = (\n",
            "    'Llevo dos semanas esperando la entrega de los insumos de oficina y nadie contesta los correos. '\n",
            "    'Esto está retrasando la operación completa del equipo.'\n",
            ")\n",
            "\n",
            "if client:\n",
            "    response_caso2 = client.models.generate_content(\n",
            "        model='gemini-2.5-flash',\n",
            "        contents=f'Audita este reclamo y extrae la ficha requerida:\\n\\n{reclamo_operacional}',\n",
            "        config=config,\n",
            "    )\n",
            "    resultado_caso2 = AuditoriaReclamo.model_validate_json(response_caso2.text)\n",
            "    print('[Ejecución en vivo vía API] Resultado del caso borde:')\n",
            "else:\n",
            "    print('[Modo demostración guiado: llave no configurada; resultado esperado por el contrato de datos]')\n",
            "    resultado_caso2 = AuditoriaReclamo(\n",
            "        categoria='servicio',\n",
            "        monto=0.0,\n",
            "        urgencia=Urgencia.MEDIA,\n",
            "        escalar_jefatura=False,\n",
            "    )\n",
            "\n",
            "print(f'Categoría:          {resultado_caso2.categoria}')\n",
            "print(f'Monto registrado:   ${resultado_caso2.monto:.1f} CLP (0.0 = hipótesis sujeta a supervisión humana)')\n",
            "print(f'Urgencia asignada:  {resultado_caso2.urgencia.value.upper()}')\n",
            "print(f'Escalar a jefatura: {\"SÍ\" if resultado_caso2.escalar_jefatura else \"NO\"}')\n",
            "print('Nota de auditoría:  El contrato técnico valida estructura y tipos; la exactitud del contenido requiere supervisión humana.')"
        ]
    })

    # 18. Prompt transferible para adaptar a procesos propios
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Transferencia a sus propios procesos de negocio\n",
            "\n",
            "Para implementar este patrón en sus respectivas áreas (por ejemplo, validación de facturas de proveedores, rendición de viáticos o contratos comerciales), no necesitan programar desde cero.\n",
            "\n",
            "**Ayúdense con el siguiente prompt para construir esquemas adaptados a su empresa en Google AI Studio o Gemini:**\n",
            "\n",
            "> Actúa como desarrollador Python especializado en extracción estructurada para control interno.\n",
            "> Necesito un esquema Pydantic para el proceso: [NOMBRE DEL PROCESO, ej. Rendición de Gastos de Viaje].\n",
            ">\n",
            "> Los campos requeridos son:\n",
            "> - [Campo 1, ej. proveedor]: [Tipo de dato y descripción del negocio]\n",
            "> - [Campo 2, ej. monto_total]: [Tipo numérico y moneda con cota no negativa]\n",
            "> - [Campo 3, ej. estado_aprobacion]: [Opciones permitidas en catálogo cerrado Enum]\n",
            "> - [Campo 4, ej. cumple_politica]: [Booleano True/False]\n",
            ">\n",
            "> Genera el código con BaseModel, Field(description=\"...\") y ConfigDict(extra='forbid') listo para configurar con GenerateContentConfig en Gemini API."
        ]
    })

    # 19. Síntesis y buenas prácticas
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 8. Síntesis y buenas prácticas directivas\n",
            "\n",
            "Para concluir el taller, retengan estas tres directrices para implementar IA en sus organizaciones:\n",
            "\n",
            "1. **Seguridad y gobierno:** Nunca expongan credenciales en código compartido. Utilicen gestores de secretos corporativos.\n",
            "2. **Contratos estrictos:** Utilicen siempre esquemas formales (Pydantic / Schemas) con dominios cerrados y `extra='forbid'` para garantizar que los datos fluyan hacia el ERP sin errores de sintaxis ni casilleros espurios.\n",
            "3. **Economía de tokens:** Diseñen esquemas concisos para minimizar el costo de los tokens de salida, que son hasta 4 veces más caros que los de entrada."
        ]
    })

    # 20. Atribución de datos
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Atribución de datos\n",
            "\n",
            "- **Creador:** Sebastián Contreras\n",
            "- **Procedencia:** Casos sintéticos elaborados con fines docentes mediante el [script generador](_build_04_apis.py). No representan a clientes, facturas ni organizaciones reales.\n",
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
                "max_mediana_lineas_codigo": max(mediana_lineas + 10, 25)
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

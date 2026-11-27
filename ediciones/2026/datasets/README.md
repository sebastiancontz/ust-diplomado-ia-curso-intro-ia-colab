# Datasets de la edición

Mantener una fila por dataset que se publique o use en una clase. El chequeo identifica un dato
sintético por la palabra **Sintético** en su fila.

| Archivo | Creador, origen y procedencia | Licencia | Usado en |
|---|---|---|---|
| [01-triaje-bancario.csv](01-triaje-bancario.csv) | **Sintético**, creado por Sebastián Contreras; [script generador](_generar_casos_01.py). No representa una organización real. | No declarada | Clase 01 |
| [02-boleta-sintetica.png](02-boleta-sintetica.png) | **Sintético**, creado por Sebastián Contreras con el generador `_generar_boleta_02.py`. Boleta de un restaurante ficticio, con el día de la fecha manchado a propósito. No representa una organización real. | No declarada | Clase 02 |
| [05-documentos/](05-documentos/) | **Sintético**, creado por Sebastián Contreras con el generador `_generar_documentos_05.py`. Paquete documental en PDF de una empresa ficticia: la política de gastos de la Clase 02, cinco comprobantes (161 a 165; al 162 una mancha le tapa la fecha), una minuta de comité y un extracto de contrato, más versiones minimizadas del comprobante 165, la minuta y el contrato. Omite datos a propósito y trae datos personales ficticios para practicar la minimización. No representa una organización real. | No declarada | Clase 05 |

Para datos de terceros, documentar fuente y licencia efectivas. Para un dato propio sintético, escribir
**Sintético**, enlazar el script generador `.py` y declarar que no representa una organización real. Si
el titular no ha declarado una licencia para ese dato, indicar `No declarada`; no inventar una condición
legal para completar la tabla.

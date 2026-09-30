# Proyecto 1: análisis comercial de TechRD

## Pregunta del negocio

¿Qué productos aportan más utilidad bruta, cómo varían las ventas por mes y cómo se distribuyen entre canales y ciudades?

## Proceso

1. **Extracción:** lectura del CSV con codificación UTF-8 y soporte para BOM.
2. **Validación:** campos obligatorios, fecha válida, cantidades enteras positivas, importes no negativos y descuento entre 0 y 100.
3. **Limpieza:** eliminación de espacios; normalización de números y fechas. Se conserva la primera fila válida de cada ID y se rechazan las demás con motivos diferenciados para duplicados y conflictos.
4. **Cuarentena:** filas rechazadas con número de línea, motivo y fila original serializada. No se rellenan campos faltantes inventando valores.
5. **Transformación:** importes monetarios en centavos; descuento redondeado por venta a medio centavo hacia arriba.
6. **Carga:** base SQLite con clave primaria e índice de fecha.
7. **Análisis:** consultas agregadas y de ventana; reporte con filtros e indicadores.
8. **Comunicación:** hallazgos, decisiones propuestas y límites de interpretación.

## Archivos principales

| Archivo | Uso |
|---|---|
| generar_datos.py | Genera 720 ventas ficticias y añade 17 filas problemáticas; semilla 42 |
| datos/ventas_demo.csv | Entrada de demostración: enero–agosto de 2026 |
| analizar.py | ETL, indicadores y exportación |
| consultas.sql | Cuatro consultas de negocio, incluida variación mensual con LAG |
| plantilla.html | Interfaz del reporte, sin servicios externos |
| salidas/ | Resultados listos para revisar |
| test_analizar.py | Cinco pruebas de calidad y resultados |

## Diccionario de datos de entrada

| Campo | Definición |
|---|---|
| id_venta | Identificador único de una venta de un solo producto |
| fecha | Fecha AAAA-MM-DD |
| producto, categoria | Descripciones no vacías; no se unifican automáticamente variantes de escritura |
| ciudad, canal | Ubicación y canal; texto no vacío |
| cantidad | Entero entre 1 y 1,000,000 |
| precio_unitario, costo_unitario | DOP por unidad, hasta dos decimales; punto decimal sin separador de miles |
| descuento_pct | Porcentaje de descuento de 0 a 100 |

Los campos calculados `ingreso_centavos`, `costo_centavos` y `utilidad_centavos` son enteros en centavos de DOP. Para mostrarlos en pesos se dividen entre 100.

## Indicadores

- Ingresos: cantidad × precio × (1 − descuento / 100).
- Utilidad bruta: ingresos − cantidad × costo unitario.
- Margen bruto: suma de utilidades / suma de ingresos × 100. No es el promedio simple de márgenes.
- Ticket promedio: ingresos / ventas válidas. En este dataset cada fila es una venta completa de un único producto.

No existe estacionalidad demostrada: solo hay ocho meses de datos sintéticos. Un cambio mensual es descriptivo y no demuestra el efecto de una campaña.

## Resultados de referencia

737 filas recibidas; 720 aceptadas; 12 duplicados exactos y 5 filas inválidas rechazadas. Ingresos RD$19,991,697.50; utilidad bruta RD$5,130,747.50; margen 25.66%; ticket RD$27,766.25.

## Ejecución

Desde esta subcarpeta: `python analizar.py`. Para otro CSV: `python analizar.py --entrada ruta.csv --salida resultados`.

Puedes importar `salidas/ventas_limpias.csv` en Excel o Power BI. Si lo haces, utiliza UTF-8, coma como delimitador y configuración numérica que reconozca el punto decimal. Los campos terminados en `_centavos` deben dividirse entre 100 para expresarlos como moneda.

## Mejoras para practicar

- Implementar el mismo ETL con pandas y comparar resultados con las pruebas existentes.
- Añadir dimensiones producto, ciudad y fecha para construir un modelo estrella.
- Crear un reporte en Power BI con medidas equivalentes y validar sus totales.
- Incorporar devoluciones y pedidos con varias líneas; separar id_pedido de id_linea antes de recalcular el ticket.

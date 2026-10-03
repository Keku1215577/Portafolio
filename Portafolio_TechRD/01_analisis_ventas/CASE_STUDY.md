# Caso de estudio: análisis comercial de TechRD

## Resumen ejecutivo

Este proyecto construye un flujo reproducible para transformar registros de ventas en información comercial. El trabajo cubre validación de calidad, limpieza, transformación, almacenamiento en SQLite, consultas SQL, generación de indicadores y comunicación de hallazgos.

Los datos utilizados son sintéticos y fueron creados exclusivamente para demostrar el proceso técnico.

## Problema de negocio

El objetivo es responder:

1. Qué productos generan mayor utilidad bruta.
2. Cómo evolucionan los ingresos por mes.
3. Cómo se distribuyen las ventas entre canales y ciudades.
4. Qué problemas de calidad existen en los datos antes del análisis.

## Datos y calidad

| Indicador | Resultado |
|---|---:|
| Filas recibidas | 737 |
| Filas válidas | 720 |
| Filas rechazadas | 17 |
| Duplicados exactos | 12 |
| Filas inválidas | 5 |

Las filas rechazadas no se eliminan silenciosamente. Se almacenan en una salida de cuarentena con el número de línea, el motivo y la fila original para facilitar revisión y auditoría.

## Proceso ETL

### 1. Extracción

Se lee un archivo CSV con soporte para codificación UTF-8 y BOM.

### 2. Validación

Se validan:

- campos obligatorios;
- fechas;
- cantidades;
- precios y costos;
- porcentaje de descuento;
- identificadores de venta.

### 3. Limpieza

Se normalizan espacios, fechas y valores numéricos. Los registros duplicados o en conflicto se identifican explícitamente.

### 4. Transformación

Los importes monetarios se representan como centavos enteros. Esto permite evitar errores de representación típicos de los números de punto flotante.

### 5. Carga

Los registros válidos se cargan en SQLite con clave primaria e índice de fecha.

### 6. Análisis

Se utilizan consultas SQL agregadas y funciones de ventana para obtener métricas comerciales y variaciones mensuales.

### 7. Comunicación

Los resultados se presentan mediante un dashboard HTML, archivos de salida y documentación técnica.

## Indicadores principales

| Métrica | Resultado |
|---|---:|
| Ingresos | RD$19,991,697.50 |
| Utilidad bruta | RD$5,130,747.50 |
| Margen bruto | 25.66% |
| Ticket promedio | RD$27,766.25 |
| Producto con mayor utilidad bruta | Laptop 14 |
| Utilidad bruta de Laptop 14 | RD$3,222,450.00 |

### Fórmulas

**Ingresos**

`cantidad × precio_unitario × (1 − descuento_pct / 100)`

**Costo**

`cantidad × costo_unitario`

**Utilidad bruta**

`ingresos − costo`

**Margen bruto**

`utilidad_bruta / ingresos × 100`

**Ticket promedio**

`ingresos / ventas_validas`

## Hallazgos

El producto con mayor utilidad bruta acumulada en el dataset es **Laptop 14**, con RD$3,222,450.00.

La calidad del dato es una etapa importante del análisis: 17 de las 737 filas recibidas no llegaron al conjunto analítico final. Separar estas filas permite evitar que los problemas de origen queden ocultos y facilita su revisión posterior.

Los cambios mensuales deben interpretarse como resultados descriptivos del dataset. No permiten concluir causalidad, estacionalidad ni impacto de campañas comerciales.

## Decisión propuesta

Antes de realizar una decisión de reposición, conviene revisar conjuntamente:

- utilidad aportada;
- unidades vendidas;
- rotación;
- inventario disponible;
- evolución mensual;
- canal de venta;
- demanda histórica.

El análisis no recomienda comprar únicamente porque un producto tenga mayor utilidad. El dato debe combinarse con inventario y comportamiento de demanda.

## Tecnologías

Python, SQL, SQLite, CSV, HTML y testing.

## Reproducibilidad

Ejecutar desde la carpeta del proyecto:

`python analizar.py`

El proceso genera las salidas en la carpeta `salidas/`.

También se puede abrir directamente el dashboard:

`salidas/dashboard.html`

## Valor profesional demostrado

Este proyecto demuestra un flujo completo de análisis y tratamiento de datos:

**Datos sin procesar → validación → limpieza → transformación → almacenamiento → SQL → métricas → dashboard → hallazgos**

La principal evidencia no es únicamente el resultado final, sino la trazabilidad del proceso utilizado para obtenerlo.

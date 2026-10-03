# Caso de estudio: análisis comercial de TechRD

## Resumen ejecutivo

Este proyecto construye un flujo reproducible para transformar registros de ventas en información comercial. El trabajo cubre validación de calidad, limpieza, transformación, almacenamiento en SQLite, consultas SQL, indicadores, dashboard y comunicación de hallazgos.

Los datos utilizados son sintéticos y fueron creados exclusivamente para demostrar el proceso técnico.

## Problema de negocio

El objetivo es responder:

1. Qué productos generan mayor utilidad bruta.
2. Cómo evolucionan los ingresos por mes.
3. Cómo se distribuyen los resultados entre canales y ciudades.
4. Qué problemas de calidad existen en los datos antes del análisis.

## Datos y calidad

| Indicador | Resultado |
|---|---:|
| Filas recibidas | 737 |
| Filas válidas | 720 |
| Filas rechazadas | 17 |
| Duplicados exactos | 12 |
| Filas inválidas | 5 |

Las filas rechazadas se conservan en una salida de cuarentena con número de línea, motivo y fila original para facilitar revisión y auditoría.

## Proceso ETL

### 1. Extracción

Lectura de un CSV con soporte para UTF-8 y BOM.

### 2. Validación

Se revisan campos obligatorios, fechas, cantidades, precios, costos, descuentos e identificadores de venta.

### 3. Limpieza

Se normalizan espacios, fechas y valores numéricos. Los registros duplicados o en conflicto se identifican explícitamente.

### 4. Transformación

Los importes monetarios se representan como centavos enteros para reducir problemas de precisión numérica.

### 5. Carga

Los registros válidos se cargan en SQLite con clave primaria e índice de fecha.

### 6. Análisis

Se utilizan consultas agregadas y funciones de ventana para calcular indicadores comerciales, variaciones y comparaciones.

### 7. Comunicación

Los resultados se presentan mediante dashboard HTML, consultas SQL, archivos de salida y documentación.

## Indicadores principales

| Métrica | Resultado |
|---|---:|
| Ingresos | RD$19,991,697.50 |
| Utilidad bruta | RD$5,130,747.50 |
| Margen bruto | 25.66% |
| Ticket promedio | RD$27,766.25 |
| Producto con mayor utilidad bruta | Laptop 14 |
| Utilidad bruta de Laptop 14 | RD$3,222,450.00 |

## Insights de negocio

### 1. Alta concentración de ingresos

**Laptop 14 representa aproximadamente 71% de los ingresos del dataset**, con RD$14,194,950.00.

Esto indica una fuerte concentración del ingreso en un producto. Sin embargo, su margen bruto es de **22.70%**, inferior al margen global de 25.66%.

### 2. Margen y contribución no significan lo mismo

**Mouse USB alcanza un margen bruto de 53.30%**, el más alto entre los productos analizados, pero genera únicamente RD$222,950.00 en ingresos.

El contraste demuestra por qué no conviene evaluar un producto únicamente por margen porcentual. Para decisiones comerciales también importa la contribución absoluta y el volumen.

### 3. Canales relativamente equilibrados

| Canal | Ingresos | Participación | Margen |
|---|---:|---:|---:|
| Tienda | RD$10,082,000.00 | 50.43% | 26.26% |
| Online | RD$9,909,697.50 | 49.57% | 25.06% |

El canal Tienda presenta una ventaja pequeña tanto en ingresos como en margen. La diferencia no es suficientemente grande para afirmar que un canal sea universalmente superior sin analizar costos operativos y comportamiento del cliente.

### 4. La Romana concentra la mayor cantidad de ingresos

| Ciudad | Ingresos | Participación | Margen |
|---|---:|---:|---:|
| La Romana | RD$7,926,980.00 | 39.65% | 25.75% |
| Santiago | RD$7,135,837.50 | 35.69% | 25.23% |
| Santo Domingo | RD$4,928,880.00 | 24.65% | 26.17% |

La Romana es la ciudad con mayor participación de ingresos en este dataset. Santo Domingo, aunque presenta menor volumen, tiene el mayor margen entre las tres ciudades.

### 5. Calidad del dato

17 de las 737 filas recibidas no llegaron al conjunto analítico final. La cuarentena permite identificar los problemas sin mezclar registros inválidos con los indicadores.

## Decisiones propuestas

Para una decisión de inventario o compras no conviene utilizar únicamente el producto líder por ingresos o utilidad. Debe revisarse conjuntamente:

- utilidad absoluta;
- margen;
- unidades vendidas;
- rotación;
- inventario disponible;
- evolución mensual;
- canal;
- ciudad;
- demanda histórica.

## Fórmulas

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

## Limitaciones

Los datos son sintéticos y cubren ocho meses. Los cambios mensuales son descriptivos y no demuestran estacionalidad, causalidad ni impacto de campañas comerciales.

No se modelan impuestos, devoluciones, gastos operativos, clientes ni pedidos con múltiples líneas.

## Valor profesional demostrado

El proyecto demuestra un flujo completo:

**datos sin procesar → calidad → ETL → almacenamiento → SQL → indicadores → visualización → insights → decisión**

La evidencia principal es la trazabilidad del proceso y la capacidad de explicar por qué cada transformación y métrica fue utilizada.

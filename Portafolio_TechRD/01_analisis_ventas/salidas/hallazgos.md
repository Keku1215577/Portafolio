# Análisis de ventas — TechRD

Dataset de demostración; no representa una empresa real.

## Resultados

- Filas recibidas: 737.
- Filas válidas: 720.
- Filas rechazadas: 17.
- Ingresos después de descuentos: RD$ 19,991,697.50.
- Utilidad bruta: RD$ 5,130,747.50.
- Margen bruto: 25.66%.
- Ticket promedio: RD$ 27,766.25.

## Hallazgos

- Laptop 14 genera RD$ 3,222,450.00 de utilidad bruta y representa aproximadamente el 71% de los ingresos.
- Laptop 14 tiene un margen bruto de 22.70%, por debajo del margen global.
- Mouse USB tiene el mayor margen bruto, 53.30%, pero un volumen de ingresos mucho menor.
- Tienda concentra 50.43% de los ingresos y un margen de 26.26%.
- Online concentra 49.57% de los ingresos y un margen de 25.06%.
- La Romana representa 39.65% de los ingresos y es la ciudad con mayor volumen.
- Santo Domingo tiene el mayor margen entre las tres ciudades, 26.17%.

## Interpretación

Los resultados muestran que volumen, utilidad absoluta y margen porcentual responden preguntas diferentes. Para decisiones de inventario, precios o promoción conviene combinar estos indicadores con rotación, inventario y demanda.

## Decisión propuesta

Revisar disponibilidad y reposición de los productos con mayor contribución, especialmente Laptop 14, pero contrastar con rotación, inversión y demanda antes de comprar. Comparar Tienda y Online y priorizar ciudades según demanda y rentabilidad.

Estos resultados describen el dataset y no demuestran causalidad.

## Definiciones y límites

Cada fila válida es una venta de un único producto; id_venta es único. Ingresos = cantidad × precio × (1 − descuento/100), redondeado a centavos por venta. Costo = cantidad × costo unitario. Utilidad bruta = ingresos − costo. Margen = utilidad bruta / ingresos. Ticket promedio = ingresos / ventas. No se modelan impuestos, devoluciones ni gastos operativos; utilidad bruta no es beneficio neto. Moneda: DOP (RD$).

Los IDs repetidos conservan la primera fila válida y rechazan las posteriores. Los conflictos quedan identificados para revisión; no se supone que la primera fila sea la versión correcta del negocio. Las filas incompletas o inválidas se ponen en cuarentena sin imputar valores.

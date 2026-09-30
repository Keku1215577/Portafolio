# Análisis de ventas — TechRD

Dataset de demostración; no representa una empresa real.

- Filas recibidas: 737. Válidas: 720. Rechazadas: 17.
- Ingresos después de descuentos: RD$ 19,991,697.50.
- Utilidad bruta: RD$ 5,130,747.50. Margen bruto: 25.66%.
- El producto con mayor utilidad bruta total es Laptop 14: RD$ 3,222,450.00.

## Decisión propuesta
Revisar disponibilidad y reposición del producto que más aporta a la utilidad; contrastar con rotación, inversión y demanda antes de comprar. Comparar Online y Tienda con los filtros del dashboard. Estos resultados describen el dataset; no demuestran causalidad.

## Definiciones y límites
Cada fila válida es una venta de un único producto; id_venta es único. Ingresos = cantidad × precio × (1 − descuento/100), redondeado a centavos por venta. Costo = cantidad × costo unitario. Utilidad bruta = ingresos − costo. Margen = utilidad bruta / ingresos. Ticket promedio = ingresos / ventas. No se modelan impuestos, devoluciones ni gastos operativos; utilidad bruta no es beneficio neto. Moneda: DOP (RD$).

Los IDs repetidos conservan la primera fila válida y rechazan las posteriores. Los conflictos quedan identificados para revisión; no se supone que la primera fila sea la versión correcta del negocio. Las filas incompletas o inválidas se ponen en cuarentena sin imputar valores.

# Diseño visual del dashboard

## Identidad visual

- Estilo: empresarial, limpio y orientado a decisiones.
- Fondo: blanco o gris muy claro.
- Color principal: azul marino.
- Color secundario: turquesa.
- Color de advertencia: naranja para entregas tardías.
- Tipografía: Segoe UI.
- Espaciado consistente, sin elementos decorativos innecesarios.
- Todas las páginas deben incluir título, período seleccionado y acceso claro a navegación.

## Página 1 — Resumen ejecutivo

### Filtros
- Fecha de compra.
- Estado del pedido.
- Estado/región del cliente.
- Categoría del producto.

### Tarjetas KPI
- Ventas de productos en pedidos entregados.
- Pedidos entregados.
- Clientes únicos.
- Ticket promedio de pedido entregado.
- Porcentaje de pedidos entregados a tiempo.
- Puntuación promedio de reseñas.

### Visuales
- Línea: ventas de productos por mes.
- Barras: ventas por categoría.
- Barras horizontales: estados con más ventas.
- Dona o barras: distribución de estados de pedidos.
- Tabla de resumen por mes con ventas, pedidos y ticket promedio.

## Página 2 — Ventas y catálogo

### Filtros
- Fecha de compra.
- Categoría.
- Vendedor.
- Estado/región.

### Visuales
- Tendencia mensual de ventas de productos.
- Ranking de categorías por ventas.
- Ranking de productos por ventas.
- Ranking de vendedores por ventas de productos.
- Flete por categoría y región.
- Tabla detallada de categorías con ventas y participación.

## Página 3 — Clientes y mercados

### Visuales
- Pedidos y ventas por estado del cliente.
- Clientes únicos por período.
- Ticket promedio por región.
- Ciudades con mayor cantidad de pedidos.
- Tabla de rendimiento por región.

Nota: un mismo cliente puede tener varios pedidos; utilizar `customer_unique_id` para contar personas únicas y no el identificador técnico `customer_id`.

## Página 4 — Logística y satisfacción

### Tarjetas KPI
- Días promedio desde la compra hasta la entrega.
- Entregas a tiempo.
- Entregas tardías.
- Puntuación promedio de reseña.

### Visuales
- Tendencia de días de entrega por mes.
- Entregas tardías por estado.
- Distribución de puntuaciones de reseña.
- Puntuación media frente a entrega a tiempo/tardía.
- Tabla de pedidos entregados con fechas estimadas y reales.

La comparación entre demora y reseña es descriptiva; no demuestra causalidad.

## Interacciones

- Filtros sincronizados entre páginas cuando tengan significado compatible.
- Tooltips con el período, el valor y la definición del KPI.
- Drill-through opcional de región a ciudad.
- Botón de restablecer filtros.
- Navegación por botones o marcadores.

## Reglas de interpretación

- Las ventas de productos se calculan a partir de `order_items[price]`.
- El flete se calcula por separado desde `order_items[freight_value]`.
- Los pagos se analizan desde la tabla de pagos, sin sumarlos en el mismo cálculo que los artículos para evitar duplicaciones por relaciones uno-a-muchos.
- No hay costo del producto, así que no se debe presentar utilidad o margen de beneficio.

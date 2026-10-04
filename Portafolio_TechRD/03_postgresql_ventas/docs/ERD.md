# Modelo de datos

## Entidades

### categories

Catálogo de categorías de productos.

### products

Productos comercializados. Mantiene precio, costo y categoría.

### customers

Clientes y su ciudad de referencia.

### orders

Cabecera de cada pedido, con fecha, cliente, canal y estado.

### order_items

Detalle de cada pedido. Conserva cantidad, precio aplicado y descuento de cada línea.

## Relaciones

```text
categories (1) ---- (N) products
customers  (1) ---- (N) orders
orders     (1) ---- (N) order_items
products   (1) ---- (N) order_items
```

## Decisiones de diseño

- Las tablas separan catálogos, clientes, pedidos y detalle de pedidos.
- Las claves foráneas protegen la integridad referencial.
- Las columnas monetarias utilizan NUMERIC en lugar de tipos flotantes.
- Las restricciones CHECK evitan cantidades negativas y descuentos fuera de rango.
- Los índices se agregan a columnas utilizadas frecuentemente en relaciones y filtros.

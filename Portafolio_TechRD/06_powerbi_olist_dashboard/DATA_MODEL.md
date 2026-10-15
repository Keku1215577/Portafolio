# Modelo de datos para Power BI

## Tablas

- `Orders`: una fila por pedido, con estado y marcas de tiempo.
- `Order Items`: detalle de cada artículo en un pedido, con precio y flete.
- `Customers`: ubicación del cliente y `customer_unique_id`.
- `Products`: categoría y atributos del producto.
- `Sellers`: ubicación del vendedor.
- `Payments`: registros de pago por pedido.
- `Reviews`: reseñas asociadas al pedido.
- `Category Translation`: traducción de categorías.
- `Date`: calendario creado en Power BI.

## Relaciones recomendadas

| Desde | Hacia | Cardinalidad esperada | Dirección |
|---|---|---|---|
| Customers[customer_id] | Orders[customer_id] | 1 a 1 o 1 a muchos, comprobar cardinalidad al cargar | Simple |
| Orders[order_id] | Order Items[order_id] | 1 a muchos | Simple |
| Products[product_id] | Order Items[product_id] | 1 a muchos | Simple |
| Sellers[seller_id] | Order Items[seller_id] | 1 a muchos | Simple |
| Orders[order_id] | Payments[order_id] | 1 a muchos | Simple |
| Orders[order_id] | Reviews[order_id] | 1 a muchos | Simple |
| Category Translation[product_category_name] | Products[product_category_name] | 1 a muchos | Simple |
| Date[Date] | Orders[Purchase Date] | 1 a muchos | Simple |

Comprueba duplicados y cardinalidad antes de fijar la relación Customers–Orders. No fuerces una relación 1:1 si los datos no cumplen esa condición.

## Columna de fecha de compra

En Power Query, crear `Purchase Date` a partir de `order_purchase_timestamp` como tipo Fecha. La tabla Date se relacionará con esa columna. Se pueden crear relaciones inactivas para analizar fechas de entrega cuando se necesite.

## Modelo y doble conteo

Orders es la tabla central que filtra artículos, pagos y reseñas. No se deben relacionar directamente Order Items con Payments ni sumar campos de las dos tablas en una fila visual común sin medidas controladas; un pedido puede tener varios artículos y varios registros de pago.

## Clientes únicos

`customer_id` es un identificador técnico de la fila de cliente asociado al pedido. Para contar personas se debe usar `customer_unique_id`. Comprueba cómo interactúan los filtros de fecha con esa medida; puede requerir una medida DAX con TREATAS o preparar una tabla de clientes únicos en Power Query.

## Validaciones del modelo

- Comprobar que Orders tiene una sola fila por order_id.
- Comprobar la clave de Products y Sellers.
- Revisar nulos de categoría y traducciones.
- Verificar que Orders a Order Items no pierda registros.
- Validar que las ventas agregadas no cambien incorrectamente al añadir una dimensión.
- Contrastar el total de pagos con ventas y flete como control de calidad, no como medida combinada por fila.

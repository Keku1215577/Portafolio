# Preparación en Power Query

## 1. Descargar los CSV

Utiliza los enlaces de `DATA_SOURCES.md`. Guarda los archivos en una carpeta local, por ejemplo:

```text
C:\PowerBI\Olist\
```

No es necesario descargar geolocalización para la primera versión.

## 2. Importar

En Power BI Desktop:

1. Selecciona **Obtener datos**.
2. Elige **Texto/CSV**.
3. Importa los archivos recomendados.
4. Renombra las consultas con nombres sencillos: Orders, Order Items, Customers, Products, Sellers, Payments, Reviews y Category Translation.

## 3. Tipos de datos

### Orders

- `order_id`, `customer_id`, `order_status`: texto.
- Marcas de tiempo: Fecha/Hora.
- Crear `Purchase Date` como Fecha a partir de `order_purchase_timestamp`.

### Order Items

- `order_id`, `product_id`, `seller_id`: texto.
- `order_item_id`: entero.
- `price` y `freight_value`: decimal fijo o decimal según configuración regional. Configura el locale de origen si fuera necesario.

### Customers y Sellers

- Identificadores: texto.
- Código postal: texto, para preservar ceros iniciales.
- Estado y ciudad: texto.

### Products

- `product_id`, `product_category_name`: texto.
- Peso y dimensiones: numérico.
- Las categorías pueden tener valores nulos.

### Payments

- `order_id`, `payment_type`: texto.
- `payment_sequential`, `payment_installments`: entero.
- `payment_value`: decimal.

### Reviews

- IDs: texto.
- `review_score`: entero.
- Marcas de tiempo: Fecha/Hora.

## 4. Limpieza y validación

- Revisar valores nulos y duplicados en las claves.
- Mantener todos los estados de pedido para análisis de estado, pero utilizar pedidos entregados para los indicadores de ventas entregadas.
- No eliminar cancelaciones sin documentarlo.
- Revisar pedidos sin fecha de entrega.
- Comprobar categoría y traducción.
- Mantener separado el valor de pago del precio de producto y del flete.
- No agregar tablas de detalle entre sí sin comprender el efecto de relaciones uno-a-muchos.

## 5. Modelo

Después de aplicar los cambios, abre la vista Modelo y define las relaciones descritas en `DATA_MODEL.md`. Marca la tabla Date como tabla de fechas y prueba filtros de fecha antes de construir los visuales.

## 6. Primer control de calidad

Comprueba:

- Conteo de pedidos por order_status.
- Suma de `Order Items[price]`.
- Suma de `Order Items[freight_value]`.
- Suma de `Payments[payment_value]`.
- Pedidos entregados por mes.
- Nulos en fechas reales de entrega.

Anota los valores de control para validar las medidas DAX después.

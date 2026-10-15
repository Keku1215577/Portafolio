# Fuente de datos y archivos requeridos

## Fuente principal

Repositorio de Olist: https://github.com/olist/work-at-olist-data

Carpeta CSV: https://github.com/olist/work-at-olist-data/tree/master/datasets

El repositorio incluye archivos CSV extraídos de una muestra relacional de transacciones de comercio electrónico. El README del repositorio original explica el contexto de negocio y los desafíos analíticos.

## Archivos recomendados para la primera versión

| Archivo | Contenido | Uso en Power BI |
|---|---|---|
| `olist_orders_dataset.csv` | Identificador, estado y fechas del pedido | Conteo de pedidos y desempeño de entrega |
| `olist_order_items_dataset.csv` | Artículos, precio y flete | Ventas de productos y flete |
| `olist_customers_dataset.csv` | Cliente, ciudad y estado | Análisis geográfico y clientes únicos |
| `olist_products_dataset.csv` | Categoría y atributos del producto | Ventas por categoría |
| `olist_sellers_dataset.csv` | Identificador y ubicación de vendedor | Análisis de vendedores |
| `olist_order_payments_dataset.csv` | Tipo, cuotas y valor pagado | Métodos y valores de pago |
| `olist_order_reviews_dataset.csv` | Puntuación y fechas de reseñas | Satisfacción |
| `product_category_name_translation.csv` | Traducción de categorías | Etiquetas legibles en inglés |

Se recomienda omitir inicialmente `olist_geolocation_dataset.csv`, ya que es considerablemente más grande y no es necesario para el primer dashboard. Podemos utilizar el estado del cliente para una vista geográfica sencilla.

## Enlaces directos a los CSV

- [Orders](https://github.com/olist/work-at-olist-data/blob/master/datasets/olist_orders_dataset.csv)
- [Order items](https://github.com/olist/work-at-olist-data/blob/master/datasets/olist_order_items_dataset.csv)
- [Customers](https://github.com/olist/work-at-olist-data/blob/master/datasets/olist_customers_dataset.csv)
- [Products](https://github.com/olist/work-at-olist-data/blob/master/datasets/olist_products_dataset.csv)
- [Sellers](https://github.com/olist/work-at-olist-data/blob/master/datasets/olist_sellers_dataset.csv)
- [Payments](https://github.com/olist/work-at-olist-data/blob/master/datasets/olist_order_payments_dataset.csv)
- [Reviews](https://github.com/olist/work-at-olist-data/blob/master/datasets/olist_order_reviews_dataset.csv)
- [Traducción de categorías](https://github.com/olist/work-at-olist-data/blob/master/datasets/product_category_name_translation.csv)

## Procedencia y límites

Los datos son reales, transaccionales y anonimizados, no datos inventados ni registros actuales. El período principal es 2016–2018. No deben describirse como ventas actuales ni como información de una empresa propia.

## Licencia

El dataset original se asocia con CC BY-NC-SA 4.0. Dar atribución a Olist y revisar los términos originales antes de redistribuir los datos o sus adaptaciones.

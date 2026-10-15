# Medidas DAX iniciales

Los nombres de las tablas deben coincidir con los nombres que se asignen durante la importación. Las medidas suponen relaciones activas entre Orders y las tablas indicadas.

## Ventas de productos

```dax
Product Sales =
SUM ( 'Order Items'[price] )
```

```dax
Product Sales - Delivered =
CALCULATE (
    [Product Sales],
    KEEPFILTERS ( Orders[order_status] = "delivered" )
)
```

## Pedidos

```dax
Orders Count =
DISTINCTCOUNT ( Orders[order_id] )
```

```dax
Delivered Orders =
CALCULATE (
    DISTINCTCOUNT ( Orders[order_id] ),
    KEEPFILTERS ( Orders[order_status] = "delivered" )
)
```

```dax
Average Order Value - Delivered =
DIVIDE ( [Product Sales - Delivered], [Delivered Orders], 0 )
```

## Flete

```dax
Freight Value =
SUM ( 'Order Items'[freight_value] )
```

```dax
Freight Value - Delivered =
CALCULATE (
    [Freight Value],
    KEEPFILTERS ( Orders[order_status] = "delivered" )
)
```

## Clientes únicos en pedidos seleccionados

Si la tabla Customers se relaciona con Orders mediante customer_id y el filtro de fecha se aplica sobre Orders, esta medida transfiere los customer_id visibles al contexto de Customers:

```dax
Unique Customers =
CALCULATE (
    DISTINCTCOUNT ( Customers[customer_unique_id] ),
    TREATAS ( VALUES ( Orders[customer_id] ), Customers[customer_id] )
)
```

Verifica esta medida después de crear las relaciones. Si Power Query incorpora customer_unique_id a Orders, la medida puede simplificarse a DISTINCTCOUNT sobre esa columna.

## Reseñas

```dax
Average Review Score =
AVERAGE ( Reviews[review_score] )
```

```dax
Review Count =
DISTINCTCOUNT ( Reviews[review_id] )
```

## Tiempo promedio de entrega

Solo se incluyen pedidos entregados que tienen fecha de compra y fecha real de entrega:

```dax
Average Delivery Days =
AVERAGEX (
    FILTER (
        Orders,
        Orders[order_status] = "delivered"
            && NOT ISBLANK ( Orders[order_purchase_timestamp] )
            && NOT ISBLANK ( Orders[order_delivered_customer_date] )
    ),
    DATEDIFF (
        Orders[order_purchase_timestamp],
        Orders[order_delivered_customer_date],
        DAY
    )
)
```

## Porcentaje de entregas a tiempo

```dax
Delivered Orders With Estimated Date =
CALCULATE (
    DISTINCTCOUNT ( Orders[order_id] ),
    FILTER (
        Orders,
        Orders[order_status] = "delivered"
            && NOT ISBLANK ( Orders[order_delivered_customer_date] )
            && NOT ISBLANK ( Orders[order_estimated_delivery_date] )
    )
)
```

```dax
Delivered On Time =
CALCULATE (
    DISTINCTCOUNT ( Orders[order_id] ),
    FILTER (
        Orders,
        Orders[order_status] = "delivered"
            && NOT ISBLANK ( Orders[order_delivered_customer_date] )
            && NOT ISBLANK ( Orders[order_estimated_delivery_date] )
            && Orders[order_delivered_customer_date]
                <= Orders[order_estimated_delivery_date]
    )
)
```

```dax
On-Time Delivery % =
DIVIDE (
    [Delivered On Time],
    [Delivered Orders With Estimated Date],
    0
)
```

## Nota importante

Estas son medidas iniciales, no indicadores validados definitivamente. Después de importar los datos, deben probarse con distintos filtros y contrastarse contra agregaciones independientes. No calcular utilidad o margen, porque el conjunto de datos no incluye costo de adquisición de cada producto.

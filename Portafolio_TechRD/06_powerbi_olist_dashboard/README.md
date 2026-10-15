# Power BI — Olist E-commerce Performance Dashboard

**Estado:** planificación y preparación del modelo de datos. El archivo PBIX se añadirá cuando el dashboard esté construido y validado en Power BI Desktop.

## Objetivo

Crear un dashboard profesional de Power BI con datos comerciales reales anonimizados del Brazilian E-Commerce Public Dataset de Olist. El informe analizará ventas de productos, pedidos, categorías, clientes, pagos, entregas y reseñas.

## Fuente de datos

Los archivos CSV están disponibles en el repositorio público de Olist:

- Repositorio: https://github.com/olist/work-at-olist-data
- Carpeta de datos: https://github.com/olist/work-at-olist-data/tree/master/datasets
- Contexto del conjunto de datos: https://github.com/olist/work-at-olist-data/blob/master/README.md
- Fuente original del dataset: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

El conjunto contiene aproximadamente 100.000 pedidos de comercio electrónico de Brasil de 2016 a 2018. Los datos son una muestra de transacciones reales y están anonimizados.

## Licencia y atribución

El dataset original de Olist está identificado como **CC BY-NC-SA 4.0** en la documentación de repositorios que lo utilizan. Este proyecto debe incluir atribución a Olist, respetar las condiciones de uso no comercial y compartir cualquier adaptación del conjunto bajo las condiciones correspondientes. Consultar siempre los términos vigentes de la fuente original antes de redistribuir datos.

No se copiarán grandes archivos CSV dentro de este repositorio. Las instrucciones enlazan los archivos de la fuente.

## Tecnologías

- Microsoft Power BI Desktop
- Power Query
- DAX
- Modelado dimensional

## Archivos de planificación

- [Fuente y descargas](DATA_SOURCES.md)
- [Modelo de datos](DATA_MODEL.md)
- [Diseño del dashboard](DASHBOARD_DESIGN.md)
- [Medidas DAX iniciales](DAX_MEASURES.md)
- [Preparación de datos con Power Query](POWER_QUERY_GUIDE.md)

## Alcance analítico

1. Desempeño general de ventas y pedidos.
2. Análisis por fecha, categoría, producto y estado.
3. Distribución por estado/ciudad y análisis de clientes.
4. Desempeño de entrega y satisfacción del cliente.

## Principios de análisis

- Distinguir ventas de productos de valores de pago y flete.
- Excluir cancelaciones de los indicadores de ventas entregadas.
- No calcular utilidad o margen porque el dataset no contiene el costo de adquisición del producto.
- No interpretar asociación entre retrasos y reseñas como causalidad.
- Verificar que las relaciones no dupliquen importes cuando se combinan tablas de hechos.

## Resultado final esperado

Un informe Power BI de varias páginas con navegación clara, KPIs, gráficos comparativos, filtros y documentación de las reglas de cálculo. El archivo PBIX y capturas del dashboard se agregarán después de construir y probar el informe en Power BI Desktop.

Autor: Juan Sebastian De la Cruz Amparo

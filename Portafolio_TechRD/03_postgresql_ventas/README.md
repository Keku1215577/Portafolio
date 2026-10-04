# PostgreSQL Sales Database

Proyecto práctico de modelado y análisis de una base de datos relacional para un negocio de ventas.

## Objetivo

Diseñar una estructura normalizada en PostgreSQL que permita registrar clientes, productos, categorías, pedidos y líneas de pedido, y después utilizar SQL para obtener indicadores comerciales.

## Qué demuestra

- Modelado relacional.
- Claves primarias y foráneas.
- Restricciones de integridad.
- Tipos de datos adecuados para dinero.
- Índices.
- Consultas con JOIN, GROUP BY, HAVING y CTE.
- Funciones de ventana.
- Análisis mensual, por producto, cliente, ciudad y canal.

## Modelo

```text
categories 1 ─── N products
customers  1 ─── N orders
orders     1 ─── N order_items
products   1 ─── N order_items
```

## Estructura

```text
03_postgresql_ventas/
├── README.md
├── docs/
│   └── ERD.md
└── sql/
    ├── 01_schema.sql
    ├── 02_seed.sql
    └── 03_queries.sql
```

## Ejecución

Con PostgreSQL instalado:

1. Crear una base de datos, por ejemplo `portfolio_ventas`.
2. Ejecutar `sql/01_schema.sql`.
3. Ejecutar `sql/02_seed.sql`.
4. Ejecutar las consultas de `sql/03_queries.sql`.

Ejemplo:

```bash
psql -U postgres -d portfolio_ventas -f sql/01_schema.sql
psql -U postgres -d portfolio_ventas -f sql/02_seed.sql
psql -U postgres -d portfolio_ventas -f sql/03_queries.sql
```

## Preguntas de negocio

- ¿Cuál es la facturación y utilidad por mes?
- ¿Qué productos generan más ingresos y utilidad?
- ¿Qué clientes tienen mayor facturación?
- ¿Cómo se distribuyen las ventas por canal?
- ¿Qué ciudades concentran más ingresos?
- ¿Cómo cambia la facturación de un mes al siguiente?

## Alcance

Los datos incluidos son demostrativos y están diseñados para práctica técnica. No representan una empresa real ni resultados comerciales reales.

## Relación con mi perfil

Este proyecto fortalece mi perfil de **Database Administrator, Data Analyst y Software Developer** mediante SQL, modelado de datos, integridad y consultas analíticas reproducibles.

Autor: Juan Sebastian De la Cruz Amparo

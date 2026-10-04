# MongoDB Inventory API Design

Proyecto práctico de modelado y consultas para un sistema de inventario utilizando MongoDB.

## Objetivo

Representar productos y movimientos de inventario con un modelo documental y utilizar consultas y pipelines de agregación para responder preguntas operativas.

## Qué demuestra

- Modelado documental.
- Documentos y arrays.
- Índices.
- Consultas con filtros.
- Agregaciones con `$match`, `$group`, `$unwind`, `$sort` y `$project`.
- Diseño de información para inventario y operaciones.

## Estructura

```text
04_mongodb_inventario/
├── README.md
├── data/
│   └── products.json
├── queries/
│   └── inventory_queries.js
└── docs/
    └── MODEL.md
```

## Ejecución

Con MongoDB Shell (`mongosh`):

```bash
mongosh
use portfolio_inventory
```

Después importar los documentos:

```javascript
load("data/products.js")
```

Como los datos se proporcionan en JSON, también pueden importarse con:

```bash
mongoimport --db portfolio_inventory --collection products --file data/products.json --jsonArray
```

Luego ejecutar `queries/inventory_queries.js`.

## Preguntas operativas

- ¿Qué productos tienen stock bajo?
- ¿Cuál es el valor total del inventario?
- ¿Qué categorías concentran más unidades?
- ¿Qué productos tienen mayor valor almacenado?
- ¿Qué proveedores concentran más productos?
- ¿Cómo se distribuye el inventario por ciudad de almacén?

## Alcance

Los datos son demostrativos y están creados para práctica técnica. No representan información de una empresa real.

## Relación con mi perfil

Este proyecto fortalece mi perfil de **Database Administrator, Data Analyst y Software Developer** mediante MongoDB, modelado documental y agregaciones orientadas a decisiones operativas.

Autor: Juan Sebastian De la Cruz Amparo

# Modelo documental

## Colección

### products

Cada documento representa un producto de inventario y mantiene en el mismo documento información relacionada con stock, proveedor y ubicación.

Campos principales:

- `sku`: identificador único del producto.
- `name`: nombre comercial.
- `category`: categoría.
- `price`: precio de venta.
- `cost`: costo.
- `stock`: unidades disponibles.
- `min_stock`: umbral para alertas.
- `supplier`: proveedor.
- `warehouse`: subdocumento con ciudad y zona.
- `active`: estado del producto.

## Decisión de modelado

La información de ubicación se mantiene como subdocumento porque ciudad y zona forman parte del contexto operativo del producto.

Para un sistema con múltiples movimientos históricos, usuarios y auditoría, sería conveniente separar o complementar esta colección con documentos de movimientos y referencias según las necesidades de consulta y volumen.

## Consultas

El proyecto utiliza operaciones de lectura y agregación para convertir documentos operativos en indicadores de inventario.

## Alcance

Modelo demostrativo orientado a aprendizaje de MongoDB. No representa una arquitectura productiva completa.

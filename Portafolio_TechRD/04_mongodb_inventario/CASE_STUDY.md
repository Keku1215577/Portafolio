# Case Study — MongoDB Inventory

## Problema

Un sistema de inventario necesita representar información operativa de productos, stock, proveedores y ubicación de almacén y después convertir esos documentos en indicadores.

## Solución

Se modeló una colección `products` con información principal del producto y un subdocumento `warehouse` para la ubicación.

## Decisiones técnicas

### Modelo documental

MongoDB permite mantener juntos datos que suelen consultarse dentro del mismo contexto operativo, como ciudad y zona del almacén.

### Agregaciones

Se utilizaron pipelines para calcular:

- valor del inventario;
- unidades por categoría;
- productos por proveedor;
- distribución por ciudad y zona;
- margen unitario.

### Índices

Se añadieron índices sobre SKU, categoría, proveedor y ubicación para consultas frecuentes.

## Valor profesional

El ejercicio muestra que conozco el enfoque documental y que puedo adaptar una pregunta de negocio a operaciones de consulta y agregación de MongoDB.

## Limitaciones

La versión actual trabaja con una sola colección principal y datos demostrativos. Un sistema productivo necesitaría considerar movimientos, auditoría, usuarios, concurrencia, políticas de actualización y estrategia de modelado según los patrones reales de consulta.

## Siguiente evolución

- Añadir colección de movimientos.
- Registrar entradas y salidas.
- Crear agregaciones de rotación.
- Exponer consultas mediante una API.
- Integrar automatización con n8n.

# Case Study — PostgreSQL Sales Database

## Problema

Se necesita una estructura relacional que permita registrar productos, clientes y pedidos sin mezclar datos de catálogos con el detalle transaccional.

## Solución

Se diseñó un modelo con cinco tablas:

- categories
- products
- customers
- orders
- order_items

Las relaciones utilizan claves foráneas y el detalle del pedido conserva la cantidad, precio aplicado y descuento de cada línea.

## Decisiones técnicas

### Integridad

Se utilizaron claves primarias, claves foráneas y restricciones CHECK para impedir cantidades negativas, descuentos fuera de rango y costos superiores al precio de venta.

### Dinero

Las columnas monetarias utilizan NUMERIC para evitar errores de precisión propios de cálculos con punto flotante.

### Rendimiento

Se añadieron índices sobre fechas de pedido y claves utilizadas en relaciones frecuentes.

### Análisis

Las consultas incluyen agregaciones, CTE y LAG para construir indicadores y analizar variaciones mensuales.

## Valor profesional

Este ejercicio demuestra que puedo pasar de una necesidad operativa a:

```text
requerimiento
   -> modelo de datos
   -> reglas de integridad
   -> SQL
   -> indicadores
   -> interpretación
```

## Limitaciones

El dataset es pequeño y demostrativo. En un entorno productivo se evaluarían volumen, particionamiento, seguridad, roles, backups, migraciones, observabilidad y estrategia de índices con datos reales.

## Siguiente evolución

- Añadir procedimientos o funciones SQL cuando aporten valor.
- Incorporar pruebas de datos.
- Añadir historial de cambios.
- Integrar la base con una API.
- Alimentar un dashboard BI.

# PostgreSQL Sales Database — Interview Guide

## Presentación de 30 segundos

Diseñé una base de datos relacional de ventas en PostgreSQL, separando catálogos, clientes, pedidos y detalle de pedidos. Apliqué claves foráneas, restricciones, índices y consultas analíticas con CTE y funciones de ventana para obtener indicadores de ventas y utilidad.

## Preguntas técnicas

### ¿Por qué separar orders y order_items?

Porque un pedido puede contener múltiples productos. Separar cabecera y detalle evita duplicar información del pedido y permite representar correctamente una relación uno a muchos.

### ¿Por qué usar NUMERIC para dinero?

Porque es un tipo pensado para valores exactos, adecuado para importes monetarios y más seguro que depender de cálculos con punto flotante.

### ¿Qué protege una foreign key?

La integridad referencial. Evita que un registro hijo apunte a una entidad inexistente, según las reglas definidas para la relación.

### ¿Para qué sirven los índices?

Reducen el costo de ciertas búsquedas y joins frecuentes, aunque agregan espacio y pueden aumentar el costo de escritura.

### ¿Qué aporta LAG?

Permite acceder al valor de una fila anterior dentro de una ventana ordenada. En este proyecto se usa para comparar ingresos de un mes con el anterior.

### ¿Qué mejorarías en producción?

Revisaría índices con EXPLAIN/EXPLAIN ANALYZE, roles y permisos, backups, migraciones, monitoreo, volumen de datos y requisitos de concurrencia.

## Pregunta de Data Analyst

¿Cómo utilizarías esta base para un dashboard?

Crearía consultas o vistas orientadas a KPIs como ingresos, utilidad, margen, unidades, evolución mensual, productos líderes y distribución geográfica o por canal.

# Guion de entrevista: gestor de inventario y ventas

## Presentación de 30 segundos

"Desarrollé una aplicación de inventario y ventas con Python y SQLite. Separé la interfaz de las reglas de negocio para que la lógica pudiera probarse de forma independiente. El sistema valida productos, controla el stock y registra una venta junto con el descuento del inventario dentro de una misma transacción. También conserva los datos históricos de la venta aunque el producto cambie posteriormente."

## Problema que resolví

El sistema está pensado para una operación pequeña que necesita controlar productos, existencias, ventas e historial sin depender de un servidor de base de datos externo.

## Arquitectura

**Presentación:** Tkinter/ttk en `app.py`.

**Lógica de negocio:** `servicio.py`.

**Persistencia:** SQLite.

**Pruebas:** `tests/test_servicio.py`.

La separación permite modificar la interfaz sin duplicar las reglas del negocio.

## Preguntas técnicas frecuentes

### ¿Cómo evitas vender más unidades de las disponibles?

La operación valida la existencia disponible dentro de la lógica de servicio y actualiza venta y stock dentro de una misma transacción.

### ¿Por qué usas una transacción?

Porque registrar la venta sin descontar el stock, o descontar stock sin registrar la venta, dejaría los datos inconsistentes. La transacción permite que ambas operaciones se confirmen o se reviertan juntas.

### ¿Por qué utilizaste BEGIN IMMEDIATE?

Para tomar una reserva de escritura antes de consultar y actualizar existencias, reduciendo el riesgo de que dos operaciones concurrentes consuman el mismo stock.

### ¿Qué ocurre si cambia el precio del producto?

Las ventas anteriores conservan una copia del precio y costo utilizados en el momento de la operación. De esta forma, el historial no cambia cuando se edita el catálogo actual.

### ¿Por qué no borras los productos vendidos?

Porque eliminar el registro puede romper el historial. El sistema utiliza archivado para retirar un producto del catálogo activo sin perder sus ventas.

### ¿Por qué no concatenas valores en SQL?

Las consultas parametrizadas separan el código SQL de los valores introducidos por el usuario y son una práctica básica para evitar problemas de inyección y errores de escapado.

### ¿Cómo probarías una venta incorrecta?

Crearía un caso donde la cantidad solicitada sea superior al stock y comprobaría dos cosas: la venta no aparece y el stock permanece sin cambios.

### ¿Qué mejorarías en producción?

Añadiría autenticación y autorización, una API REST, auditoría de movimientos, devoluciones, compras a proveedores, filtros de historial y un dashboard conectado a los datos.

## Relación con tus tres perfiles

**Data Analyst:** el historial exportado puede alimentar análisis de ventas, inventario y productos.

**Database Administrator:** el proyecto demuestra claves, persistencia relacional, índices, consultas e integridad transaccional.

**Software Developer:** demuestra separación de responsabilidades, validaciones, CRUD, transacciones y pruebas.

## Regla para la entrevista

No digas solamente "usé SQLite".

Explica el problema que resolviste con SQLite, por qué necesitabas una transacción y cómo protegiste el historial.

# Caso de estudio: gestor de inventario y ventas

## Resumen

Aplicación de escritorio desarrollada para gestionar productos, existencias y ventas con persistencia en SQLite. El proyecto se diseñó separando la interfaz de usuario de las reglas de negocio y del acceso a datos.

## Problema

Una pequeña operación necesita controlar:

- catálogo de productos;
- stock disponible;
- ventas;
- productos archivados;
- historial;
- exportación para análisis posterior.

El sistema debe evitar ventas superiores al stock y conservar la información histórica cuando cambian los datos actuales del catálogo.

## Arquitectura

### Capa de presentación

`app.py` utiliza Tkinter/ttk para formularios, tablas, mensajes y eventos de usuario.

### Capa de servicio

`servicio.py` concentra validaciones, reglas de negocio, consultas y transacciones. Esto evita que la interfaz tenga que controlar directamente la lógica de persistencia.

### Persistencia

SQLite almacena productos y ventas. La relación entre ambas entidades se establece mediante `producto_id`.

## Decisiones técnicas

### Consistencia de ventas

Registrar una venta y descontar el stock se ejecutan dentro de la misma transacción.

Si una operación falla, las dos acciones se revierten.

### Control de concurrencia

`BEGIN IMMEDIATE` reserva la escritura antes de consultar existencias, reduciendo el riesgo de que dos operaciones simultáneas utilicen el mismo stock disponible.

### Historial

Cada venta conserva una copia del nombre, categoría, precio y costo utilizados en el momento de la venta.

Esto permite que una modificación posterior del producto no altere el historial.

### Seguridad de consultas

Las consultas que reciben valores del usuario utilizan parámetros en lugar de concatenar directamente el texto.

### Manejo monetario

Los importes se almacenan como centavos enteros y se validan mediante `Decimal`.

## Reglas de negocio

- SKU único incluso cuando un producto está archivado.
- No se permite stock negativo.
- Las cantidades de venta deben ser enteras y positivas.
- No se puede vender una cantidad superior al stock.
- Una venta no puede dejar el sistema en un estado parcialmente actualizado.
- Archivar un producto no elimina su historial.
- Los avisos se generan cuando el stock es menor o igual al mínimo configurado.

## Pruebas

El proyecto incluye siete pruebas del servicio con bases temporales aisladas.

Las pruebas cubren operaciones y reglas críticas del sistema, especialmente las relacionadas con validación y consistencia.

## Valor profesional

Este proyecto demuestra competencias relacionadas con:

**Software Development**

Separación de responsabilidades, CRUD, validaciones, transacciones y pruebas.

**Database**

Persistencia relacional, claves, consultas parametrizadas e integridad de datos.

**Data**

Exportación del historial para que la información pueda utilizarse posteriormente en análisis.

## Limitaciones

Es una aplicación educativa local orientada a un operador.

No incluye:

- autenticación;
- autorización por roles;
- compras a proveedores;
- devoluciones;
- impuestos;
- auditoría completa de movimientos;
- múltiples usuarios;
- API remota.

## Próxima evolución

La siguiente versión podría convertir la capa de servicio en una API REST con autenticación, añadir una tabla de movimientos de inventario y conectar el historial con un dashboard de indicadores.

## Ejecución

Desde la carpeta del proyecto:

`python app.py`

Requiere una sesión de escritorio con Tkinter disponible.

# Proyecto 2: gestor de inventario y ventas

Aplicación de escritorio que permite crear, consultar, editar y archivar productos, registrar ventas, controlar existencias y exportar el historial para análisis.

## Arquitectura

- `app.py`: presentación y eventos de Tkinter/ttk. Formularios, tabla, confirmaciones y mensajes.
- `servicio.py`: reglas de negocio, validación, consultas y transacciones. No depende de la interfaz.
- `datos/inventario.sqlite3`: persistencia local, creada en el primer inicio.
- `tests/test_servicio.py`: siete pruebas del servicio con bases temporales aisladas.

## Modelo relacional

`productos` contiene SKU único, nombre, categoría, precio y costo en centavos, stock, mínimo y estado activo. `ventas.producto_id` referencia `productos.id`; un producto puede tener muchas ventas. La venta guarda además una copia del nombre, categoría, precio y costo para que una edición posterior no modifique los resultados históricos.

## Reglas importantes

- SKU único sin distinción de mayúsculas ASCII, incluso en productos archivados.
- No se permite stock negativo ni cantidades de venta de cero, negativas o fraccionarias.
- Registrar venta y descontar stock ocurren en la misma transacción. Un fallo revierte ambas operaciones.
- `BEGIN IMMEDIATE` reserva la escritura antes de consultar existencias y evita que dos ventas simultáneas gasten el mismo stock.
- Consultas parametrizadas para valores introducidos por el usuario.
- Importes guardados como enteros en centavos; se valida con Decimal.
- Archivar conserva ventas y producto. La interfaz no incluye restauración de archivados.
- Precio y costo cero están permitidos; vender bajo costo también. El usuario debe revisar si esos valores son intencionales.
- Los avisos usan stock menor o igual al mínimo. No se realizan compras automáticas.

## Ejecutar

`python app.py` desde esta subcarpeta. Requiere una sesión de escritorio con Tkinter disponible. No hay que instalar un servidor de base de datos ni dependencias con pip.

## Casos de prueba manual

| Acción | Resultado esperado |
|---|---|
| Crear producto con SKU nuevo | Aparece en el catálogo y persiste tras reiniciar |
| Crear SKU duplicado | Mensaje de error; no se inserta |
| Editar precio | Nuevas ventas usan el precio nuevo; ventas previas no cambian |
| Vender con existencias | Disminuye stock y aumenta el historial |
| Vender más que el stock | Se rechaza sin alterar registros |
| Archivar producto vendido | Sale del catálogo activo; sus ventas siguen visibles |
| Exportar CSV | El archivo puede procesarse con el proyecto 1 |

## Alcance y extensiones

Aplicación educativa local para un operador. El historial muestra todas las ventas, sin filtros de fechas. No gestiona carritos, compras a proveedores, devoluciones, impuestos, usuarios ni permisos. La edición de stock no registra movimientos auditables. Para una siguiente versión: añadir tabla de movimientos, registrar entradas y devoluciones, permitir restaurar archivados y reemplazar la interfaz por una API con autenticación.

# MongoDB Inventory — Interview Guide

## Presentación de 30 segundos

Modelé un inventario en MongoDB usando documentos de productos, subdocumentos para ubicaciones y pipelines de agregación para calcular indicadores operativos. El proyecto demuestra modelado documental, consultas, índices y análisis de inventario.

## Preguntas técnicas

### ¿Cuándo elegirías MongoDB sobre PostgreSQL?

Cuando el problema se beneficia de un modelo documental flexible y los patrones de consulta encajan mejor con documentos agregados. La decisión debe basarse en estructura, consistencia, relaciones, volumen y patrones reales de acceso.

### ¿Por qué warehouse es un subdocumento?

Porque ciudad y zona forman parte del contexto de ubicación del producto y se consultan como una unidad.

### ¿Qué hace $group?

Agrupa documentos por una clave y permite calcular acumulados como sumas, conteos o promedios.

### ¿Qué hace $unwind?

Descompone un array para procesar cada elemento como un documento separado dentro del pipeline.

### ¿Qué función cumplen los índices?

Permiten acelerar determinadas consultas, a cambio de espacio y costo adicional en escrituras.

### ¿Qué añadirías para un inventario real?

Una colección de movimientos, control de concurrencia, auditoría, validación de esquemas, autenticación, monitoreo y una estrategia de modelado definida por los patrones de consulta.

## Comparación con PostgreSQL

PostgreSQL del portafolio demuestra relaciones, restricciones e integridad referencial.

MongoDB demuestra documentos, subdocumentos y agregaciones.

La combinación evidencia que conozco ambos enfoques y puedo seleccionar una estrategia según el problema.

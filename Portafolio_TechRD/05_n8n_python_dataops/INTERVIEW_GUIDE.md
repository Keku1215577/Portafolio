# DataOps Automation — Interview Guide

## Presentación de 30 segundos

Construí una automatización donde n8n recibe datos por un Webhook y coordina una API Python con FastAPI y Pandas. Python valida, normaliza y transforma los registros, calcula ingresos y utilidad y conserva las filas rechazadas con su motivo. El objetivo es mostrar una automatización reproducible y preparada para crecer hacia persistencia y BI.

## Preguntas técnicas

### ¿Qué aporta n8n?

La orquestación del flujo. Permite conectar la entrada con el servicio Python y controlar el movimiento del resultado sin colocar toda la lógica de negocio dentro del workflow.

### ¿Por qué Python en vez de hacer toda la transformación dentro de n8n?

Porque las reglas de datos quedan centralizadas en código versionado, reutilizable y testeable. Además, Pandas facilita operaciones de transformación y análisis.

### ¿Qué ocurre con un registro inválido?

No se elimina silenciosamente. Se marca como rechazado y se conserva junto con un motivo para facilitar auditoría y corrección.

### ¿Por qué FastAPI?

Proporciona una interfaz HTTP sencilla para exponer el procesamiento como un servicio reutilizable.

### ¿Por qué Docker?

Permite levantar n8n y la API Python en un entorno reproducible y mantener la comunicación entre servicios mediante una red de Compose.

### ¿Cómo lo llevarías a producción?

Añadiría autenticación, gestión segura de secretos, persistencia, logs estructurados, métricas, retries, monitoreo, control de acceso y una estrategia clara de despliegue.

### ¿Cómo lo conectarías con tu proyecto PostgreSQL?

Después del procesamiento, n8n podría enviar los registros validados a un servicio que realice la carga a PostgreSQL y posteriormente activar un proceso de actualización de indicadores para BI.

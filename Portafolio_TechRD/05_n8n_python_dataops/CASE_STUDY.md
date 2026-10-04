# Case Study — DataOps Automation

## Problema

Los datos de ventas pueden llegar desde diferentes sistemas y necesitan validarse y transformarse antes de ser utilizados por analistas o cargados en otros sistemas.

## Solución

Se construyó un flujo donde n8n recibe la solicitud y orquesta el procesamiento, mientras una API Python aplica las reglas de calidad y genera el resultado.

## Arquitectura

```text
Webhook n8n
    |
    v
HTTP Request
    |
    v
FastAPI
    |
    v
Pandas
    |
    +--> validación
    +--> normalización
    +--> métricas
    +--> rechazados
    |
    v
Respuesta a n8n
```

## Decisión principal

La lógica de datos no se colocó directamente en el workflow. Python mantiene las reglas de transformación en código reutilizable y testeable.

Esto permite que otra aplicación o automatización pueda consumir el mismo servicio.

## Calidad de datos

El proceso distingue entre:

- registros aceptados;
- registros rechazados;
- motivo de rechazo.

Esto evita que un error de calidad desaparezca silenciosamente.

## Valor profesional

El proyecto demuestra:

- automatización;
- APIs;
- Python;
- Pandas;
- validación;
- Docker;
- testing;
- integración de herramientas.

## Evolución

La siguiente versión puede integrar PostgreSQL como destino, programar ingestas, agregar alertas y producir un dataset listo para Power BI.

## Limitaciones

Es una demostración local. En producción se necesitarían autenticación del webhook, secretos gestionados fuera del repositorio, observabilidad, retries y políticas de acceso.

# DataOps Automation with n8n and Python

Proyecto de automatización de datos que combina n8n como orquestador y Python como servicio de procesamiento.

## Objetivo

Automatizar un flujo reproducible para recibir datos de ventas, validarlos, transformarlos y devolver un resultado listo para análisis.

La arquitectura separa la **orquestación del proceso** de la **lógica de datos**:

```text
Cliente
  |
  v
n8n Webhook
  |
  v
HTTP Request
  |
  v
Python / FastAPI
  |
  +--> Validación
  +--> Normalización
  +--> Cálculo de métricas
  +--> Filas rechazadas
  |
  v
n8n
  |
  v
Respuesta del proceso
```

## Qué demuestra

- Automatización de workflows con n8n.
- Integración entre n8n y una API Python.
- Diseño de procesos ETL/ELT.
- Validación y control de calidad de datos.
- Transformación de datos con Pandas.
- Desarrollo de APIs con FastAPI.
- Manejo explícito de filas rechazadas.
- Pruebas automatizadas.
- Separación entre orquestación y lógica de negocio.
- Preparación de una solución para futuras integraciones con bases de datos, dashboards y notificaciones.

## Stack

- n8n
- Python
- FastAPI
- Pandas
- Pydantic
- Docker
- GitHub Actions

## Flujo

1. Un cliente envía un conjunto de registros al Webhook de n8n.
2. n8n envía los registros al servicio Python.
3. Python valida campos obligatorios y reglas de negocio.
4. Python normaliza fechas, cantidades, precios y descuentos.
5. Las filas válidas se transforman y se calculan ingresos y utilidad bruta.
6. Las filas inválidas se conservan en una sección de rechazo con el motivo.
7. n8n recibe el resultado y devuelve el resumen del procesamiento.

## Estructura

```text
05_n8n_python_dataops/
├── README.md
├── .env.example
├── docker-compose.yml
├── api/
│   ├── app.py
│   ├── processor.py
│   ├── requirements.txt
│   └── tests/
│       └── test_processor.py
├── data/
│   └── ventas_demo.json
├── docs/
│   └── ARCHITECTURE.md
└── n8n/
    ├── README.md
    └── workflows/
        └── 01_sales_data_quality.json
```

## Ejecución local

Requisitos:

- Docker Desktop
- Docker Compose

Iniciar servicios:

```bash
docker compose up --build
```

Servicios principales:

- n8n: `http://localhost:5678`
- Python API: `http://localhost:8000/docs`

En n8n se debe importar el workflow incluido en:

```text
n8n/workflows/01_sales_data_quality.json
```

El workflow utiliza la URL interna `http://python-api:8000/process`, por lo que la comunicación ocurre dentro de la red Docker del proyecto.

## API Python

### GET /health

Verifica disponibilidad del servicio.

### POST /process

Recibe:

```json
{
  "records": [
    {
      "date": "2026-08-14",
      "product": "Laptop 14",
      "quantity": 2,
      "unit_price": 95000,
      "cost": 73500,
      "discount_pct": 10
    }
  ]
}
```

Devuelve un resumen con:

- registros recibidos;
- registros aceptados;
- registros rechazados;
- ingresos;
- utilidad bruta;
- margen bruto;
- detalle de filas rechazadas.

## Calidad de datos

El procesador valida:

- fecha válida;
- producto no vacío;
- cantidad entera positiva;
- precio no negativo;
- costo no negativo;
- costo no superior al precio;
- descuento entre 0 y 100.

Las filas inválidas no desaparecen silenciosamente: se conservan con un motivo de rechazo.

## Ejemplo de resultado

```json
{
  "status": "completed_with_rejections",
  "received": 5,
  "accepted": 4,
  "rejected": 1,
  "revenue": 210000.0,
  "gross_profit": 52800.0,
  "gross_margin_pct": 25.14
}
```

## Alcance

Proyecto académico/personal de práctica. Los datos son demostrativos y no representan una empresa real.

Para una implementación productiva se añadirían autenticación del webhook, gestión de credenciales, persistencia, observabilidad, alertas y controles de acceso. n8n dispone de mecanismos de seguridad y auditoría para revisar aspectos de la instancia y sus workflows. 

## Relación con mi perfil

Este proyecto une directamente mis tres líneas profesionales:

- **Data Analyst:** calidad, transformación, métricas y preparación de datos.
- **Software Developer:** API Python, estructura modular, validaciones y pruebas.
- **Database/Data Engineering:** preparación del pipeline para persistencia y automatización de procesos de datos.

Autor: Juan Sebastian De la Cruz Amparo

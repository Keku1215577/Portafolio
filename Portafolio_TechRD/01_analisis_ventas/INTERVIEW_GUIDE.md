# Guion de entrevista: análisis de ventas E-commerce

## Presentación de 30 segundos

"Desarrollé un proyecto de análisis de ventas con un flujo reproducible desde el CSV hasta los indicadores y el dashboard. Primero validé y limpié los registros, después cargué los datos válidos en SQLite y utilicé SQL para obtener métricas de ingresos, utilidad, margen, ticket promedio y variación mensual. También conservé las filas rechazadas para poder revisar la calidad del dato."

## Qué problema resolví

El proyecto busca responder preguntas comerciales sobre rentabilidad por producto, evolución mensual y distribución de ventas por canal y ciudad.

## Qué hice técnicamente

### Python

Utilicé Python para:

- leer el archivo;
- validar registros;
- normalizar campos;
- separar registros rechazados;
- transformar los importes;
- generar resultados.

### SQL y SQLite

Utilicé SQLite como almacenamiento analítico local y SQL para:

- agregaciones;
- rankings de productos;
- cálculo de métricas;
- variación mensual;
- comparación de canales;
- función de ventana LAG.

### Calidad de datos

Recibí 737 filas. El proceso aceptó 720 y rechazó 17.

No rellené valores faltantes inventando información. Las filas problemáticas se conservaron en cuarentena con su motivo.

## Métricas que debo conocer

**Ingresos:** RD$19,991,697.50

**Utilidad bruta:** RD$5,130,747.50

**Margen bruto:** 25.66%

**Ticket promedio:** RD$27,766.25

**Producto con mayor utilidad bruta:** Laptop 14, con RD$3,222,450.00

## Preguntas frecuentes

### ¿Por qué no eliminaste simplemente las filas inválidas?

Porque eliminar silenciosamente los registros dificulta auditar el origen del problema. Prefiero separar los registros no utilizables y conservar la evidencia para revisión.

### ¿Por qué guardaste el dinero en centavos?

Para evitar errores de precisión asociados a operaciones con valores monetarios de punto flotante.

### ¿Por qué el margen no es el promedio de los márgenes de cada venta?

Porque el indicador debe representar el resultado global. Por eso calculé la utilidad total dividida entre los ingresos totales.

### ¿Por qué SQLite?

El proyecto es una demostración local y SQLite permite tener una base relacional completa sin instalar un servidor independiente.

### ¿Qué harías en una empresa real?

Primero validaría la fuente y el modelo de datos con las áreas responsables. Luego añadiría controles de calidad automatizados, un modelo analítico más formal, dimensiones de producto/cliente/fecha, seguimiento de devoluciones y un dashboard conectado a una fuente actualizable.

### ¿Qué limitación importante tiene el proyecto?

Los datos son sintéticos y cubren ocho meses. Por eso los resultados sirven para demostrar el proceso técnico, pero no para describir el comportamiento de una empresa real.

## Cómo relacionarlo con el puesto

**Data Analyst:** limpieza, transformación, SQL, KPIs, análisis y comunicación.

**Database Administrator:** SQLite, claves, índices, integridad y consultas.

**Software Developer:** Python, modularización, validaciones, automatización y pruebas.

## Regla para la entrevista

No memorizar números sin entenderlos.

Debo poder explicar:

**qué problema había → qué datos tenía → qué limpié → cómo calculé las métricas → qué encontré → qué decisión podría apoyarse en esos datos → qué limitaciones existen.**

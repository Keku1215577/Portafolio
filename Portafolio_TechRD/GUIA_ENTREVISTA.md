# Guía para explicar los proyectos en una entrevista

## Antes de presentarlos

Ejecuta los proyectos, entiende las funciones principales y añade al menos una mejora que puedas explicar. Evita memorizar una presentación sin comprender el código. Describe los datos como ficticios y el trabajo como práctica personal con asistencia de IA.

## Proyecto de analista: recorrido de 3 minutos

1. **Problema:** una tienda necesita conocer ventas, rentabilidad y diferencias entre canales.
2. **Datos:** 737 filas de demostración; identifiqué duplicados, fechas inválidas, campos vacíos y valores fuera de rango.
3. **Método:** separé 17 filas problemáticas, conservé evidencia de los rechazos y cargué 720 ventas válidas en SQLite.
4. **Análisis:** calculé ingresos, utilidad bruta, margen ponderado y ticket; añadí consultas por producto, mes y canal.
5. **Resultado:** muestro el dashboard y sus filtros; explico un hallazgo de `salidas/hallazgos.md` y una decisión que requeriría validar con el negocio.
6. **Límite:** son datos sintéticos; no puedo inferir rentabilidad neta ni causalidad.

### Preguntas que debes poder responder

**¿Por qué no eliminaste filas sin dejar evidencia?**
Porque necesito que las decisiones de limpieza se puedan revisar; el archivo de rechazos conserva el motivo y la fila original.

**¿Por qué margen ponderado?**
Porque el margen global se calcula sobre el total de ingresos; promediar porcentajes por venta daría el mismo peso a operaciones de importes distintos.

**¿Qué ocurre si un mismo ID tiene dos valores diferentes?**
Conservo la primera fila válida y marco la posterior como conflicto. En un negocio real consultaría la fuente antes de decidir cuál es correcta.

**¿Por qué no usaste pandas?**
La primera versión hace explícitos los pasos de validación y SQL sin dependencias externas. Una ampliación útil es implementar el mismo proceso con pandas y comprobar que produce los mismos resultados.

## Proyecto de programador: recorrido de 3 minutos

1. **Problema:** controlar productos y evitar ventas que dejen el inventario negativo.
2. **Diseño:** separé presentación, reglas de negocio y persistencia.
3. **Demostración:** creo un producto, registro una venta, intento una sobreventa y reviso el historial.
4. **Consistencia:** una transacción actualiza existencias y registra la venta; si algo falla se revierte la operación.
5. **Pruebas:** muestro validaciones, reversión ante errores y dos intentos de compra concurrentes.
6. **Integración:** exporto el CSV y genero el análisis comercial de esas ventas.

### Preguntas que debes poder responder

**¿Por qué SQLite?**
El alcance es una aplicación local y un archivo facilita ejecutar y respaldar el proyecto. Una solución multiusuario en red requeriría reevaluar la base de datos y la arquitectura.

**¿Por qué guardas precios históricos en ventas?**
Para que cambiar el catálogo no altere el importe de operaciones ya realizadas.

**¿Cómo evitas una sobreventa?**
La transacción adquiere el bloqueo de escritura antes de consultar el stock, valida la cantidad y realiza los dos cambios de manera atómica.

**¿Qué mejorarías primero?**
Añadiría movimientos auditables de inventario. Después incorporaría devoluciones y pedidos con varias líneas, adaptando las métricas del análisis.

## Ejercicio para hacerlos tuyos

1. Añade un filtro de fecha al historial del inventario.
2. Añade un indicador de unidades por venta al reporte.
3. Escribe una prueba del filtro o cálculo nuevo.
4. Documenta tu decisión, una dificultad encontrada y cómo la resolviste.
5. Guarda capturas de tu versión para el portafolio.

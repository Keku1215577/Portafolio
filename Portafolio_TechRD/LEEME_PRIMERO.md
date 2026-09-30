# Portafolio TechRD — Análisis de datos y desarrollo de software

Dos proyectos complementarios preparados para Juan Sebastian De la Cruz Amparo. Nivel inicial–intermedio. El negocio y los datos son ficticios. El objetivo es practicar, comprender el código y demostrar habilidades con una solución que se puede ejecutar localmente.

| Proyecto | Qué demuestra | Tecnologías |
|---|---|---|
| 01_analisis_ventas | Limpieza, controles de calidad, consultas SQL, indicadores, visualización e interpretación | Python, CSV, SQLite, SQL, HTML/CSS/JavaScript |
| 02_gestor_inventario | Interfaz de escritorio, persistencia, validaciones, transacciones y pruebas | Python, Tkinter/ttk, SQLite, unittest |

## 1. Ver el resultado inmediatamente

Descomprime todo el ZIP. Abre `01_analisis_ventas/salidas/dashboard.html` con Chrome, Edge o Firefox. No requiere instalar Python para ver este reporte ya generado. Prueba los filtros; los cuatro indicadores, gráficos y tabla se actualizan con la misma selección.

El código editable es `plantilla.html`; `salidas/dashboard.html` se vuelve a generar al ejecutar el análisis.

## 2. Preparar Python en Windows

1. Instala Python 3.10 o superior desde https://www.python.org/downloads/ si no lo tienes. Incluye Tcl/Tk y, si el instalador ofrece la opción, agrega Python a PATH.
2. Abre una terminal y escribe `py -3 --version`. Si tu instalación no tiene el comando `py`, usa `python --version`.
3. Para comprobar la interfaz gráfica, ejecuta `py -3 -m tkinter`. Debe aparecer una ventana de prueba. Si falta Tkinter, modifica o reinstala Python con Tcl/Tk.
4. No necesitas ejecutar `pip install`: los dos proyectos usan la biblioteca estándar de Python.
5. Abre esta carpeta completa en tu editor de código. También puedes utilizar los archivos `.bat` incluidos.

Documentación oficial: https://docs.python.org/3/library/tkinter.html y https://docs.python.org/3/library/sqlite3.html.

## 3. Ejecutar el proyecto de analista

Desde esta carpeta principal:

```powershell
py -3 01_analisis_ventas/analizar.py
```

También puedes abrir `EJECUTAR_ANALISIS.bat` con doble clic. Después abre `01_analisis_ventas/salidas/dashboard.html`.

El CSV de ejemplo ya está incluido. Para regenerar exactamente el mismo dataset:

```powershell
py -3 01_analisis_ventas/generar_datos.py
```

El análisis produce CSV limpios, CSV de filas rechazadas, SQLite, resumen JSON, hallazgos y el dashboard. Cada ejecución reemplaza los resultados de la carpeta de salida elegida, sin cambiar el CSV de entrada.

## 4. Ejecutar el proyecto de programador

```powershell
py -3 02_gestor_inventario/app.py
```

También puedes abrir `ABRIR_INVENTARIO.bat`. La primera ejecución crea `02_gestor_inventario/datos/inventario.sqlite3` con cuatro productos de ejemplo. Las siguientes ejecuciones conservan tus cambios.

Prueba este recorrido:

1. Selecciona Mouse USB: el stock inicial es 4 y el mínimo 5; aparece una alerta de reposición.
2. Vende 2 unidades. El stock baja a 2 y la venta aparece en Historial.
3. Intenta vender 3 unidades: la aplicación lo rechaza y conserva el stock.
4. Pulsa Nuevo / limpiar; crea otro producto con un SKU diferente.
5. Selecciona un producto y cambia precio o stock; pulsa Guardar producto.
6. Exporta las ventas desde Historial y exportación.
7. Cierra y abre la aplicación para comprobar que persisten los registros.

Usa punto decimal sin separadores de miles en los formularios: `1500.50`. Cada venta contiene un solo producto. Archivar retira el producto del catálogo activo y conserva su historial. El inventario a costo solo incluye productos activos.

## 5. Conectar ambos proyectos

Exporta el CSV de ventas del inventario y guárdalo, por ejemplo, como `ventas_inventario.csv` en esta carpeta principal. Luego:

```powershell
py -3 01_analisis_ventas/analizar.py --entrada ventas_inventario.csv --salida 01_analisis_ventas/salidas_inventario
```

Abre `01_analisis_ventas/salidas_inventario/dashboard.html`. Así conservas separado el reporte de demostración.

## 6. Ejecutar las pruebas

Desde esta carpeta principal:

```powershell
py -3 -m unittest discover -s 01_analisis_ventas -p "test_*.py" -v
py -3 -m unittest discover -s 02_gestor_inventario/tests -v
```

Se incluyen 12 pruebas automáticas: cálculos y redondeo, fechas y valores inválidos, duplicados, archivo vacío, resultados reproducibles, ventas, stock insuficiente, reversión ante errores, concurrencia, SKU único, exportación y persistencia.

Validación durante la preparación: 12 pruebas aprobadas en Python 3.12; integración inventario → CSV → análisis aprobada; lógica JavaScript del dashboard comprobada con DOM simulado (totales, filtros, selección vacía y restablecimiento). No se verificó el renderizado visual en un navegador en este entorno. La interfaz Tkinter no se abrió en este entorno porque no hay pantalla gráfica disponible; comprueba el recorrido manual anterior en Windows. La lógica del inventario se probó independientemente de la interfaz.

## 7. Cómo estudiarlos y presentarlos

1. Lee el README de cada proyecto.
2. Ejecuta el ejemplo y revisa los resultados antes de editar.
3. Estudia `analizar.py` y `servicio.py`: contienen las decisiones principales.
4. Cambia datos y añade una mejora propia; ejecuta nuevamente las pruebas.
5. Consulta `GUIA_ENTREVISTA.md` para preparar la explicación.
6. Publica cada subcarpeta como repositorio independiente o el paquete como un repositorio con dos proyectos. Incluye descripción y capturas. No publiques datos personales ni bases de datos reales.

El código fue preparado con asistencia de IA. Preséntalo como proyecto personal de aprendizaje después de comprenderlo y personalizarlo, sin atribuirle experiencia empresarial ni resultados de una empresa real.

## Alcance

Son proyectos locales de portafolio. No incluyen autenticación, sincronización entre equipos, facturación fiscal, impuestos, devoluciones ni auditoría completa de ajustes de stock. Las ventas conservan precio, costo, nombre y categoría históricos. La edición manual de stock es una corrección administrativa, no un registro de compras. El dashboard calcula utilidad bruta, no beneficio neto.

No se despliega nada en internet. Para proteger tus datos de práctica, cierra la aplicación y copia el archivo SQLite a otra carpeta como respaldo.

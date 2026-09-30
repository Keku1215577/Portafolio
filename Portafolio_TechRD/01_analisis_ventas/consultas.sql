-- Ejecutar contra salidas/analisis.sqlite3, por ejemplo en DB Browser for SQLite.
-- Ingresos, utilidad bruta y margen ponderado.
SELECT COUNT(*) AS ventas, SUM(ingreso_centavos)/100.0 AS ingresos_rd,
       SUM(utilidad_centavos)/100.0 AS utilidad_rd,
       ROUND(100.0*SUM(utilidad_centavos)/NULLIF(SUM(ingreso_centavos),0),2) AS margen_pct
FROM ventas;

-- Ranking de productos por utilidad; cantidad no equivale a número de ventas.
SELECT producto, SUM(cantidad) AS unidades,
       SUM(ingreso_centavos)/100.0 AS ingresos_rd,
       SUM(utilidad_centavos)/100.0 AS utilidad_rd
FROM ventas GROUP BY producto ORDER BY utilidad_rd DESC;

-- Variación mensual; si faltan meses, LAG compara con el mes observado anterior.
WITH mensual AS (
  SELECT substr(fecha,1,7) AS mes, SUM(ingreso_centavos)/100.0 AS ingresos
  FROM ventas GROUP BY mes
), comparacion AS (
  SELECT *, LAG(ingresos) OVER (ORDER BY mes) AS anterior FROM mensual
)
SELECT mes, ingresos, ROUND((ingresos-anterior)*100.0/NULLIF(anterior,0),2) AS variacion_pct
FROM comparacion ORDER BY mes;

-- Comparación de canales: participación y ticket promedio.
SELECT canal, COUNT(*) AS ventas,
       ROUND(AVG(ingreso_centavos)/100.0,2) AS ticket_rd,
       ROUND(100.0*SUM(ingreso_centavos)/NULLIF((SELECT SUM(ingreso_centavos) FROM ventas),0),2) AS participacion_pct
FROM ventas GROUP BY canal;

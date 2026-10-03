-- Ejecutar contra salidas/analisis.sqlite3, por ejemplo en DB Browser for SQLite.

-- 1. Ingresos, utilidad bruta y margen ponderado.
SELECT COUNT(*) AS ventas,
       SUM(ingreso_centavos)/100.0 AS ingresos_rd,
       SUM(utilidad_centavos)/100.0 AS utilidad_rd,
       ROUND(100.0*SUM(utilidad_centavos)/NULLIF(SUM(ingreso_centavos),0),2) AS margen_pct
FROM ventas;

-- 2. Ranking de productos por utilidad.
SELECT producto,
       COUNT(*) AS ventas,
       SUM(cantidad) AS unidades,
       SUM(ingreso_centavos)/100.0 AS ingresos_rd,
       SUM(utilidad_centavos)/100.0 AS utilidad_rd,
       ROUND(100.0*SUM(utilidad_centavos)/NULLIF(SUM(ingreso_centavos),0),2) AS margen_pct
FROM ventas
GROUP BY producto
ORDER BY utilidad_rd DESC;

-- 3. Variación mensual de ingresos.
WITH mensual AS (
  SELECT substr(fecha,1,7) AS mes,
         SUM(ingreso_centavos)/100.0 AS ingresos
  FROM ventas
  GROUP BY mes
), comparacion AS (
  SELECT *,
         LAG(ingresos) OVER (ORDER BY mes) AS anterior
  FROM mensual
)
SELECT mes,
       ingresos,
       ROUND((ingresos-anterior)*100.0/NULLIF(anterior,0),2) AS variacion_pct
FROM comparacion
ORDER BY mes;

-- 4. Comparación de canales.
SELECT canal,
       COUNT(*) AS ventas,
       SUM(cantidad) AS unidades,
       ROUND(SUM(ingreso_centavos)/100.0,2) AS ingresos_rd,
       ROUND(SUM(utilidad_centavos)/100.0,2) AS utilidad_rd,
       ROUND(100.0*SUM(utilidad_centavos)/NULLIF(SUM(ingreso_centavos),0),2) AS margen_pct,
       ROUND(100.0*SUM(ingreso_centavos)/NULLIF((SELECT SUM(ingreso_centavos) FROM ventas),0),2) AS participacion_ingresos_pct
FROM ventas
GROUP BY canal
ORDER BY ingresos_rd DESC;

-- 5. Comparación de ciudades.
SELECT ciudad,
       COUNT(*) AS ventas,
       SUM(cantidad) AS unidades,
       ROUND(SUM(ingreso_centavos)/100.0,2) AS ingresos_rd,
       ROUND(SUM(utilidad_centavos)/100.0,2) AS utilidad_rd,
       ROUND(100.0*SUM(utilidad_centavos)/NULLIF(SUM(ingreso_centavos),0),2) AS margen_pct
FROM ventas
GROUP BY ciudad
ORDER BY ingresos_rd DESC;

-- 6. Productos ordenados por margen.
-- El margen alto no implica necesariamente una gran contribución en valor absoluto.
SELECT producto,
       ROUND(SUM(ingreso_centavos)/100.0,2) AS ingresos_rd,
       ROUND(SUM(utilidad_centavos)/100.0,2) AS utilidad_rd,
       ROUND(100.0*SUM(utilidad_centavos)/NULLIF(SUM(ingreso_centavos),0),2) AS margen_pct
FROM ventas
GROUP BY producto
ORDER BY margen_pct DESC, utilidad_rd DESC;

-- 7. Participación de cada producto en los ingresos totales.
SELECT producto,
       ROUND(SUM(ingreso_centavos)/100.0,2) AS ingresos_rd,
       ROUND(100.0*SUM(ingreso_centavos)/NULLIF((SELECT SUM(ingreso_centavos) FROM ventas),0),2) AS participacion_ingresos_pct
FROM ventas
GROUP BY producto
ORDER BY participacion_ingresos_pct DESC;

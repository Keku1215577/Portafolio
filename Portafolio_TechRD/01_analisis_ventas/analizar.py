"""ETL auditable: CSV -> validación -> SQLite -> indicadores -> informe HTML."""
import argparse
import csv
import json
import sqlite3
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

BASE = Path(__file__).resolve().parent
FIELDS = ['id_venta','fecha','producto','categoria','ciudad','canal','cantidad','precio_unitario','costo_unitario','descuento_pct']

def number(value, label):
    try:
        n = Decimal(str(value).strip())
    except InvalidOperation:
        raise ValueError(f'{label}: número inválido') from None
    if not n.is_finite():
        raise ValueError(f'{label}: número no finito')
    return n

def cents(value, label):
    n = number(value, label)
    if n < 0 or n > 1_000_000_000 or n != n.quantize(Decimal('.01')):
        raise ValueError(f'{label}: use 0 a 1000000000 con máximo 2 decimales')
    return int(n * 100)

def clean_row(raw):
    r = {k: str(raw.get(k) or '').strip() for k in FIELDS}
    if any(not r[k] for k in FIELDS):
        raise ValueError('Hay campos vacíos')
    try:
        r['fecha'] = date.fromisoformat(r['fecha']).isoformat()
    except ValueError:
        raise ValueError('Fecha inválida; use AAAA-MM-DD') from None
    q = number(r['cantidad'], 'cantidad')
    if q != q.to_integral_value() or not 1 <= q <= 1_000_000:
        raise ValueError('Cantidad: debe ser un entero positivo hasta 1000000')
    r['cantidad'] = int(q)
    price = cents(r['precio_unitario'], 'precio_unitario')
    cost = cents(r['costo_unitario'], 'costo_unitario')
    discount = number(r['descuento_pct'], 'descuento_pct')
    if not 0 <= discount <= 100:
        raise ValueError('Descuento fuera del rango 0–100')
    r['precio_unitario'] = price/100
    r['costo_unitario'] = cost/100
    r['descuento_pct'] = float(discount)
    r['ingreso_centavos'] = int((Decimal(price)*int(q)*(1-discount/100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    r['costo_centavos'] = cost*int(q)
    r['utilidad_centavos'] = r['ingreso_centavos']-r['costo_centavos']
    return r

def extract(path):
    accepted, rejected, seen = [], [], {}
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not set(FIELDS).issubset(reader.fieldnames):
            raise ValueError('Columnas requeridas: '+', '.join(FIELDS))
        for line, raw in enumerate(reader, 2):
            try:
                if None in raw:
                    raise ValueError('La fila tiene más columnas que el encabezado')
                r = clean_row(raw)
                key = r['id_venta']
                if key in seen:
                    raise ValueError('Duplicado exacto' if r == seen[key] else 'ID repetido con valores diferentes')
                seen[key] = r
                accepted.append(r)
            except ValueError as e:
                rejected.append({'linea':line,'id_venta':raw.get('id_venta',''),'motivo':str(e),'fila_original':json.dumps(raw,ensure_ascii=False)})
    return accepted, rejected

def write_csv(path, rows, fields):
    with Path(path).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

def run(source, out):
    accepted, rejected = extract(source)
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    fields = FIELDS+['ingreso_centavos','costo_centavos','utilidad_centavos']
    write_csv(out/'ventas_limpias.csv', accepted, fields)
    write_csv(out/'filas_rechazadas.csv', rejected, ['linea','id_venta','motivo','fila_original'])
    db = sqlite3.connect(out/'analisis.sqlite3')
    db.row_factory = sqlite3.Row
    try:
        with db:
            db.execute('DROP TABLE IF EXISTS ventas')
            definitions = [f'{k} '+('INTEGER' if k in ['cantidad','ingreso_centavos','costo_centavos','utilidad_centavos'] else 'REAL' if k in ['precio_unitario','costo_unitario','descuento_pct'] else 'TEXT') for k in fields]
            db.execute('CREATE TABLE ventas ('+', '.join(definitions)+', PRIMARY KEY(id_venta))')
            db.executemany('INSERT INTO ventas VALUES ('+','.join('?' for _ in fields)+')', [tuple(r[k] for k in fields) for r in accepted])
            db.execute('CREATE INDEX idx_ventas_fecha ON ventas(fecha)')
        total = sum(r['ingreso_centavos'] for r in accepted)
        profit = sum(r['utilidad_centavos'] for r in accepted)
        summary = {'filas_origen':len(accepted)+len(rejected),'filas_validas':len(accepted),'filas_rechazadas':len(rejected),'ingresos_rd':total/100,'utilidad_bruta_rd':profit/100,'margen_bruto_pct':round(profit/total*100,2) if total else 0,'ticket_promedio_rd':round(total/100/len(accepted),2) if accepted else 0}
        monthly = [dict(r) for r in db.execute("SELECT substr(fecha,1,7) AS mes, ROUND(SUM(ingreso_centavos)/100.0,2) AS ingresos_rd, ROUND(SUM(utilidad_centavos)/100.0,2) AS utilidad_rd FROM ventas GROUP BY mes ORDER BY mes")]
        write_csv(out/'ventas_por_mes.csv', monthly, ['mes','ingresos_rd','utilidad_rd'])
        top = db.execute('SELECT producto, SUM(utilidad_centavos)/100.0 AS utilidad FROM ventas GROUP BY producto ORDER BY utilidad DESC, producto LIMIT 1').fetchone()
    finally:
        db.close()
    (out/'resumen.json').write_text(json.dumps(summary, indent=2,ensure_ascii=False), encoding='utf-8')
    payload = json.dumps({'rows':accepted,'quality':summary},ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    template = (BASE/'plantilla.html').read_text(encoding='utf-8')
    (out/'dashboard.html').write_text(template.replace('__DATA__',payload), encoding='utf-8')
    insight = f"El producto con mayor utilidad bruta total es {top['producto']}: RD$ {top['utilidad']:,.2f}." if top else 'No hay ventas válidas para analizar.'
    (out/'hallazgos.md').write_text(f'''# Análisis de ventas — TechRD\n\nDataset de demostración; no representa una empresa real.\n\n- Filas recibidas: {summary['filas_origen']}. Válidas: {len(accepted)}. Rechazadas: {len(rejected)}.\n- Ingresos después de descuentos: RD$ {total/100:,.2f}.\n- Utilidad bruta: RD$ {profit/100:,.2f}. Margen bruto: {summary['margen_bruto_pct']}%.\n- {insight}\n\n## Decisión propuesta\nRevisar disponibilidad y reposición del producto que más aporta a la utilidad; contrastar con rotación, inversión y demanda antes de comprar. Comparar Online y Tienda con los filtros del dashboard. Estos resultados describen el dataset; no demuestran causalidad.\n\n## Definiciones y límites\nCada fila válida es una venta de un único producto; id_venta es único. Ingresos = cantidad × precio × (1 − descuento/100), redondeado a centavos por venta. Costo = cantidad × costo unitario. Utilidad bruta = ingresos − costo. Margen = utilidad bruta / ingresos. Ticket promedio = ingresos / ventas. No se modelan impuestos, devoluciones ni gastos operativos; utilidad bruta no es beneficio neto. Moneda: DOP (RD$).\n\nLos IDs repetidos conservan la primera fila válida y rechazan las posteriores. Los conflictos quedan identificados para revisión; no se supone que la primera fila sea la versión correcta del negocio. Las filas incompletas o inválidas se ponen en cuarentena sin imputar valores.\n''',encoding='utf-8')
    print(json.dumps(summary, indent=2,ensure_ascii=False))
    print(f'Abre en tu navegador: {(out/"dashboard.html").resolve()}')
    return summary

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada', type=Path, default=BASE/'datos'/'ventas_demo.csv')
    parser.add_argument('--salida', type=Path, default=BASE/'salidas')
    args = parser.parse_args()
    try:
        run(args.entrada, args.salida)
    except (ValueError, OSError, csv.Error, sqlite3.Error) as e:
        parser.exit(1, f'Error: {e}\n')

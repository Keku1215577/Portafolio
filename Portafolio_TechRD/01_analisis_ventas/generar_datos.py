"""Genera ventas ficticias reproducibles con problemas de calidad intencionales."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

FIELDS = ['id_venta','fecha','producto','categoria','ciudad','canal','cantidad','precio_unitario','costo_unitario','descuento_pct']
CATALOGO = [('Laptop 14','Computadoras',38500,28500),('Monitor 24','Monitores',8900,6100),('Mouse USB','Accesorios',650,290),('Teclado','Accesorios',1450,780),('SSD 500 GB','Almacenamiento',3200,2100),('Memoria RAM 16 GB','Componentes',2800,1700)]

def generar(path):
    rng = random.Random(42)
    rows = []
    for i in range(720):
        p, cat, price, cost = rng.choice(CATALOGO)
        rows.append(dict(zip(FIELDS, [f'V{i+1:04d}',str(date(2026,1,1)+timedelta(days=rng.randrange(243))),p,cat,rng.choice(['Santo Domingo','Santiago','La Romana']),rng.choice(['Tienda','Online']),rng.randint(1,5),price,cost,rng.choice([0,0,5,10])])))
    rows += [r.copy() for r in rows[:12]]
    for field, bad in [('fecha','2026-02-30'),('cantidad','-2'),('precio_unitario',''),('descuento_pct','150'),('ciudad','')]:
        r = rows[30].copy()
        r['id_venta'] = 'ERROR_'+field
        r[field] = bad
        rows.append(r)
    # Espacios y formatos que sí se pueden normalizar.
    rows[15]['ciudad'] = '  Santo Domingo  '
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader(); w.writerows(rows)
    print(f'Datos ficticios: {len(rows)} filas en {path}')

if __name__ == '__main__':
    generar(Path(__file__).parent/'datos'/'ventas_demo.csv')

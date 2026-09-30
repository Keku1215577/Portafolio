"""Reglas de negocio independientes de Tkinter. Dinero almacenado en centavos."""
import csv
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

SCHEMA = '''
CREATE TABLE IF NOT EXISTS productos (
 id INTEGER PRIMARY KEY, sku TEXT NOT NULL UNIQUE COLLATE NOCASE,
 nombre TEXT NOT NULL, categoria TEXT NOT NULL,
 precio INTEGER NOT NULL CHECK(precio>=0), costo INTEGER NOT NULL CHECK(costo>=0),
 stock INTEGER NOT NULL CHECK(stock>=0), minimo INTEGER NOT NULL CHECK(minimo>=0),
 activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0,1))
);
CREATE TABLE IF NOT EXISTS ventas (
 id INTEGER PRIMARY KEY, fecha TEXT NOT NULL,
 producto_id INTEGER NOT NULL REFERENCES productos(id),
 producto TEXT NOT NULL, categoria TEXT NOT NULL,
 ciudad TEXT NOT NULL, canal TEXT NOT NULL CHECK(canal IN ('Tienda','Online')),
 cantidad INTEGER NOT NULL CHECK(cantidad>0),
 precio INTEGER NOT NULL CHECK(precio>=0), costo INTEGER NOT NULL CHECK(costo>=0)
);
CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas(fecha);
'''

def texto(value, label):
    value = str(value).strip()
    if not value or len(value) > 120:
        raise ValueError(f'{label}: obligatorio, máximo 120 caracteres.')
    return value

def entero(value, label, positive=False):
    try:
        n = int(str(value))
    except (ValueError, TypeError):
        raise ValueError(f'{label}: escriba un número entero.') from None
    if not (1 if positive else 0) <= n <= 1_000_000:
        raise ValueError(f'{label}: valor fuera del rango permitido.')
    return n

def dinero(value):
    try:
        n = Decimal(str(value).strip())
    except InvalidOperation:
        raise ValueError('Precio/costo: número inválido; use punto decimal.') from None
    if not n.is_finite() or not 0 <= n <= 1_000_000_000 or n != n.quantize(Decimal('.01')):
        raise ValueError('Precio/costo: use un valor positivo o cero con máximo 2 decimales.')
    return int(n*100)

class Inventario:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.conexion() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def conexion(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            db.close()

    def guardar(self, sku, nombre, categoria, precio, costo, stock, minimo, producto_id=None):
        values = (texto(sku,'SKU').upper(), texto(nombre,'Nombre'), texto(categoria,'Categoría'), dinero(precio), dinero(costo), entero(stock,'Stock'), entero(minimo,'Stock mínimo'))
        try:
            with self.conexion() as db:
                if producto_id is None:
                    return db.execute('INSERT INTO productos(sku,nombre,categoria,precio,costo,stock,minimo) VALUES(?,?,?,?,?,?,?)',values).lastrowid
                cur = db.execute('UPDATE productos SET sku=?,nombre=?,categoria=?,precio=?,costo=?,stock=?,minimo=? WHERE id=? AND activo=1',values+(producto_id,))
                if cur.rowcount != 1:
                    raise ValueError('El producto ya no está activo o no existe.')
                return producto_id
        except sqlite3.IntegrityError as e:
            if 'UNIQUE' in str(e):
                raise ValueError('Este SKU ya existe, incluso si está archivado.') from None
            raise

    def listar(self, busqueda='', incluir_archivados=False):
        with self.conexion() as db:
            return [dict(r) for r in db.execute('SELECT * FROM productos WHERE (? OR activo=1) AND (instr(lower(nombre),lower(?))>0 OR instr(lower(sku),lower(?))>0) ORDER BY nombre',(int(incluir_archivados),busqueda,busqueda))]

    def archivar(self, producto_id):
        with self.conexion() as db:
            if db.execute('UPDATE productos SET activo=0 WHERE id=? AND activo=1',(producto_id,)).rowcount != 1:
                raise ValueError('Seleccione un producto activo.')

    def vender(self, producto_id, cantidad, ciudad='Santo Domingo', canal='Tienda'):
        cantidad = entero(cantidad,'Cantidad',positive=True)
        ciudad = texto(ciudad,'Ciudad')
        if canal not in ('Tienda','Online'):
            raise ValueError('Canal no válido.')
        with self.conexion() as db:
            # Reserva la escritura antes de consultar: evita sobreventa concurrente.
            db.execute('BEGIN IMMEDIATE')
            p = db.execute('SELECT * FROM productos WHERE id=? AND activo=1',(producto_id,)).fetchone()
            if p is None:
                raise ValueError('El producto no existe o está archivado.')
            if p['stock'] < cantidad:
                raise ValueError(f"Stock insuficiente. Disponible: {p['stock']}.")
            db.execute('UPDATE productos SET stock=stock-? WHERE id=?',(cantidad,producto_id))
            sale_id = db.execute('INSERT INTO ventas(fecha,producto_id,producto,categoria,ciudad,canal,cantidad,precio,costo) VALUES(?,?,?,?,?,?,?,?,?)', (datetime.now().isoformat(timespec='seconds'),producto_id,p['nombre'],p['categoria'],ciudad,canal,cantidad,p['precio'],p['costo'])).lastrowid
            return sale_id

    def ventas(self):
        with self.conexion() as db:
            return [dict(r) for r in db.execute('SELECT *,cantidad*precio AS total,cantidad*(precio-costo) AS utilidad FROM ventas ORDER BY fecha DESC,id DESC')]

    def resumen(self):
        with self.conexion() as db:
            p = dict(db.execute('SELECT COUNT(*) AS productos, COALESCE(SUM(stock*costo),0) AS valor, COALESCE(SUM(stock<=minimo),0) AS alertas FROM productos WHERE activo=1').fetchone())
            p.update(dict(db.execute('SELECT COUNT(*) AS ventas,COALESCE(SUM(cantidad*precio),0) AS ingresos FROM ventas').fetchone()))
            return p

    def exportar(self, path):
        fields=['id_venta','fecha','producto','categoria','ciudad','canal','cantidad','precio_unitario','costo_unitario','descuento_pct']
        with Path(path).open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
            for v in self.ventas():
                w.writerow(dict(zip(fields,[f"INV-{v['id']}",v['fecha'][:10],v['producto'],v['categoria'],v['ciudad'],v['canal'],v['cantidad'],f"{v['precio']/100:.2f}",f"{v['costo']/100:.2f}",0])))

    def datos_demo(self):
        # No duplica el catálogo al abrir la aplicación nuevamente.
        with self.conexion() as db:
            if db.execute('SELECT COUNT(*) FROM productos').fetchone()[0]:
                return
            db.executemany('INSERT INTO productos(sku,nombre,categoria,precio,costo,stock,minimo) VALUES(?,?,?,?,?,?,?)',[
                ('LAP-001','Laptop 14','Computadoras',3850000,2850000,12,3),
                ('MON-001','Monitor 24','Monitores',890000,610000,18,4),
                ('MOU-001','Mouse USB','Accesorios',65000,29000,4,5),
                ('SSD-001','SSD 500 GB','Almacenamiento',320000,210000,20,5)])

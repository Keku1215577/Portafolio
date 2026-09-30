import csv
import sqlite3
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from servicio import Inventario

class InventarioTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.service=Inventario(Path(self.tmp.name)/'test.sqlite3')
        self.pid=self.service.guardar('SKU-1','Mouse','Accesorios','100.25','60.10',5,2)
    def tearDown(self):self.tmp.cleanup()
    def test_venta_descuenta_stock_y_conserva_precio_historico(self):
        self.service.vender(self.pid,2)
        self.assertEqual(self.service.listar()[0]['stock'],3)
        self.service.guardar('SKU-1','Mouse nuevo','Accesorios','200','90',3,2,self.pid)
        sale=self.service.ventas()[0]
        self.assertEqual(sale['total'],20050)
        self.assertEqual(sale['utilidad'],8030)
        self.assertEqual(sale['producto'],'Mouse')
    def test_rechaza_sobreventa_sin_mutaciones(self):
        with self.assertRaises(ValueError):self.service.vender(self.pid,6)
        self.assertEqual(self.service.listar()[0]['stock'],5)
        self.assertEqual(self.service.ventas(),[])
    def test_rollback_si_falla_insertar_venta(self):
        with self.service.conexion() as db:
            db.execute("CREATE TRIGGER falla BEFORE INSERT ON ventas BEGIN SELECT RAISE(ABORT,'fallo simulado'); END")
        with self.assertRaises(sqlite3.IntegrityError):self.service.vender(self.pid,2)
        self.assertEqual(self.service.listar()[0]['stock'],5)
    def test_dos_compras_concurrentes_no_generan_stock_negativo(self):
        def buy(_):
            try:self.service.vender(self.pid,4);return True
            except ValueError:return False
        with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(buy,range(2)))
        self.assertEqual(sorted(results),[False,True])
        self.assertEqual(self.service.listar()[0]['stock'],1)
    def test_sku_unico_incluso_archivado(self):
        self.service.archivar(self.pid)
        with self.assertRaises(ValueError):self.service.guardar('sku-1','Otro','Otra',1,0,1,0)
        with self.assertRaises(ValueError):self.service.vender(self.pid,1)
        self.assertEqual(self.service.listar(),[])
    def test_exportacion_y_persistencia(self):
        self.service.vender(self.pid,1,'Santiago','Online')
        other=Inventario(self.service.path)
        self.assertEqual(other.resumen()['ingresos'],10025)
        path=Path(self.tmp.name)/'ventas.csv';other.exportar(path)
        with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual(rows[0]['precio_unitario'],'100.25')
        self.assertEqual(rows[0]['ciudad'],'Santiago')
    def test_validaciones(self):
        for bad in ['-1','nan','Infinity','12.345','texto']:
            with self.subTest(bad=bad),self.assertRaises(ValueError):self.service.guardar('OTRO','P','C',bad,0,1,0)
        for bad in [0,-1,'1.5','abc']:
            with self.subTest(bad=bad),self.assertRaises(ValueError):self.service.vender(self.pid,bad)

if __name__=='__main__':unittest.main()

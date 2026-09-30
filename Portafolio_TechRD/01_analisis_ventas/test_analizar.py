import csv
import tempfile
import unittest
from pathlib import Path
from analizar import clean_row, extract, run, FIELDS

BASE_ROW=dict(zip(FIELDS,['V1','2026-01-01','Mouse','Accesorios','Santo Domingo','Online','2','100.25','60.10','5']))
class AnalisisTests(unittest.TestCase):
    def test_calculos_y_normalizacion(self):
        row=clean_row({**BASE_ROW,'ciudad':' Santo Domingo '})
        self.assertEqual(row['ingreso_centavos'],19048)
        self.assertEqual(row['utilidad_centavos'],7028)
        self.assertEqual(row['ciudad'],'Santo Domingo')
    def test_datos_invalidos(self):
        for k,v in [('fecha','2026-02-30'),('cantidad','-1'),('cantidad','1.2'),('precio_unitario','NaN'),('costo_unitario',''),('descuento_pct','101')]:
            with self.subTest(k=k,v=v),self.assertRaises(ValueError):clean_row({**BASE_ROW,k:v})
    def test_rechazo_duplicados_y_conflictos(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'input.csv'
            with path.open('w',encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows([BASE_ROW,BASE_ROW,{**BASE_ROW,'cantidad':'3'}])
            rows,errors=extract(path)
            self.assertEqual(len(rows),1)
            self.assertEqual([r['motivo'] for r in errors],['Duplicado exacto','ID repetido con valores diferentes'])
    def test_archivo_vacio_genera_reporte(self):
        with tempfile.TemporaryDirectory() as t:
            source=Path(t)/'input.csv';source.write_text(','.join(FIELDS)+'\n',encoding='utf-8')
            result=run(source,Path(t)/'output')
            self.assertEqual(result['filas_validas'],0)
            self.assertTrue((Path(t)/'output'/'dashboard.html').exists())
    def test_demo_resultados_reproducibles(self):
        rows,errors=extract(Path(__file__).parent/'datos'/'ventas_demo.csv')
        self.assertEqual((len(rows),len(errors)),(720,17))
        self.assertEqual(sum(r['ingreso_centavos'] for r in rows),1999169750)
        self.assertEqual(sum(r['utilidad_centavos'] for r in rows),513074750)

if __name__=='__main__':unittest.main()

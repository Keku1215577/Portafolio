"""Aplicación de escritorio local. Ejecutar: python app.py."""
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, filedialog
from servicio import Inventario

BASE = Path(__file__).resolve().parent

def rd(cents):
    return f'RD$ {cents/100:,.2f}'

class App(tk.Tk):
    def __init__(self, db_path=BASE/'datos'/'inventario.sqlite3'):
        super().__init__()
        self.title('TechRD | Inventario y ventas')
        self.geometry('1180x760'); self.minsize(1000,680)
        self.configure(bg='#edf3f8')
        self.service=Inventario(db_path); self.service.datos_demo()
        self.selected_id=None
        style=ttk.Style(self);style.theme_use('clam')
        style.configure('TFrame',background='#edf3f8')
        style.configure('TLabel',background='#edf3f8',font=('Segoe UI',10))
        style.configure('Title.TLabel',font=('Segoe UI',23,'bold'),foreground='#12364a')
        style.configure('TButton',font=('Segoe UI',10),padding=8)
        style.configure('Treeview',rowheight=30,font=('Segoe UI',10))
        style.configure('Treeview.Heading',font=('Segoe UI',10,'bold'))
        outer=ttk.Frame(self,padding=22);outer.pack(fill='both',expand=True)
        ttk.Label(outer,text='TechRD / Inventario y ventas',style='Title.TLabel').pack(anchor='w')
        ttk.Label(outer,text='Proyecto de práctica · Catálogo ficticio · Moneda: pesos dominicanos').pack(anchor='w',pady=(4,16))
        self.metrics=tk.StringVar();ttk.Label(outer,textvariable=self.metrics,font=('Segoe UI',11,'bold')).pack(anchor='w',pady=(0,16))
        tabs=ttk.Notebook(outer);tabs.pack(fill='both',expand=True)
        products=ttk.Frame(tabs,padding=14);sales=ttk.Frame(tabs,padding=14)
        tabs.add(products,text='Productos y ventas');tabs.add(sales,text='Historial y exportación')
        self.build_products(products);self.build_sales(sales)
        self.status=tk.StringVar(value='Listo. Seleccione un producto para editarlo o venderlo.')
        ttk.Label(outer,textvariable=self.status).pack(anchor='w',pady=(12,0))
        self.refresh()

    def build_products(self,parent):
        searchbar=ttk.Frame(parent);searchbar.pack(fill='x',pady=(0,10))
        ttk.Label(searchbar,text='Buscar nombre o SKU:').pack(side='left')
        self.search=tk.StringVar();entry=ttk.Entry(searchbar,textvariable=self.search,width=35);entry.pack(side='left',padx=10)
        entry.bind('<Return>',lambda e:self.refresh())
        ttk.Button(searchbar,text='Buscar',command=self.refresh).pack(side='left')
        ttk.Button(searchbar,text='Nuevo / limpiar',command=self.clear).pack(side='right')
        self.tree=self.make_tree(parent,[('sku','SKU',100),('nombre','Producto',190),('categoria','Categoría',120),('precio','Precio',115),('costo','Costo',115),('stock','Stock',65),('minimo','Mínimo',65),('estado','Estado',120)],8)
        self.tree.tag_configure('bajo',foreground='#ad3e16',background='#fff2e5')
        self.tree.bind('<<TreeviewSelect>>',self.select)
        form=ttk.Frame(parent);form.pack(fill='x',pady=12)
        self.fields={}
        definitions=[('sku','SKU'),('nombre','Nombre'),('categoria','Categoría'),('precio','Precio RD$'),('costo','Costo RD$'),('stock','Stock'),('minimo','Mínimo')]
        for i,(key,label) in enumerate(definitions):
            ttk.Label(form,text=label).grid(row=(i//4)*2,column=i%4,sticky='w',padx=(0,12),pady=(4,0))
            var=tk.StringVar(value='0' if key in ['precio','costo','stock','minimo'] else '')
            self.fields[key]=var
            ttk.Entry(form,textvariable=var,width=23).grid(row=(i//4)*2+1,column=i%4,sticky='ew',padx=(0,12))
        for i in range(4):form.columnconfigure(i,weight=1)
        actions=ttk.Frame(parent);actions.pack(fill='x')
        ttk.Button(actions,text='Guardar producto',command=self.save).pack(side='left')
        ttk.Button(actions,text='Archivar seleccionado',command=self.archive).pack(side='left',padx=10)
        ttk.Label(parent,text='Venta rápida del producto seleccionado (guarde primero cualquier cambio):').pack(anchor='w',pady=(16,6))
        bar=ttk.Frame(parent);bar.pack(fill='x')
        self.quantity=tk.StringVar(value='1');self.city=tk.StringVar(value='Santo Domingo');self.channel=tk.StringVar(value='Tienda')
        ttk.Label(bar,text='Unidades').pack(side='left');ttk.Entry(bar,textvariable=self.quantity,width=7).pack(side='left',padx=8)
        ttk.Label(bar,text='Ciudad').pack(side='left');ttk.Entry(bar,textvariable=self.city,width=22).pack(side='left',padx=8)
        ttk.Combobox(bar,textvariable=self.channel,values=['Tienda','Online'],state='readonly',width=10).pack(side='left',padx=8)
        ttk.Button(bar,text='Registrar venta',command=self.sell).pack(side='left',padx=8)

    def make_tree(self,parent,columns,height):
        frame=ttk.Frame(parent);frame.pack(fill='both',expand=True)
        tree=ttk.Treeview(frame,columns=[c[0] for c in columns],show='headings',height=height,selectmode='browse')
        for key,title,width in columns:
            tree.heading(key,text=title);tree.column(key,width=width,minwidth=55)
        sy=ttk.Scrollbar(frame,orient='vertical',command=tree.yview)
        sx=ttk.Scrollbar(frame,orient='horizontal',command=tree.xview)
        tree.configure(yscrollcommand=sy.set,xscrollcommand=sx.set)
        tree.grid(row=0,column=0,sticky='nsew');sy.grid(row=0,column=1,sticky='ns');sx.grid(row=1,column=0,sticky='ew')
        frame.rowconfigure(0,weight=1);frame.columnconfigure(0,weight=1)
        return tree

    def build_sales(self,parent):
        ttk.Label(parent,text='Las ventas conservan el nombre, precio y costo del momento de la operación.').pack(anchor='w',pady=(0,12))
        self.history=self.make_tree(parent,[('id','Venta',65),('fecha','Fecha',160),('producto','Producto',180),('canal','Canal',90),('cantidad','Unidades',70),('total','Total',130),('utilidad','Utilidad bruta',130)],15)
        ttk.Button(parent,text='Exportar ventas CSV para el proyecto de análisis',command=self.export).pack(anchor='w',pady=14)

    def clear(self):
        self.selected_id=None
        for key,var in self.fields.items():var.set('0' if key in ['precio','costo','stock','minimo'] else '')
        self.tree.selection_remove(self.tree.selection())
        self.status.set('Nuevo producto. Complete los campos y pulse Guardar producto.')

    def refresh(self):
        self.selected_id=None
        self.tree.delete(*self.tree.get_children())
        self.products={p['id']:p for p in self.service.listar(self.search.get())}
        for pid,p in self.products.items():
            low=p['stock']<=p['minimo']
            self.tree.insert('','end',iid=str(pid),values=(p['sku'],p['nombre'],p['categoria'],rd(p['precio']),rd(p['costo']),p['stock'],p['minimo'],'Reponer' if low else 'Disponible'),tags=('bajo',) if low else ())
        self.history.delete(*self.history.get_children())
        for v in self.service.ventas():self.history.insert('','end',values=(v['id'],v['fecha'].replace('T',' '),v['producto'],v['canal'],v['cantidad'],rd(v['total']),rd(v['utilidad'])))
        r=self.service.resumen();self.metrics.set(f"{r['productos']} productos activos   |   {r['alertas']} alertas de stock   |   Inventario a costo: {rd(r['valor'])}   |   Ventas acumuladas: {rd(r['ingresos'])}")
        self.clear()

    def select(self,event=None):
        selection=self.tree.selection()
        if not selection:return
        self.selected_id=int(selection[0]);p=self.products[self.selected_id]
        for key,var in self.fields.items():var.set(f"{p[key]/100:.2f}" if key in ('precio','costo') else str(p[key]))
        self.status.set(f"Seleccionado: {p['nombre']} ({p['sku']})")

    def action(self,callback,success):
        try:
            callback();self.refresh();self.status.set(success)
        except (ValueError,sqlite3.Error,OSError) as e:
            messagebox.showerror('Revise la operación',str(e),parent=self)

    def save(self):
        self.action(lambda:self.service.guardar(**{k:v.get() for k,v in self.fields.items()},producto_id=self.selected_id),'Producto guardado.')

    def archive(self):
        if self.selected_id is None:
            messagebox.showinfo('Seleccione un producto','Seleccione el producto que desea archivar.',parent=self);return
        if messagebox.askyesno('Archivar','¿Ocultar este producto del catálogo activo? Su historial de ventas se conservará.',parent=self):
            self.action(lambda:self.service.archivar(self.selected_id),'Producto archivado.')

    def sell(self):
        if self.selected_id is None:
            messagebox.showinfo('Seleccione un producto','Seleccione un producto de la tabla.',parent=self);return
        if messagebox.askyesno('Confirmar venta',f"¿Registrar {self.quantity.get()} unidades de {self.products[self.selected_id]['nombre']}?",parent=self):
            self.action(lambda:self.service.vender(self.selected_id,self.quantity.get(),self.city.get(),self.channel.get()),'Venta registrada; stock actualizado.')

    def export(self):
        path=filedialog.asksaveasfilename(parent=self,title='Exportar ventas',defaultextension='.csv',initialfile='ventas_inventario.csv',filetypes=[('CSV','*.csv')])
        if path:self.action(lambda:self.service.exportar(path),f'Ventas exportadas: {path}')

if __name__=='__main__':
    App().mainloop()

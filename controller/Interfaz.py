import sys
import os

ruta_actual = os.path.dirname(__file__)
ruta_proyecto = os.path.abspath(os.path.join(ruta_actual, '..'))
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)

import tkinter as tk
from os import system
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET
from controller.ListasDobles import ListaDoble, ListaMovimiento, ListaSistemaDrones, ListaMensaje, ListaMsgProcess, ListaContenido, ListaAlturas, ListaInstruccion
from controller.Nodos import Altura, Contenido, SistemaDrones, Instruccion, Mensaje, Movimientos, MensajeProcesado

class Interfaz():
    def __init__(self):
        self.root = tk.Tk()
        self.file_path = ''
        self.lista_drones = ListaDoble() 
        self.lista_sistemas_mensajes = ListaDoble()
        self.lista_drones_mensajes = ListaDoble()
        self.text_box_agregar_dron = None
        self.tree_view = None
        self.gestion_drones_ventana = None
        self.tree_view_mensaje = None
        self.tree_view_instruccion = None
        
        self.lista_sistema_drones = ListaSistemaDrones()
        self.lista_msg = ListaMensaje()
        self.lista_msg_process = ListaMsgProcess()
        
    def cargar_frame(self):
        wventana = 1000
        hventana = 650
        
        self.root.geometry(f"{wventana}x{hventana}")
        self.root.resizable(0, 0)
        self.root.title("Sistema de Drones - 202200174")
        
        wtotal = self.root.winfo_screenwidth()
        htotal = self.root.winfo_screenheight()
        
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        
        self.root.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        self.root.grid()
        
        barra_menu = tk.Menu(self.root)
        menu_archivo = tk.Menu(barra_menu)
        barra_menu.add_cascade(label='Archivo', menu=menu_archivo)
        menu_archivo.add_command(label='Inicialización', command=None)
        menu_archivo.add_command(label='Cargar Archivo', command=self.cargar_archivo_xml)
        menu_archivo.add_command(label='Generar Archivo', command=self.generar_archivo)
        menu_archivo.add_command(label='Ayuda', command=None)
        menu_archivo.add_command(label='Salir', command=self.salir)
        
        menu_gestiones = tk.Menu(barra_menu)
        barra_menu.add_cascade(label='Gestiones', menu=menu_gestiones)
        menu_gestiones.add_command(label='Gestión de Drones', command=self.gestion_drones)
        menu_gestiones.add_command(label='Gestión de Sistemas Drones', command=self.ventana_gestion_sistemas)
        menu_gestiones.add_command(label='Gestión de Mensajes', command=self.gestion_mensajes)
        
        self.root.config(menu=barra_menu)
        self.root.mainloop()
        
    def salir(self):
        self.root.destroy()
    
    def cargar_archivo_xml(self):
        self.file_path = filedialog.askopenfilename(title="Seleccione un archivo", filetypes=(("XML", "*.xml"), ("all files", "*.*")))
        if self.file_path:
            with open(self.file_path, 'r', encoding='UTF-8') as file:
                try:
                    messagebox.showinfo('Archivo ha sido cargado', 'El archivo ha sido cargado y leído correctamente')
                except FileNotFoundError:
                    messagebox.showerror('ERROR!', "Error al decodificar el archivo XML")
                file.close()
    
    def gestion_drones(self):
        try:
            root = ET.parse(self.file_path).getroot()
            if self.lista_drones.is_empty():
                lista_drones_element = root.find('listaDrones')
                for dron_elements in lista_drones_element.findall('dron'):
                    self.lista_drones.append(dron_elements.text)
                self.lista_drones.organizar_lista_drones()
            
            self.gestion_drones_ventana = tk.Toplevel(self.root)
            self.gestion_drones_ventana.geometry("500x400")
        except FileNotFoundError:
            messagebox.showerror('ERROR!', "Cargué un archivo XML primero, en el apartado de archivo.")
            return
        
        wventana = 750
        hventana = 500
        
        self.gestion_drones_ventana.geometry(f"{wventana}x{hventana}")
        self.gestion_drones_ventana.resizable(0, 0)
        self.gestion_drones_ventana.title("Gestión de Drones")
        
        wtotal = self.gestion_drones_ventana.winfo_screenwidth()
        htotal = self.gestion_drones_ventana.winfo_screenheight()
        
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        
        self.gestion_drones_ventana.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        self.gestion_drones_ventana.grid()
        
        self.tree_view = ttk.Treeview(self.gestion_drones_ventana, columns=('first', 'last'), show='headings')
        self.tree_view.heading('first', text='No.')
        self.tree_view.heading('last', text='Dron')
        
        self.lista_drones.organizar_lista_drones()
        actual = self.lista_drones.head
        size = 0
        while actual:
            size += 1
            self.tree_view.insert('', 'end', values=(size, actual.dron))
            actual = actual.next

        self.text_box_agregar_dron = tk.Entry(self.gestion_drones_ventana, width=20)
        self.text_box_agregar_dron.pack()
        self.text_box_agregar_dron.place(x=300, y=230)
        
        button_agregar_dron = tk.Button(self.gestion_drones_ventana, text="Agregar Dron", command=self.agregar_dron)
        button_agregar_dron.pack()
        button_agregar_dron.place(x=300, y=350)
        
        self.tree_view.pack()

    def agregar_dron(self):
        text = self.text_box_agregar_dron.get().strip()
        
        if self.lista_drones.is_found(text):
            messagebox.showerror('ERROR!', "El dron ya existe.", parent=self.gestion_drones_ventana)
            self.text_box_agregar_dron.delete(0, tk.END)
            return
        
        self.tree_view.delete(*self.tree_view.get_children())
        self.lista_drones.append(text)
        self.text_box_agregar_dron.delete(0, tk.END)
        self.lista_drones.organizar_lista_drones()
        actual = self.lista_drones.head
        size = 0
        while actual:
            size += 1
            self.tree_view.insert('', 'end', values=(size, actual.dron))
            actual = actual.next
            
        messagebox.showinfo('Dron agregado', 'El dron ha sido agregado correctamente.', parent=self.gestion_drones_ventana)
    
    def ventana_gestion_sistemas(self):
        wventana = 500
        hventana = 300
        
        gestion_sistemas_ventana = tk.Toplevel(self.root)
        gestion_sistemas_ventana.geometry(f"{wventana}x{hventana}")
        gestion_sistemas_ventana.resizable(0, 0)
        gestion_sistemas_ventana.title("Gestión de Sistemas")
        
        wtotal = gestion_sistemas_ventana.winfo_screenwidth()
        htotal = gestion_sistemas_ventana.winfo_screenheight()
        
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        
        gestion_sistemas_ventana.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        gestion_sistemas_ventana.grid()
        
        button_agregar_sistema = tk.Button(gestion_sistemas_ventana, text="Graficar Sistemas", command=self.gestion_sistemas_drones)
        button_agregar_sistema.pack()
        button_agregar_sistema.place(x=200, y=150)

    
    def gestion_sistemas_drones(self):
        contador_sistema = 0
        graph_body = ''
        graph_head = 'digraph G {\nnode [shape=plaintext];\n'
        graph_footer = '\n}'
        root = ET.parse(self.file_path).getroot()
        lista_sistemas_drones_element = root.find('listaSistemasDrones')
        
        graph_table = ''
        for sistema_drones_elements in lista_sistemas_drones_element.findall('sistemaDrones'):            
            lista_sistemas_drones = ListaDoble()
            contador_sistema += 1
            nombre_sistema = sistema_drones_elements.get('nombre')
            altura_maxima = sistema_drones_elements.find('alturaMaxima').text
            
            graph_table = f'table_{nombre_sistema} [label = \n'
            graph_table += '<<table border="1" cellspacing="0">\n'
            for dron_contenido in sistema_drones_elements.findall('contenido'):
                contador_altura = 0
                dron_nombre = dron_contenido.find('dron').text
                alturas_element = dron_contenido.find('alturas')
                for altura_element in alturas_element.findall('altura'):
                    contador_altura += 1
                    dron_valor = altura_element.text
                    dron_altura = altura_element.get('valor')
                    
                    if contador_altura > int(altura_maxima):
                        messagebox.showerror('ERROR!', "La cantidad de alturas es mayor a la altura máxima.", parent=self.gestion_drones_ventana)
                        return
                    lista_sistemas_drones.append_mensaje(dron_nombre, dron_altura, dron_valor, nombre_sistema)
            graph_new = ''
            graph_table += lista_sistemas_drones.graficar(None, graph_new, nombre_sistema, lista_sistemas_drones)
            graph_table += '</table>>\n];\n'
            graph_body += graph_table
        
        graph = graph_head + graph_body + graph_footer
        with open('graphviz_sistema_drones_202200174.dot', 'w', encoding='UTF-8') as archivo:
            archivo.write(graph)
            archivo.close()
            
        system('dot -Tpng graphviz_sistema_drones_202200174.dot -o graphviz_sistema_drones_202200174.png')
        system('cd ./graphviz_sistema_drones_202200174.png')
        messagebox.showinfo('Sistemas de Drones', 'Los sistemas de drones han sido graficados correctamente.')
        
    def gestion_mensajes(self):
        
        root = ET.parse(self.file_path).getroot()
        
        wventana = 750
        hventana = 500
        
        gestion_mensajes_ventana = tk.Toplevel(self.root)
        gestion_mensajes_ventana.geometry(f"{wventana}x{hventana}")
        gestion_mensajes_ventana.resizable(0, 0)
        gestion_mensajes_ventana.title("Gestión de Mensajes")
        
        wtotal = gestion_mensajes_ventana.winfo_screenwidth()
        htotal = gestion_mensajes_ventana.winfo_screenheight()
        
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        
        gestion_mensajes_ventana.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        gestion_mensajes_ventana.grid()
        
        self.tree_view_mensaje = ttk.Treeview(gestion_mensajes_ventana, columns=('first', 'last'), show='headings')
        self.tree_view_mensaje.heading('first', text='Nombre')
        self.tree_view_mensaje.heading('last', text='Sistema de Drones')
        self.tree_view_mensaje.pack()
        
        button_gestions_mensajes = ttk.Button(gestion_mensajes_ventana, text="Gestión de Mensajes", command=self.graficar_mensajes)
        button_gestions_mensajes.pack()
        
        self.tree_view_instruccion = ttk.Treeview(gestion_mensajes_ventana, columns=('first', 'last'), show='headings')
        self.tree_view_instruccion.heading('first', text='Dron')
        self.tree_view_instruccion.heading('last', text='Instrucción')
        self.tree_view_instruccion.pack()
        self.tree_view_instruccion.place(x=175, y=250)

        lista_mensaje = root.find('listaMensajes')
        for mensaje_element in lista_mensaje.findall('Mensaje'):
            nombre_msg = mensaje_element.get('nombre')
            
            sistema_drones_element = mensaje_element.find('sistemaDrones')
            sistema_drones_nombre = sistema_drones_element.text
            
            self.tree_view_mensaje.insert('', 'end', values=(nombre_msg, sistema_drones_nombre))
                
        self.tree_view_mensaje.bind('<<TreeviewSelect>>', self.on_select_tree)

    def on_select_tree(self, event):
        item_seleccionado = self.tree_view_mensaje.selection()
        if item_seleccionado:
            opcion_mensaje = self.tree_view_mensaje.item(item_seleccionado)["values"][0]
            opcion_sistema_drones = self.tree_view_mensaje.item(item_seleccionado)["values"][1]
        
        root = ET.parse(self.file_path).getroot()
        for mensaje_element in root.findall(".//Mensaje"):
            nombre_mensaje = mensaje_element.get('nombre')
            self.lista_sistemas_mensajes.clear()
            self.tree_view_instruccion.delete(*self.tree_view_instruccion.get_children())
            if nombre_mensaje == opcion_mensaje:
                sistema_drones_element = mensaje_element.find('sistemaDrones')
                sistema_drones = sistema_drones_element.text
                
                if sistema_drones == opcion_sistema_drones:
                    instrucciones_element = mensaje_element.find('instrucciones')
                    
                    for instruccion_element in instrucciones_element.findall('instruccion'):
                        dron_inst = instruccion_element.get('dron')
                        valor_dron_inst = instruccion_element.text
                        
                        self.lista_sistemas_mensajes.append_inst(dron_inst, valor_dron_inst)
                        
                actual = self.lista_sistemas_mensajes.head
                while actual:
                    self.tree_view_instruccion.insert('', 'end', values=(actual.dron, actual.altura))
                    actual = actual.next
                break
    
    def graficar_mensajes(self):
        item_seleccionado = self.tree_view_mensaje.selection()
        if item_seleccionado:
            opcion_sistema_drones = self.tree_view_mensaje.item(item_seleccionado)["values"][1]
        
        root = ET.parse(self.file_path).getroot()
        lista_sistema_drones = root.find("listaSistemasDrones")
        for sistema_drones_elements in lista_sistema_drones.findall('sistemaDrones'):
            sistema_drones = sistema_drones_elements.get('nombre')
            
            if sistema_drones == opcion_sistema_drones:
                self.lista_drones_mensajes.clear()
                contador_drones = 0
                cantidad_drones = sistema_drones_elements.find('cantidadDrones').text
                
                for dron_contenido in sistema_drones_elements.findall('contenido'):
                    contador_drones += 1
                    nombre_dron = dron_contenido.find('dron').text
                    if contador_drones > int(cantidad_drones):
                        messagebox.showerror('ERROR!', "La cantidad de drones es mayor a la cantidad de drones permitidos.", parent=self.gestion_drones_ventana)
                        self.lista_drones_mensajes.clear()
                        return
                    
                    self.lista_drones.append(nombre_dron)
                    for dron_alturas in dron_contenido.find('alturas'):
                        dron_letra = dron_alturas.text
                        dron_altura = dron_alturas.get('valor')
                        self.lista_drones_mensajes.append_mensaje(nombre_dron, dron_altura, dron_letra, None)
        
        root = ET.parse(self.file_path).getroot()
        lista_mensajes = root.find("listaMensajes")
        for mensaje_element in lista_mensajes.findall("Mensaje"):
            
            sistema_drones_element = mensaje_element.find('sistemaDrones')
            sistema_drones = sistema_drones_element.text
                
            if sistema_drones == opcion_sistema_drones:
                nombre_mensaje = mensaje_element.get('nombre')
                instrucciones_element = mensaje_element.find('instrucciones')
                    
                for instruccion_element in instrucciones_element.findall('instruccion'):
                    dron_inst = instruccion_element.get('dron')
                    valor_dron_inst = instruccion_element.text
                    self.lista_drones_mensajes.update(dron_inst, valor_dron_inst)
        
        graph_head = 'digraph G {\nnode [shape=plaintext];\ntable [label = \n'
        graph_body = '<<table border="1" cellspacing="0">'
        
        graph_body = self.lista_drones_mensajes.graficar(nombre_mensaje=nombre_mensaje, graph_body=graph_body, sistema_drones=opcion_sistema_drones, lista=self.lista_drones_mensajes)
        graph_footer = '</table>>\n];\n}'
        graph = graph_head + graph_body + graph_footer
        nombre_sin_espacios = f'{opcion_sistema_drones}'.replace(' ', '_')
        with open(f'graphviz_{nombre_sin_espacios}.dot', 'w', encoding='UTF-8') as archivo:
            archivo.write(graph)
            archivo.close()
            
        system(f'dot -Tpng graphviz_{nombre_sin_espacios}.dot -o graphviz_{nombre_sin_espacios}.png')
        system(f'cd ./graphviz_{nombre_sin_espacios}.png')
        
    def generar_archivo(self):
        root = ET.parse(self.file_path).getroot()
        
        for drones in root.findall('./listaSistemasDrones/sistemaDrones'):
            nombre = drones.get('nombre')
            altura_max = drones.find('alturaMaxima').text
            cantidad_drones = drones.find('cantidadDrones').text
            
            lista_contenido = ListaContenido()
            count = 1
            for contenidos in drones.findall('contenido'):
                dron_contenido = contenidos.find('dron').text
                lista_alturas = ListaAlturas()
                
                for alturas_dron in contenidos.findall('./alturas/altura'):
                    altura_nueva = Altura(alturas_dron.get('valor'), alturas_dron.text, dron_contenido, count)
                    lista_alturas.append(altura_nueva)
                count += 1
                
                contenido_nuevo = Contenido(dron_contenido, lista_alturas)
                lista_contenido.append(contenido_nuevo)
                
            nuevo_sistema = SistemaDrones(nombre, altura_max, cantidad_drones, lista_contenido)
            self.lista_sistema_drones.append(nuevo_sistema)
        
        for mensajes in root.findall('./listaMensajes/Mensaje'):
            sistema_drones_mensaje = mensajes.find('sistemaDrones').text
            lista_inst = ListaInstruccion()
            
            for instrucciones in mensajes.findall('./instrucciones/instruccion'):
                nueva_inst = Instruccion(instrucciones.get('dron'), instrucciones.text)
                lista_inst.append(nueva_inst)
                
            nuevo_msg = Mensaje(mensajes.get('nombre'), sistema_drones_mensaje, lista_inst)
            self.lista_msg.append(nuevo_msg)
        
        self.calcular_datos()
        self.lista_msg_process.generar_xml(self.lista_msg_process)
        messagebox.showinfo('Archivo generado', 'El archivo .xml ha sido generado correctamente.')
        
    def calcular_datos(self):
        for mensajes in self.lista_msg:
            mensaje = ''
            lista_mov = ListaMovimiento()
            sistema = self.lista_sistema_drones.get_sistema(mensajes.sistema)
            for index, inst in enumerate(mensajes.instrucciones):
                tiempo = 0
                self.mover_dron(inst.instruccion, inst.dron, lista_mov, tiempo, index)
                alturas_dron = sistema.contenido.get_contenido(inst.dron)
                for alturas in alturas_dron.alturas:
                    if inst.instruccion == alturas.altura:
                        mensaje += alturas.valor
            
            for index, list_inst in enumerate(mensajes.instrucciones):
                lista_mov.complete_esperar(list_inst.dron, list_inst.instruccion, index)
            tiempo_optimo = lista_mov.get_mayor_tiempo()
            
            nuevo_msg_process = MensajeProcesado(mensajes.nombre_msg, mensaje, sistema.nombre, tiempo_optimo, lista_mov)
            self.lista_msg_process.append(nuevo_msg_process)
    
    def mover_dron(self, altura, dron, list_mov, tiempo, num):
        tiempo_actual = tiempo
        tiempo_final = int(list_mov.get_tiempo_dron(dron))
        altura_actual = int(list_mov.get_movimientos_dron(dron))
        altura_final = int(altura)
        indice = int(list_mov.get_indice_dron(dron, num))
        
        if tiempo_final > 0:
            tiempo_actual = tiempo_final
            
        numero_inst = int(list_mov.get_numero_dron(dron))
        if numero_inst != 0:
            num = numero_inst
            
        if altura_actual < int(altura):
            while altura_actual < altura_final:
                altura_actual += 1
                tiempo_actual += 1
                nuevo_movimiento = Movimientos("Subir", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
            tiempo_actual += 1
            bandera = list_mov.get_tiempo(tiempo_actual)
            if bandera:
                nuevo_movimiento = Movimientos("Esperar", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
                self.mover_dron(altura, dron, list_mov, tiempo_actual, indice)
            else :
                nuevo_movimiento = Movimientos("Emitir luz", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
        elif altura_actual > int(altura):
            while altura_actual > altura_final:
                tiempo_actual += 1
                nuevo_movimiento = Movimientos("Bajar", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
                altura_actual -= 1
            
            tiempo_actual += 1
            bandera = list_mov.get_tiempo(tiempo_actual)
            if bandera:
                nuevo_movimiento = Movimientos("Esperar", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
                self.mover_dron(altura, dron, list_mov, tiempo_actual, indice)
            else :
                nuevo_movimiento = Movimientos("Emitir luz", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
        elif altura_actual == int(altura):
            tiempo_actual += 1
            bandera = list_mov.get_tiempo(tiempo_actual)
            if bandera:
                nuevo_movimiento = Movimientos("Esperar", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
                self.mover_dron(altura, dron, list_mov, tiempo_actual, indice)
            else:
                nuevo_movimiento = Movimientos("Emitir luz", tiempo_actual, dron, altura, indice)
                list_mov.append_sorted(nuevo_movimiento)
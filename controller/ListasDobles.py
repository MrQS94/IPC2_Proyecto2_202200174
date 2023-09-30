from controller.Nodos import Nodo_regular, Nodo, Movimientos
from os import system
from xml.etree import ElementTree as ET
from xml.dom import minidom

class ListaDoble():
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.mensaje = ''
        
    def append(self, dron):
        nuevo_nodo = Nodo_regular(dron, None, None, None)
        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
        else:
            actual = self.head
            while actual.next:
                actual = actual.next
            actual.next = nuevo_nodo
            self.size += 1

    def append_inst(self, dron, altura):
        nuevo_nodo = Nodo_regular(dron, altura, None, None)
        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
        else:
            actual = self.head
            while actual.next:
                actual = actual.next
            actual.next = nuevo_nodo
            self.size += 1
    
    def append_mensaje(self, dron, altura, letra, instruccion):
        nuevo_nodo = Nodo_regular(dron, altura, letra, instruccion)
        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
        else:
            actual = self.head
            while actual.next:
                actual = actual.next
            actual.next = nuevo_nodo
            self.size += 1
            
    def update(self, dron, instruccion):
        actual = self.head
        while actual:
            if actual.dron == dron and int(actual.altura) == int(instruccion): 
                actual.instruccion = 'Emitir Luz'
                self.mensaje += actual.letra
            actual = actual.next
            
    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            dron, altura, letra, instruccion = self.actual.dron, self.actual.altura, self.actual.letra, self.actual.instruccion
            self.actual = self.actual.next
            return dron, letra, altura, instruccion
        else:
            raise StopIteration
    
    def graficar(self, nombre_mensaje, graph_body, sistema_drones, lista):
        graph_body += f"""
        <tr>
            <td rowspan="1000"> {sistema_drones} </td>
        </tr>
        """
        count_final_altura = self.get_size_altura_per_dron()
        dron_actual = ''
        graph_body += '<tr>\n'
        for dron, _, _, _ in lista:
            if dron != dron_actual:
                dron_actual = dron
                graph_body += f'<td> {dron} </td>\n'
        graph_body += '</tr>\n'
        
        actual = self.head
        count_altura = 1
        graph_table = ''
        is_label_tr = True
        while True:
            if is_label_tr:
                graph_table += '<tr>\n'
                is_label_tr = False
            if actual is None:
                actual = self.head
                graph_table += '</tr>\n'
                count_altura += 1  
                is_label_tr = True
                
            if count_altura == int(actual.altura):
                if actual.instruccion == 'Emitir Luz':
                    graph_table += f'<td bgcolor=\'pink\'> {actual.letra} </td>\n'
                else:
                    graph_table += f'<td> {actual.letra} </td>\n'
            if count_altura == count_final_altura + 1:
                break
            actual = actual.next
        graph_body += graph_table
        return graph_body
    
    def get_size_altura_per_dron(self):
        actual = self.head
        
        dron_altura = -1
        dron_actual = actual.dron
        
        while actual:
            dron_altura += 1
            if dron_actual != actual.dron:
                return dron_altura
            actual = actual.next
        
    def organizar_lista_drones(self):
        if not self.head:
            return
        
        sorted_head = None
        current = self.head
        while current:
            next_node = current.next
            if not sorted_head or current.dron < sorted_head.dron:
                current.next = sorted_head
                sorted_head = current
            else:
                prev = sorted_head
                while prev.next and prev.next.dron < current.dron:
                    prev = prev.next
                current.next = prev.next
                prev.next = current
            current = next_node
        self.head = sorted_head
    
    def get_size_altura(self):
        actual = self.head
        dron_actual = actual.dron
        
        contador = 0
        while actual:
            if actual.dron == dron_actual:
                contador += 1
            actual = actual.next
        return contador
    
    def get_size(self):
        return self.size
    
    def display(self):
        actual = self.head
        while actual:
            print(actual.dron, ' - ', actual.altura, end=" -> ")
            actual = actual.next
            
    def is_empty(self):
        return self.head is None or self.size == 0
        
    def is_found(self, dron):
        current = self.head
        while current:
            if current.dron == dron:
                return True
            current = current.next
        return False
    
    def clear(self):
        self.head = None
        self.size = 0
        

class ListaAlturas():
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, altura):
        nuevo_nodo = Nodo(tipo_dato = altura)
        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
            return
        actual = self.head
        while actual.next:
            actual = actual.next

        actual.next = nuevo_nodo
        self.size += 1

    def append_sorted(self, altura):
        nuevo_nodo = Nodo(tipo_dato = altura)
        if self.size == 0:
            self.head = nuevo_nodo
        else:
            actual = self.head
            anterior = None
            while actual is not None and (int(actual.tipo_dato.altura) < int(nuevo_nodo.tipo_dato.altura) or (int(actual.tipo_dato.altura) == int(nuevo_nodo.tipo_dato.altura) and int(actual.tipo_dato.num_contenido) < int(nuevo_nodo.tipo_dato.num_contenido))):
                anterior = actual
                actual = actual.next
            if anterior is None:
                nuevo_nodo.next = self.head
                self.head = nuevo_nodo
            else:
                nuevo_nodo.next = actual
                anterior.next = nuevo_nodo
        self.size += 1

    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.tipo_dato
            self.actual = self.actual.next
            return valor_actual
        else:
            raise StopIteration
    
    def get_alturas(self, dron_buscado):
        actual = self.head

        while actual is not None:
            if actual.tipo_dato.dron == dron_buscado:
                return actual.tipo_dato
            actual = actual.next

        return None
    
    def display(self):
        print("TOTAL ALTURAS", self.size)
        print("")

        actual = self.head
        while actual is not None:
            print("Altura:", actual.tipo_dato.altura, "| Valor:", actual.tipo_dato.valor)
            actual = actual.next

class ListaSistemaDrones():
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, sistema_drones):
        nuevo_nodo = Nodo(tipo_dato = sistema_drones)
        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
            return
        actual = self.head
        while actual.next:
            actual = actual.next
        actual.next = nuevo_nodo
        self.size += 1
    
    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.tipo_dato
            self.actual = self.actual.next
            return valor_actual
        else:
            raise StopIteration
        
    def get_sistema(self, sistema):
        actual = self.head
        while actual is not None:
            if actual.tipo_dato.nombre == sistema:
                return actual.tipo_dato
            actual = actual.next
        return None
        
    def clear(self):
        while self.head is not None:
            actual = self.head
            self.head = self.head.next
            del actual
        self.size = 0
        print("-> Lista sistema eliminada...")
    
    def display(self):
        print("TOTAL SISTEMAS:", self.size)
        print("")

        actual = self.head
        while actual is not None:
            print("Nombre:", actual.tipo_dato.nombre, "| Altura maxima:", actual.tipo_dato.altura_max, "| Cantidad drones:", actual.tipo_dato.cantidad)
            print("------ Contenido ------")
            actual.tipo_dato.contenido.display()
            actual = actual.next

class ListaContenido():
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, contenido):
        nuevo_nodo = Nodo(tipo_dato = contenido)
        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
            return

        actual = self.head
        while actual.next:
            actual = actual.next
        actual.next = nuevo_nodo
        self.size += 1

    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.tipo_dato
            self.actual = self.actual.next
            return valor_actual
        else:
            raise StopIteration
        
    def get_contenido(self, dron_buscado):
        actual = self.head
        while actual is not None:
            if actual.tipo_dato.dron == dron_buscado:
                return actual.tipo_dato
            actual = actual.next
        return None
    
    def display(self):
        print("TOTAL CONTENIDOS:", self.size)
        print("")
        actual = self.head
        while actual is not None:
            print("Dron:", actual.tipo_dato.dron)
            print("------ Alturas ------")
            actual.tipo_dato.alturas.display()
            actual = actual.next

class ListaInstruccion():
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, instruccion):
        nuevo_nodo = Nodo(tipo_dato = instruccion)

        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
            return
        
        actual = self.head
        while actual.next:
            actual = actual.next

        actual.next = nuevo_nodo
        self.size += 1

    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.tipo_dato
            self.actual = self.actual.next
            return valor_actual
        else:
            raise StopIteration
        
    def display(self):
        print("TOTAL INSTRUCCIONES", self.size)
        print("")
        actual = self.head
        while actual is not None:
            print("Dron:", actual.tipo_dato.dron, "| Instruccion:", actual.tipo_dato.instruccion)
            actual = actual.next

class ListaMensaje():
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, mensaje):
        nuevo_nodo = Nodo(tipo_dato = mensaje)

        if self.size == 0:
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:
        
            actual = self.head
            anterior = None
            while actual is not None and actual.tipo_dato.nombre_msg.lower() < nuevo_nodo.tipo_dato.nombre_msg.lower():
                anterior = actual
                actual = actual.next
            if anterior is None:
                nuevo_nodo.next = self.head
                self.head = nuevo_nodo
            else:
                nuevo_nodo.next = actual
                anterior.next = nuevo_nodo
        self.size += 1

    def get_msg(self, msg):
        actual = self.head
        while actual is not None:
            if actual.tipo_dato.nombre_msg == msg:
                return actual.tipo_dato
            actual = actual.next
        return None

    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.tipo_dato
            self.actual = self.actual.next
            return valor_actual
        else:
            raise StopIteration

    def clear(self):
        while self.head is not None:
            actual = self.head
            self.head = self.head.next
            del actual
        self.size = 0
        print("-> Lista Mensajes eliminada...")
    
    def display(self):
        print("TOTAL Mensajes", self.size)
        print("")
        actual = self.head
        while actual is not None:
            print("Nombre:", actual.tipo_dato.nombre_msg, "| Sistema:", actual.tipo_dato.sistema)
            print("------- Instrucciones -------")
            actual.tipo_dato.instrucciones.display()
            actual = actual.next

class ListaMovimiento:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, movimiento):
        nuevo_nodo = Nodo(tipo_dato = movimiento)

        if self.head is None:
            self.head = nuevo_nodo
            self.size += 1
            return
        
        actual = self.head
        while actual.next:
            actual = actual.next

        actual.next = nuevo_nodo
        self.size += 1

    def append_sorted(self, movimiento):
        nuevo_nodo = Nodo(tipo_dato = movimiento)

        if self.size == 0:
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:
            actual = self.head
            anterior = None
            while actual is not None and (int(actual.tipo_dato.tiempo) < int(nuevo_nodo.tipo_dato.tiempo) or (int(actual.tipo_dato.tiempo) == int(nuevo_nodo.tipo_dato.tiempo) and int(actual.tipo_dato.num_instruccion) < int(nuevo_nodo.tipo_dato.num_instruccion))):
                anterior = actual
                actual = actual.next
            if anterior is None:
                nuevo_nodo.next = self.head
                self.head = nuevo_nodo
            else:
                nuevo_nodo.next = actual
                anterior.next = nuevo_nodo
        self.size += 1

    def get_indice_dron(self, dron_buscado, indice_):
        actual = self.head
        indice = indice_
        while actual is not None:
            if actual.tipo_dato.dron == dron_buscado:
                indice = actual.tipo_dato.num_instruccion
                return indice
            actual = actual.next
        return indice

    def get_movimientos_dron(self, dron_buscado):
        actual = self.head
        movimiento = 0
        while actual is not None:
            if actual.tipo_dato.dron == dron_buscado:
                movimiento = actual.tipo_dato.altura
            actual = actual.next
        return movimiento
    
    def get_tiempo_dron(self, dron_buscado):
        actual = self.head
        tiempo = 0
        while actual is not None:
            if actual.tipo_dato.dron == dron_buscado:
                tiempo = actual.tipo_dato.tiempo
            actual = actual.next
        return tiempo
    
    def get_numero_dron(self, dron_buscado):
        actual = self.head
        numero = 0
        while actual is not None:
            if actual.tipo_dato.dron == dron_buscado:
                numero = actual.tipo_dato.num_instruccion
            actual = actual.next
        return numero
    
    def get_numero_dron_head(self, dron_buscado):
        actual = self.head
        numero = 0
        while actual is not None:
            if actual.tipo_dato.dron == dron_buscado:
                numero = actual.tipo_dato.num_instruccion
                return numero
            actual = actual.next
        return 0
    
    def get_altura(self, altura):
        actual = self.head
        while actual is not None:
            if actual.tipo_dato.altura == altura:
                return True
            actual = actual.next
        return False
    
    def get_tiempo(self, tiempo):
        actual = self.head
        while actual is not None:
            if actual.tipo_dato.tiempo == tiempo and actual.tipo_dato.movimiento == "Emitir luz":
                return True
            actual = actual.next
        return False

    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.tipo_dato
            self.actual = self.actual.next
            return valor_actual
        else:
            raise StopIteration
        
    def get_mayor_tiempo(self):
        if not self.head:
            return None
        actual = self.head
        tiempo_max = actual.tipo_dato.tiempo
        while actual is not None:
            if actual.tipo_dato.tiempo > tiempo_max:
                tiempo_max = actual.tipo_dato.tiempo
            actual = actual.next
        return tiempo_max
    
    def valide_posicion(self, tiempo, dron_buscado):
        actual = self.head
        while actual:
            if actual.tipo_dato.tiempo == tiempo and actual.tipo_dato.dron == dron_buscado:
                return True
            actual = actual.next
        return False
    
    def complete_esperar(self, dron_buscar, altura, indice):
        tiempo = int(self.get_mayor_tiempo())

        for tiempos in range(1, tiempo+1):
            if self.valide_posicion(tiempos, dron_buscar) is False:
                nuevo_movimiento = Movimientos("Esperar", tiempos, dron_buscar,altura, indice)
                self.append_sorted(nuevo_movimiento)

    def display(self):
        print("TOTAL MOVIMIENTOS:", self.size)
        print("")
        actual = self.head
        while actual is not None:
            print("Tiempo:", actual.tipo_dato.tiempo, "| MOVIMIENTO:", actual.tipo_dato.movimiento, "\t| Dron:", actual.tipo_dato.dron, "| No. In:", actual.tipo_dato.num_instruccion)
            actual = actual.next

class ListaMsgProcess:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, mensaje_procesado):
        nuevo_nodo = Nodo(tipo_dato=mensaje_procesado)

        if self.size == 0:
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:

            actual = self.head
            anterior = None
            while actual is not None and actual.tipo_dato.nombre_mensaje.lower() < nuevo_nodo.tipo_dato.nombre_mensaje.lower():
                anterior = actual
                actual = actual.next
            if anterior is None:
                nuevo_nodo.next = self.head
                self.head = nuevo_nodo
            else:
                nuevo_nodo.next = actual
                anterior.next = nuevo_nodo

        self.size += 1

    def __iter__(self):
        self.actual = self.head
        return self

    def __next__(self):
        if self.actual is not None:
            valor_actual = self.actual.tipo_dato
            self.actual = self.actual.next
            return valor_actual
        else:
            raise StopIteration

    def obtener_size(self):
        return self.size

    def obtener_datos_msg(self, msg):
        actual = self.head

        while actual is not None:
            if actual.tipo_dato.nombre_mensaje == msg:
                return actual.tipo_dato
            actual = actual.next
            
    def clear(self):
        while self.head is not None:
            actual = self.head
            self.head = self.head.next
            del actual
        self.size = 0
        print("-> Lista mensajes procesados eliminada...")

    def mostrar_lista(self):
        print("TOTAL MENSAJES", self.size)
        print("")

        actual = self.head
        while actual is not None:
            print("Nombre:", actual.tipo_dato.nombre_mensaje, "| Sistema:", actual.tipo_dato.sistema, "| Mensaje:", actual.tipo_dato.mensaje)
            print("------- Instrucciones -------")
            actual.tipo_dato.movimientos.mostrar_lista()
            actual = actual.next
            
    def generar_xml(self, mensajes):
        respuesta = ET.Element('respuesta')      
        lista_mensajes = ET.SubElement(respuesta, 'listaMensajes')
        
        for msg in mensajes:
            msg_found = self.obtener_datos_msg(msg.nombre_mensaje)
            mensaje = ET.SubElement(lista_mensajes, 'mensaje', nombre=f'{msg.nombre_mensaje}')
            
            sistema = ET.SubElement(mensaje, 'sistemaDrones')
            sistema.text = msg.sistema
            
            tiempo_optimo = ET.SubElement(mensaje, 'tiempoOptimo')
            tiempo_optimo.text = str(msg_found.tiempo)
            
            mensaje_recibido = ET.SubElement(mensaje, 'mensajeRecibido')
            mensaje_recibido.text = msg_found.mensaje
            
            instrucciones = ET.SubElement(mensaje, 'instrucciones')
            
            for i in range(1, int(msg_found.tiempo) + 1):
                tiempo = ET.SubElement(instrucciones, 'tiempo', valor=f'{i}')
                acciones = ET.SubElement(tiempo, 'acciones')
                for mov in msg_found.movimientos:
                    if i == int(mov.tiempo):
                        dron = ET.SubElement(acciones, 'dron', nombre=f'{mov.dron}')
                        dron.text = mov.movimiento
            
        pretty = self.prettify_xml(respuesta)
        with open("202200174_salida.xml", "w", encoding='UTF-8') as file:
            file.write(pretty)
    
    def prettify_xml(self, elem):
        rough_string = ET.tostring(elem, "UTF-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
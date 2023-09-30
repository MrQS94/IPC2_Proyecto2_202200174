class Nodo_regular():
    def __init__(self, dron, altura, letra, instruccion):
        self.dron = dron
        self.altura = altura
        self.letra = letra
        self.instruccion = instruccion
        self.next = None
        self.back = None
        
class Nodo:
    def __init__(self, tipo_dato = None):
        self.tipo_dato = tipo_dato
        self.next = None

class Mensaje:
    def __init__(self, nombre_msg, sistema, instrucciones):
        self.nombre_msg = nombre_msg
        self.sistema = sistema
        self.instrucciones = instrucciones

class MensajeProcesado():
    def __init__(self, nombre_mensaje, mensaje, sistema, tiempo, movimientos):
        self.nombre_mensaje = nombre_mensaje
        self.mensaje = mensaje
        self.sistema = sistema
        self.tiempo = tiempo
        self.movimientos = movimientos

class Altura:
    def __init__(self, altura, valor, dron, num_contenido):
        self.altura = altura
        self.valor = valor
        self.dron = dron
        self.num_contenido = num_contenido

class Instruccion:
    def __init__(self, dron, instruccion):
        self.dron = dron
        self.instruccion = instruccion

class Contenido:
    def __init__(self, dron, alturas):
        self.dron = dron
        self.alturas = alturas

class SistemaDrones:
    def __init__(self, nombre, altura_max, cantidad, contenido):
        self.nombre = nombre
        self.altura_max = altura_max
        self.cantidad = cantidad
        self.contenido = contenido

class Movimientos:
    def __init__(self, movimiento, tiempo, dron, altura, num_instruccion):
        self.movimiento = movimiento
        self.tiempo = tiempo
        self.dron = dron
        self.altura = altura
        self.num_instruccion = num_instruccion
        
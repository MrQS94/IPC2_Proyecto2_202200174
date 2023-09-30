import sys
import os

ruta_actual = os.path.dirname(__file__)
ruta_proyecto = os.path.abspath(os.path.join(ruta_actual, '..'))
if ruta_proyecto not in sys.path:
    sys.path.append(ruta_proyecto)

from controller.Interfaz import Interfaz

control_interfaz = Interfaz()

if __name__ == '__main__':
    control_interfaz.cargar_frame()
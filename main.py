#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   PL_Proyecto1 - main
#   Nayeli Gissel Larios Pérez

from objetoSeguro import ObjetoSeguro

if __name__ == '__main__':
    print("CREACION DE OBJETO SEGURO")
    nombre = input("Nombre del objeto : ")
    mi_puerto = int(input("Mi puerto : "))
    puerto_destino = int(input("Puerto destino : "))
    Mensajero = ObjetoSeguro(nombre, mi_puerto, puerto_destino)
    Mensajero.espera_conexion()
    Mensajero.inicia_comunicacion()
    Mensajero.termina_comunicacion()


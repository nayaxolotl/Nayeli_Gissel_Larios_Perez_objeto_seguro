#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   PL_Proyecto1 - main
#   Nayeli Gissel Larios Pérez

from objetoSeguro import ObjetoSeguro

if __name__ == '__main__':
    Obj1 = ObjetoSeguro("Obj1")
    Obj2 = ObjetoSeguro("Obj2")
    Obj2.saludar(Obj2.nombre,Obj2.cifrar_msj(Obj1.llave_publica(), "Hola Mundo"))
    Obj2.almacenar_msj("Hola mundo")
    Obj2.almacenar_msj("Segundo mensaje")
    Obj2.almacenar_msj("Tercer mensaje")
    Obj2.consultar_msj(0)
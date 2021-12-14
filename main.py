#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   PL_Proyecto1 - main
#   Nayeli Gissel Larios Pérez

from objetoSeguro import ObjetoSeguro

if __name__ == '__main__':
    # Se instancia el Obj1
    print("CREACION DE OBJETO SEGURO")
    nombre = input("Nombre del objeto : ")
    mi_puerto = int(input("Mi puerto : "))
    puerto_destino = int(input("Puerto destino : "))
    Mensajero = ObjetoSeguro(nombre, mi_puerto, puerto_destino)
    Mensajero.espera_conexion()
    


# Comunicacion Obj2 -> Obj1
#    print("Mensaje de Obj2 -> Obj1 = ")
#    mensaje1 = input()
# Obj2 pide la llave publica de Obj1 para comunicarse con el
#    llavepublicaObj1 = Obj1.llave_publica()
# Obj2 cifra el mensaje que quiere enviar a Obj1 con su llave publica (Obj1)
#    mensaje_cifrado = Obj2.cifrar_msj(llavepublicaObj1,mensaje1)
# "Hola Objeto1 soy Objeto2")
# Obj2 envia un saludo a Obj1 y Obj1
#    Obj1.saludar(Obj2.nombre, mensaje_cifrado)


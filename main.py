#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   PL_Proyecto1 - main
#   Nayeli Gissel Larios Pérez

from objetoSeguro import ObjetoSeguro

if __name__ == '__main__':
    # Se instancia el Obj1
    Obj1 = ObjetoSeguro("Obj1")
    # Se instancia el Obj2
    Obj2 = ObjetoSeguro("Obj2")

# Comunicacion Obj2 -> Obj1
    print("Mensaje de Obj2 -> Obj1 = ")
    mensaje1 = input()
    # Obj2 pide la llave publica de Obj1 para comunicarse con el
    llavepublicaObj1 = Obj1.llave_publica()
    # Obj2 cifra el mensaje que quiere enviar a Obj1 con su llave publica (Obj1)
    mensaje_cifrado = Obj2.cifrar_msj(llavepublicaObj1,mensaje1)
                                      # "Hola Objeto1 soy Objeto2")
    # Obj2 envia un saludo a Obj1 y Obj1
    Obj1.saludar(Obj2.nombre, mensaje_cifrado)

    print("Mensaje de Obj1 -> Obj2 = ")
    mensaje2 = input()
# Comunicacion Obj1 -> Obj2
    # Obj1 pide la llave publica de Obj2 para comunicarse con el
    llavepublicaObj2 = Obj2.llave_publica()
    # Obj1 cifra el mensaje que quiere enviar a Obj2 con su llave publica (Obj2)
    mensaje_cifrado = Obj1.cifrar_msj(llavepublicaObj2, mensaje2)
    # Obj2 envia un saludo a Obj1 y Obj1
    Obj2.saludar(Obj1.nombre, mensaje_cifrado)

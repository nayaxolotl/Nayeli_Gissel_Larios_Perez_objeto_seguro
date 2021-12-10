#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   PL_Proyecto1 - Objeto seguro
#   Nayeli Gissel Larios Pérez

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import logging

logging.basicConfig(format='DEBUG : %(message)s', level=logging.DEBUG)

KEY_SIZE = 32  # Para AES-256


# Clase ObjetoSeguro
class ObjetoSeguro:
    def __init__(self, nombre: str):
        # Atributos de la clase ObjetoSeguro
        self.nombre = nombre
        self.llavePublica, self.__llavePrivada = self.__gen_llaves()
        self.__conteoMensajes = 0
        self.__mensajeRecibido = ""

    # Métodos del ObjetoSeguro
    # Metodo privado que, al instanciar el objeto genera la llave publica y privada
    @staticmethod
    def __gen_llaves():
        secreto = RSA.generate(1024)
        privada = secreto.exportKey()
        publica = secreto.publickey().exportKey()
        return publica, privada

    # Metodo privado que codifica el str ascii ingresado a byte de base64
    @staticmethod
    def __codificar64(msj: str) -> bytes:
        aux = base64.b64encode(msj.encode('ascii'))
        return aux

    # Metodo privado que decodifica byte de base64 a string ascii
    @staticmethod
    def __decodificar64(msj: bytes) -> str:
        aux = base64.b64decode(msj)
        return aux.decode("ascii")

    # Metodo privado que almacena un mensaje recibido en un archivo de texto
    def __almacenar_msj(self, msj: str) -> dict:
        aux = dict(
            ID=self.conteoMensajes,
            MSJ=msj
        )
        self.conteoMensajes += 1
        logging.debug("{}".format(aux))
        archivo = open(f"RegistoMsj_{self.nombre}.txt", "a")
        with archivo as f:
            print(f"ID: {aux['ID']}, MSJ: {aux['MSJ']}", file=f)
        archivo.close()
        return aux

    # Metodo privado que almacena un mensaje recibido en un archivo de texto
    @staticmethod
    def __consultar_msj(id: int) -> dict:
        archivo = open("RegistoMsj_{self.nombre}.txt", "r")
        with archivo as f:
            for texto in f:
                linea = texto.split(",", maxsplit=1)
                extrae_id = linea[0].split(":")
                extrae_txt = linea[1].split(":")
                if int(extrae_id[1]) == id:
                    print(f"ID {id}: {extrae_txt[1]}")
        aux = dict(
            ID=id,
            MSJ=extrae_txt[1]
        )
        return aux

    # Metodo publico que cifra un mensaje con una llave publica
    def cifrar_msj(self, pub_key: str, msj: str) -> bytes:
        llave_publica = RSA.importKey(pub_key)
        llave_publica = PKCS1_OAEP.new(llave_publica)
        texto_cifrado = llave_publica.encrypt(self.__codificar64(msj))
        return texto_cifrado

    # Metodo publico que descifra un mensaje con una llave publica
    def descifrar_msj(self, msj: bytes) -> bytes:
        llave_privada = RSA.importKey(self.__llavePrivada)
        llave_privada = PKCS1_OAEP.new(llave_privada)
        texto_descifrado = llave_privada.decrypt(msj)
        return texto_descifrado

    # Metodo publico con el que se obtiene la llave publica del objeto
    # No es string por que la biblioteca crea las llaves con otro formato
    def llave_publica(self):
        return self.llavePublica

    # Metodo publico que recibe un saludo con un mensaje cifrado
    def saludar(self, name: str, msj: str):
        self.mensajeRecibido = msj
        print(f"Hola soy {name} y me quiero comunicar contigo")
        # print(f"Te envio el mensaje cifrado: {msj}")
        self.esperar_respuesta(self.responder(name))
        return

    # Metodo publico que procesa una respuesta a un saludo recibido
    def responder(self, msj: str) -> bytes:
        print(f"Hola {msj} recibi tu mensaje")
        mensaje_respuesta = self.__codificar64("MensajeRespuesta")
        return mensaje_respuesta + self.mensajeRecibido

    def esperar_respuesta(self, msj: bytes):
        print("Procesando una respuesta")
        mensaje_respuesta = self.__codificar64("MensajeRespuesta")
        mensaje_codificado = msj.lstrip(mensaje_respuesta)
        # print(self.decodificar64(self.descifrar_msj(mensaje_codificado)))
        self.__almacenar_msj(self.__decodificar64(self.descifrar_msj(mensaje_codificado)))
        return
    
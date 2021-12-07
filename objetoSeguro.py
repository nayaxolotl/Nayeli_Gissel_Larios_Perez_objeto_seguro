#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   PL_Proyecto1 - Objeto seguro
#   Nayeli Gissel Larios Pérez

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import logging

logging.basicConfig(format='DEBUG : %(message)s',level=logging.DEBUG)

KEY_SIZE = 32  # Para AES-256

class ObjetoSeguro:
    def __init__(self, nombre: str):
        # Atributos de la clase ObjetoSeguro
        self.nombre = nombre
        self.llavePublica, self.llavePrivada = self.__gen_llaves()
        self.conteoMensajes = 0
        self.mensajeRecibido = ""

    # Métodos del ObjetoSeguro
    def __gen_llaves(self):
        secreto = RSA.generate(1024)
        privada = secreto.exportKey()
        publica = secreto.publickey().exportKey()
        return publica, privada

    def __codificar64(self, msj: str) -> bytes:
        aux = base64.b64encode(msj.encode('ascii'))
        return aux

    def __decodificar64(self, msj: bytes) -> str:
        aux = base64.b64decode(msj)
        return aux.decode("ascii")

    def cifrar_msj(self, pub_key: str, msj: str) -> bytes:
        llavePublica = RSA.importKey(pub_key)
        llavePublica =PKCS1_OAEP.new(llavePublica)
        textoCifrado = llavePublica.encrypt(self.__codificar64(msj))
        return textoCifrado

    def descifrar_msj(self, msj: bytes) -> bytes:
        llavePrivada = RSA.importKey(self.llavePrivada)
        llavePrivada = PKCS1_OAEP.new(llavePrivada)
        textoDescifrado = self.__decodificar64(llavePrivada.decrypt(msj))
        return textoDescifrado

    def llave_publica(self) -> str:
        return self.llavePublica

    def saludar(self, name: str, msj: str):
        self.mensajeRecibido = msj
        print(f"Hola soy {name} y me quiero comunicar contigo")
        print(f"Te envio el mensaje cifrado: {msj}")
        self.responder(name)
        return

    def responder(self, msj: str) -> bytes:
        print((f"Hola {msj} recibi tu mensaje"))
        aux = self.mensajeRecibido + self.__codificar64("MensajeRespuesta")
        return aux

    def almacenar_msj(self, msj: str) -> dict:
        aux = dict(
            ID = self.conteoMensajes,
            MSJ = msj
        )
        self.conteoMensajes += 1
        logging.debug("{}".format(aux))
        archivo = open("MensajesRecibidos.txt","a")
        with archivo as f:
            print(f"ID: {aux['ID']}, MSJ: {aux['MSJ']}", file=f)
        archivo.close()
        return

    def consultar_msj(self, id: int) -> dict:
        a = 0
        archivo = open("MensajesRecibidos.txt","r")
        with archivo as f:
            for texto in f:
                linea = texto.split(",")
                extraeID = linea[0].split(":")
                extraeTXT = linea[1].split(":")
                if int(extraeID[1]) == id:
                    print(f"ID {id}: {extraeTXT[1]}")
        return

    def esperar_respuesta(self, msj: bytes):
        print("Recibi una respuesta")
        self.almacenar_msj(self.__decodificar64(self.descifrar_msj(msj)))
        return
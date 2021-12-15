#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   PL_Proyecto1 - Objeto seguro
#   Nayeli Gissel Larios Pérez

from concurrent.futures import ThreadPoolExecutor
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import logging
from socket_cliente import SocketClient
from socket_servidor import SocketServer

logging.basicConfig(format='\tDEBUG : %(message)s', level=logging.DEBUG)

KEY_SIZE = 32  # Para AES-256


# Clase ObjetoSeguro
class ObjetoSeguro:
    def __init__(self, nombre: str, puerto_servidor: int, puerto_cliente: int):
        # Atributos de la clase ObjetoSeguro
        logging.debug("OBJETO : {}".format(nombre))
        self.nombre = nombre
        self.llavePublica, self.__llavePrivada = self.__gen_llaves()
        self.__conteoMensajes = 0
        self.__mensajeRecibido = ""
        self.socketcliente = SocketClient(puerto_cliente)
        self.socketservidor = SocketServer(nombre, puerto_servidor)
        self.comunicacion = ThreadPoolExecutor(max_workers=3)
        self.llavePublicaReceptor = bytearray()
        self.write = None
        self.read = None
        self.captura = None

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
        aux = base64.b64encode(msj.encode("ascii"))
        return aux

    # Metodo privado que decodifica byte de base64 a string ascii
    @staticmethod
    def __decodificar64(msj: bytes) -> str:
        aux = base64.b64decode(msj)
        return aux.decode("ascii")

    # Metodo privado que almacena un mensaje recibido en un archivo de texto
    @staticmethod
    def __consultar_msj(identificador: int) -> dict:
        archivo = open("RegistoMsj_{self.nombre}.txt", "r")
        with archivo as f:
            for texto in f:
                linea = texto.split(",", maxsplit=1)
                extrae_id = linea[0].split(":")
                extrae_txt = linea[1].split(":")
                if int(extrae_id[1]) == id:
                    print(f"ID {identificador}: {extrae_txt[1]}")
        aux = dict(
            ID=id,
            MSJ=extrae_txt[1]
        )
        return aux

    # Metodo publico que cifra un mensaje con una llave publica
    def cifrar_msj(self, pub_key, msj: str) -> bytes:
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
        return str(self.llavePublica)

    def esperar_respuesta(self):
        print("Procesando una respuesta")
        # mensaje_respuesta = self.__codificar64("MensajeRespuesta")
        # mensaje_codificado = msj.rstrip(mensaje_respuesta)
        # print(self.decodificar64(self.descifrar_msj(mensaje_codificado)))
        # self.__almacenar_msj(self.__decodificar64(self.descifrar_msj(mensaje_codificado)))
        return

    def espera_conexion(self):
        inicializa = self.socketservidor.inicializa_socket()
        conectar = self.socketcliente.connect()
        while not conectar.done() and not inicializa.done():
            pass
        logging.debug("OBJETO : Conexion completa")

    def inicia_comunicacion(self):
        self.write = self.comunicacion.submit(self.socketcliente.write)
        self.read = self.comunicacion.submit(self.socketservidor.read)
        self.intercambia_llaves()
        logging.debug("OBJETO : ---------------inicia conexion segura---------------")
        self.captura = self.comunicacion.submit(self.captura_mensaje)

    def intercambia_llaves(self):
        aux = 1
        self.socketcliente.write_text(self.llave_publica())
        while aux:
            if '-BEGIN PUBLIC KEY-' in self.socketservidor.ultimo_mensaje:
                logging.debug("OBJETO : Llave recibida!")
                self.llavePublicaReceptor = self.socketservidor.ultimo_mensaje
                aux = 0

    # Metodo para capturar mensaje de la terminal
    def captura_mensaje(self):
        while True:
            mensaje = input()
            # llave2 = str.encode(self.llavePublicaReceptor)
            # mensaje_cifrado = self.cifrar_msj(llave, mensaje)
            # self.socketcliente.write_text(mensaje_cifrado)
            self.socketcliente.write_text(mensaje)

    def termina_comunicacion(self):
        while not self.write.done(): # and not self.write.done():
            pass
        self.read.cancel()
        self.captura.cancel()
        self.socketcliente.close()
        self.socketservidor.close()

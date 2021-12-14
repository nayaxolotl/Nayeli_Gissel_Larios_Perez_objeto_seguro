#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   Proyecto final - socket_cliente
#   Nayeli Gissel Larios Pérez
from concurrent.futures import ThreadPoolExecutor
from objetoSeguro import ObjetoSeguro
import logging
import socket

logging.basicConfig(format='DEBUG : %(message)s',
                    level=logging.DEBUG)


class SocketClient:
    def __init__(self, id_cliente: str):
        # atributos de la clase SocketClient
        # Crea el socket de comunicacion de tipo stream
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se especifica la ip y el puerto de conexion
        self.port_and_ip = ('127.0.0.1', 12345)
        # Administrador de threads un hilo para recepcion y otro para transmision
        self.tpe_comunicacion = ThreadPoolExecutor(max_workers=3)
        # Atributo donde se almacena la respuesta
        self.resp = ""
        self.mensaje_seguro = ObjetoSeguro("c"+id_cliente)
        self.llavePublicaReceptor = bytearray()
        logging.debug(">CLIENTE socket creado")

    def connect(self):
        # Conecta el socket a la direccion especificada
        try:
            self.node.connect(self.port_and_ip)
        except ConnectionRefusedError:
            logging.debug(">CLIENTE socket servidor en {} no esta activo".format(self.port_and_ip[0]))
        logging.debug(">CLIENTE socket conectado a {} puerto {}".format(self.port_and_ip[0], self.port_and_ip[1]))

    # Metodo que cierra el socket
    def close(self):
        self.node.shutdown(socket.SHUT_RDWR)
        self.node.close()
        logging.debug(">CLIENTE socket cerrado")

    # Metodo que envia el mensaje por el socket
    def send_sms(self, sms):
        self.node.send(sms.encode())
        self.resp = ""

    # Metodo que procesa la informacion que se va a mandar
    def write(self):
        while self.resp != "exit":
            if self.resp == "":
                pass
            else:
                aux = self.mensaje_seguro.nombre + ":" + self.resp
                logging.debug(">>{}".format(aux))
                self.send_sms(aux)

    # Metodo que procesa los datos que se reciben por el socket
    def read(self):
        message = ""
        while message == "":
            # Se indica que recibira mensajes de tamano
            message = self.node.recv(20).decode()
            if message != "":
                logging.debug("<<{}".format(message))
                extrae = message.split(":")
                if extrae[1] != "exit":
                    message = ""

    # Metodo para capturar mensaje de la terminal
    def captura_mensaje(self):
        while True:
            self.resp = input()

    # Metodo que ejecuta los hilos de comunicacion
    def comunicacion(self):
        write = self.tpe_comunicacion.submit(self.write)
        read = self.tpe_comunicacion.submit(self.read)
        self.saludo()
        self.habilita_terminal()
        while not write.done() and not read.done():
            pass
        self.close()

    def habilita_terminal(self):
        self.tpe_comunicacion.submit(self.captura_mensaje)

    def saludo(self):
        self.resp = "Hola"

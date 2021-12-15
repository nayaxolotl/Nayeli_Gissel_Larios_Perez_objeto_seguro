#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   Proyecto final - socket_cliente
#   Nayeli Gissel Larios Pérez
from concurrent.futures import ThreadPoolExecutor
import logging
import socket

LOCAL_HOST = '127.0.0.1'
logging.basicConfig(format='\tDEBUG : %(message)s',
                    level=logging.DEBUG)


class SocketClient:
    def __init__(self, puerto: int):
        # atributos de la clase SocketClient
        # Crea el socket de comunicacion de tipo stream
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se especifica la ip y el puerto de conexion
        self.port_and_ip = ('127.0.0.1', puerto)
        # Administrador de threads un hilo para recepcion y otro para transmision
        self.tpe_comunicacion = ThreadPoolExecutor(max_workers=4)
        # Atributo donde se almacena la respuesta
        self.resp = ""
        logging.debug("CLIENTE : socket creado {}".format(self.port_and_ip))

    # Metodo que buscara servidor al que se quiere conectar hasta encontrarlo
    def busca_servidor(self):
        while True:
            try:
                self.node.connect(self.port_and_ip)
                break
            except ConnectionRefusedError:
                pass
        logging.debug("CLIENTE : conectado a {}".format(self.port_and_ip))

    def connect(self):
        # Conecta el socket a la direccion especificada
        return self.tpe_comunicacion.submit(self.busca_servidor)

    # Metodo que cierra el socket
    def close(self):
        self.node.shutdown(socket.SHUT_RDWR)
        self.node.close()
        logging.debug("CLIENTE : socket cerrado")

    # Metodo que envia el mensaje por el socket
    def send_sms(self, sms):
        self.node.send(sms.encode())
        if sms != "exit":
            self.resp = ""

    # Metodo que procesa la informacion que se va a mandar
    def write(self):
        while self.resp != "exit":
            if self.resp == "":
                pass
            else:
                aux = self.resp
                self.send_sms(aux)

    # Metodo que recibe un texto a enviar desde le programa
    def write_text(self, texto):
        self.resp = texto

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

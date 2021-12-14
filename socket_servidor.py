#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   Proyecto final - socket_servidor
#   Nayeli Gissel Larios Pérez
from concurrent.futures import ThreadPoolExecutor
from objetoSeguro import ObjetoSeguro
import logging
import socket

logging.basicConfig(format='DEBUG : %(message)s',
                    level=logging.DEBUG)


class SocketServer:
    def __init__(self, id_servidor: str):
        # atributos de la clase SocketServer
        # Crea el socket de comunicacion de tipo stream
        self.connection = None
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se especifica la ip y el puerto de conexion
        self.port_and_ip = ('127.0.0.1', 12345)
        # Administrador de threads un hilo para recepcion y otro para transmision
        self.tpe_comunicacion = ThreadPoolExecutor(max_workers=2)
        # Atributo donde se almacena la respuesta
        self.resp = ""
        self.mensaje_seguro = ObjetoSeguro("s"+id_servidor)
        self.llavePublicaReceptor = bytearray()
        logging.debug(">SERVIDOR socket creado")

    def bind(self):
        # El socket solo se puede ver desde la misma maquina
        self.node.bind(self.port_and_ip)

    def listen(self):
        # Se especifica cuantas solictudes max se pondran en la cola
        self.node.listen(5)

    def accept(self):
        # Acepta conexiones
        self.connection, addr = self.node.accept()
        logging.debug(">SERVIDOR acepta conexion : {} puerto {}".format(addr[0], addr[1]))

    # Metodo que cierra el socket
    def close(self):
        self.node.shutdown(socket.SHUT_RDWR)
        self.node.close()
        logging.debug(">SERVIDOR socket cerrado")

    # Metodo que envia el mensaje por el socket
    def send_sms(self, sms):
        self.connection.send(sms.encode())

    # Metodo que procesa la informacion que se va a mandar
    def write(self):
        while self.resp != "exit":
            if self.resp == "":
                pass
            else:
                aux = self.mensaje_seguro.nombre + ":" + self.resp
                logging.debug("<<{}".format(aux))
                self.send_sms(aux)
                self.resp = ""
        self.send_sms(self.mensaje_seguro.nombre + ":exit")

    # Metodo que procesa los datos que se reciben por el socket
    def read(self):
        msg = ""
        extrae = ["", ""]
        while extrae[1] != "exit":
            # Se indica que recibira mensajes de tamano 20
            msg = self.connection.recv(20).decode()
            logging.debug(">>{}".format(msg))
            extrae = msg.split(":")
            self.resp = str("ok")
        self.resp = str("exit")

    # Metodo que llama a los metodos necesarios para iniciar una conexion
    def inicializa_socket(self):
        self.bind()
        self.listen()
        self.accept()

    # Metodo que ejecuta los hilos de comunicacion
    def comunicacion(self):
        write = self.tpe_comunicacion.submit(self.write)
        read = self.tpe_comunicacion.submit(self.read)
        self.saludo()
        while not write.done() and not read.done():
            pass
        self.close()

    def saludo(self):

        pass


#   Desarrollo de talento especializado 2021-2: Ciberseguridad
#   Python y Linux
#   Proyecto final - socket_servidor
#   Nayeli Gissel Larios Pérez
from concurrent.futures import ThreadPoolExecutor
import logging
import socket

LOCAL_HOST = '127.0.0.1'
logging.basicConfig(format='\tDEBUG : %(message)s',
                    level=logging.DEBUG)


class SocketServer:
    def __init__(self, puerto: int):
        # atributos de la clase SocketServer
        # Crea el socket de comunicacion de tipo stream
        self.connection = None
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se especifica la ip y el puerto de conexion
        self.port_and_ip = (LOCAL_HOST, puerto)
        # Administrador de threads un hilo para recepcion y otro para transmision
        self.tpe_comunicacion = ThreadPoolExecutor(max_workers=3)
        # Atributo donde se almacena la respuesta
        self.resp = ""
        logging.debug("SERVIDOR : socket creado {}".format(self.port_and_ip))

    def bind(self):
        # El socket solo se puede ver desde la misma maquina
        self.node.bind(self.port_and_ip)

    def listen(self):
        # Se especifica cuantas solictudes max se pondran en la cola
        self.node.listen(5)

    def accept(self):
        # Acepta conexiones
        self.connection, addr = self.node.accept()
        logging.debug("SERVIDOR : acepta conexion -> {}".format(addr))

    # Metodo que cierra el socket
    def close(self):
        self.node.shutdown(socket.SHUT_RDWR)
        self.node.close()
        logging.debug("SERVIDOR : socket cerrado")

    # Metodo que envia el mensaje por el socket
    def send_sms(self, sms):
        self.connection.send(sms.encode())

    # Metodo que procesa la informacion que se va a mandar
    def write(self):
        while self.resp != "exit":
            if self.resp == "":
                pass
            else:
                aux = ":" + self.resp
                logging.debug("<<{}".format(aux))
                self.send_sms(aux)
                self.resp = ""
        self.send_sms(":exit")

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
        return self.tpe_comunicacion.submit(self.accept)

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

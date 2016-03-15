
import serial
from serial.tools import list_ports
import threading
import Queue
import logging

PARITY_DICT = {'None': serial.PARITY_NONE, 'Even': serial.PARITY_EVEN,
               'Odd': serial.PARITY_ODD, 'Mask': serial.PARITY_MARK,
               'Space': serial.PARITY_SPACE}

def get_ports():
    ports = []
    for comport in list_ports.comports():
        port = comport[0]
        if (port.startswith('/dev/ttyACM') or port.startswith('/dev/ttyUSB') or
                port.startswith('COM') or
                port.startswith('/dev/cu.')):
            ports.append(port)

    return ports

class Serial(object):

    def __init__(self, on_received, on_failed):
        self.notify = on_received
        self.warn = on_failed

        self.tx_queue = Queue.Queue()
        self.rx_queue = Queue.Queue()
        self.serial = None
        self.tx_thread = None
        self.rx_thread = None

        self.stop_event = threading.Event()

    def start(self, port, baud, bytesize, stopbits, parity):
        if self.serial:
            self.serial.close()

        try:
            self.serial = serial.Serial(port=port,
                                        baudrate=baud,
                                        bytesize=bytesize,
                                        stopbits=stopbits,
                                        parity=PARITY_DICT[parity],
                                        timeout=0.2)
            self.tx_queue.queue.clear()
            self.rx_queue.queue.clear()
            self.stop_event.set()
            self.tx_thread = threading.Thread(target=self._send)
            self.rx_thread = threading.Thread(target=self._recv)
            self.stop_event.clear()
            self.tx_thread.start()
            self.rx_thread.start()

        except IOError as e:
            logging.warning(e)
            self.warn()

    def join(self):
        self.stop_event.set()
        if self.tx_thread:
            self.tx_thread.join()
            self.rx_thread.join()

        if self.serial:
            self.serial.close()

    def write(self, data):
        self.tx_queue.put(data)

    def read(self):
        return self.rx_queue.get()

    def _send(self):
        logging.info('tx thread is started')
        while not self.stop_event.is_set():
            try:
                data = self.tx_queue.get(True, 1)
                logging.info('tx:' + data)
                self.serial.write(data)
            except Queue.Empty:
                continue
            except IOError as e:
                logging.warning(e)
                self.serial.close()
                self.stop_event.set()
                self.warn()

        logging.info('tx thread exits')

    def _recv(self):
        logging.info('rx thread is started')
        while not self.stop_event.is_set():
            try:
                data = self.serial.read(1024)

                if data and len(data) > 0:
                    logging.info('rx:' + data)
                    self.rx_queue.put(data)
                    if self.notify:
                        self.notify()
            except IOError as e:
                logging.warning(e)
                self.serial.close()
                self.stop_event.set()
                self.warn()

        logging.info('rx thread exits')

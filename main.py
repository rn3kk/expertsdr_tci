import collections
import signal
import threading
import time
from threading import Thread

import rel

import websocket
from websocket import create_connection

CMD_START = 'START;'
CMD_STOP = 'STOP;'
CMD_FREQ = 'VFO:1,A;'
CMD_MUTE = 'MUTE;'
CMD_VFO_LIMITS = 'VFO_LIMITS:10000,30000000;'
CMD_CW = 'cw_msg:RA6LH;'
CMD_DDS_READ = 'DDS:1;'
CMD_DDS_WRITE = 'DDS:1,{};'
CMD_VFO_WRITE = 'VFO:0,0,{};'


class TCI_Connection(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.__rel = None
        self.__ws = None
        self.__terminate = False
        self.__queue = collections.deque(maxlen=5)
        self.__mutex = threading.Lock()

    def run(self) -> None:
        self.__ws = websocket.WebSocket()

        while not self.__terminate:
            try:
                if not self.__ws.connected:
                    self.__ws.connect('ws://127.0.0.1:50001')
                    self.__ws.settimeout(0.1)

                if len(self.__queue) > 0:
                    self.__mutex.acquire()
                    self.__ws.send(self.__queue.popleft())
                    self.__mutex.release()
                self.__ws.recv()
            except Exception as e:
                print(e)
            time.sleep(0.01)
        self.__ws.close()
        print('WS End loop')

    def set_terminate(self):
        self.__terminate = True

    def set_freq(self, freq):
        if not self.__ws:
            return
        s = str(CMD_VFO_WRITE).format(freq)
        self.__mutex.acquire()
        self.__queue.append(s)
        self.__mutex.release()


terminate = False
tci = None


def handler(signum, frame):
    global tci, terminate
    terminate = True
    if tci:
        tci.set_terminate()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    tci = TCI_Connection()
    tci.start()
    freq = 7000000
    while not terminate:
        tci.set_freq(freq)
        print('freq {}'.format(freq))
        freq += 1
        time.sleep(0.5)

    tci.join()

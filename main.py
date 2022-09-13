import time

from websocket import create_connection

CMD_START = 'START;'
CMD_STOP = 'STOP;'
CMD_FREQ = 'VFO:1,A;'
CMD_MUTE = 'MUTE;'
CMD_VFO_LIMITS = 'VFO_LIMITS:10000,30000000;'
CMD_CW = 'cw_msg:RA6LH;'
CMD_DDS_READ = 'DDS:1;'
CMD_DDS_WRITE = 'DDS:0,{};'

if __name__ == "__main__":
    ws = create_connection("ws://127.0.0.1:50001")
    d = b'1'
    freq = 7000000
    while d != b'':
        freq += 1
        s = CMD_DDS_WRITE.format(freq)
        ws.send(s)
        print(ws.recv())
        time.sleep(0.05)





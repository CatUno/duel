import socket
import time
import struct
from threading import Thread

NUM_BULLETS = 3
ENEMY_MSG_FORMAT = '>HHHH'

def runProc(num, enemySender):
    enemySender.run()

class EnemySender:
    task = 0
    def __init__(self, ip, port, dstPort, enemys):
        print("EnemySender constructor")
        self.enemys = enemys
        self.ip = ip
        self.port = port
        self.dstPort = dstPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(30.0)

        self.sock.bind(('', port))
        self.task = Thread(target=runProc, args=(1, self))
        self.task.start()
        self.printCnt = 1000
        
    def __del__(self):
        print("EnemySender destructor")
        self.sock.close()
        self.task.join()


    def send(self, playerCoord, bullets):
        if len(bullets):
            message = struct.pack(ENEMY_MSG_FORMAT, 
                  playerCoord[0], playerCoord[1], bullets[0], bullets[1])
        else: 
            message = struct.pack(ENEMY_MSG_FORMAT, 
                  playerCoord[0], playerCoord[1], 0, 0)

        #print("EnemySender: " + str(message) + "==>")
        self.sock.sendto(message, ('255.255.255.255', self.dstPort))

    def run(self):
        '''data, addr = self.sock.recvfrom(256)
        print('client addr: ', addr)
        print('msg: ', data)'''

        while True:
            try:
                buffer, addr = self.sock.recvfrom(256)
                data = struct.unpack(ENEMY_MSG_FORMAT, buffer)
                self.printCnt -= 1
                if self.printCnt == 0:
                    print('msg: ', buffer)
                if len(self.enemys):
                    self.enemys[0].goTo(data[0], data[1])
            except:
                print('exception')
                break

'''
enemies = []
enemySender = EnemySender('localhost', 7070, 7071, enemies)

time.sleep(8)
'''

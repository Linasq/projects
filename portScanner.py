import socket
from threading import Thread
import time

# read all inputs we need
target = input('IPv4 of the target: ')
ports = input('Range of ports to scan \nfor example: 0-10\n').split('-')
whenOut = float(input('Set timeout: '))
threadsMAX = int(input('How many threads: '))

#function to check whether port alive or not
def isalive():
    for thread in threads:
        if thread.is_alive():
            return True
    return False

# function to scan ports
def scan(port, target, whenOut):
    # print(f'port {port}\ntarget {target}\ntimeout {whenOut}')
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(whenOut)
        sock.connect((target, port))
    except:
        return

    print(f'port {port} is opened')

threadsCTR = 0
threads = []

for port in range(int(ports[0]), int(ports[1])+1):
    if threadsCTR % threadsMAX == 0:
        while isalive():
            time.sleep(0.0001)
        
        threads.clear()

    thread = Thread(target=scan, args=[port, target, whenOut])
    threads.append(thread)
    thread.start()
    threadsCTR+=1

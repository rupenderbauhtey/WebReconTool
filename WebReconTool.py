import threading
from queue import Queue
import requests
import random
import sys
import socket
import time
from datetime import datetime


def port_scanner(host_name):
    
    print_lock = threading.Lock()
    
    #Defining target
    target = socket.gethostbyname(host_name) #Translating hostname to IPv4


    #Adding a banner
    print("--" * 50)
    print("Starting Scan")
    print("Scanning Target " +target)
    print("Time Started :" +str(datetime.now()))
    print("--" * 50)

    print("\nScanning for Open Ports....")
        
    def pscan(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            socket.setdefaulttimeout(2)
            result = s.connect_ex((target, port))
            with print_lock:
                if result == 0:
                    print("PORT {} IS OPEN".format(port))
            s.close()

        except KeyboardInterrupt:
            print("\n Exiting Program. ")
            sys.exit()

        except socket.gaierror:
            print("Hostname could not be resolved. ")
            sys.exit()
        
        except socket.error:
            print("Couldn't connect to server. ")
            sys.exit()

    def threader():
        while True:
            worker=q.get()
            pscan(worker)
            q.task_done()

    q= Queue()

    for x in range(50):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in range(1,1000):
        q.put(worker)

    q.join()



def brute_force(website, urlp):
    
    url=urlp
    wordlist="Common.txt"
    ext=".php"

    try:
        target = socket.gethostbyname(website) #Translating hostname to IPv4

    except socket.gaierror:
        print("Hostname could not be resolved. ")
        sys.exit()
        
    except socket.error:
        print("Couldn't connect to server. ")
        sys.exit()

    #Adding a banner
    print("\nLooking for Directories....")
    
    fo = open(wordlist,"r+")
    for i in range(1000):
        word = fo.readline(10).strip()
        surl = url+word+ext
            
        response = requests.get(surl)
        if (response.status_code == 200):
            print ("[+] Found :- ",surl)
        else:
            pass


def subdomain(website):
    
    #Adding a banner
    print("\nEnumerating Subdomains....")
    
    subdomains = []

    req = requests.get(f'https://crt.sh/?q={website}&output=json')

    if req.status_code != 200:
        print('[*] Information not available!')
        sys.exit(1)

    for (key,value) in enumerate(req.json()):
        subdomains.append(value['name_value'])

    subs = sorted(set(subdomains))

    for s in subs:
        print(f'[*] {s}\n')
    

if __name__ == '__main__':

    while True:
        
        print("*" * 50)
        print('\n Welcome to the Target Scanner ! \n')
        print("*" * 50)

        website= (input("Enter target Domain : "))
        url= (input("\nEnter target URL : "))
        #wordlist= (input("\nEnter brute force Wordlist : "))
        #extension= (input("\nEnter extension for Directory : "))

        port_scanner(website)
        brute_force(website, url)
        subdomain(website)
                
        print("--" *50)
        print("scan completed succesfully")
        print("Time Completed: " +str(datetime.now()))
        print("--" *50)

        print("\n")
        print("\nGood Bye ! \n")
        exit()

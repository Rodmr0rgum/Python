import scapy.all as scapy
import sys
import time


#Ingresamos la ip del router y la ip de la victima
router_ip = str(sys.argv[1])
target_ip = str(sys.argv[2])


#funcion para sacar la macaddress del router y la victima
def get_mac_address(ip_address):
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_layer = scapy.ARP(pdst=ip_address)
    get_mac_packet = broadcast/arp_layer
    answer = scapy.srp(get_mac_packet, timeout=2 , verbose=True)[0]
    return answer[0][1].hwsrc


target_mac= str(get_mac_address(target_ip))
router_mac= str(get_mac_address(router_ip))

print (router_mac)
print (target_mac)

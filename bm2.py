from scapy.all import *
from collections import defaultdict
import socket
from pprint import pprint
from operator import itemgetter




s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip=s.getsockname()[0]


#print(traffic)
# return human readable units given bytes
def human(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

# callback function to process each packet
# get total packets for each source->destination combo
def traffic_monitor_callbak(pkt):
    if IP in pkt:
        src = pkt.sprintf("%IP.src%")
        dst = pkt.sprintf("%IP.dst%")

        size = pkt.sprintf("%IP.len%")

        # initialize
        if (src, dst) not in traffic:
            traffic[(src, dst)] = 0

        else:
            traffic[(src, dst)] += int(size)

def writea(a,b,c,d,e):
    z= open('data.txt', 'a')
    z.write('-----%s: %s (%s) -> %s (%s)-----\n' % (a,b,c,d,e))
    z.close()

# def writecsv(a,b,c,d,e):
#     writer=csv.writer(open("data.csv","w"))
#     entries ="%s: %s (%s) -> %s (%s)\n" % (a,b,c,d,e).split("|");
#     writer.writerows(entries)
#     writer.close()

w = open('data.txt', 'w')
w.close()

while True:
    traffic = defaultdict(list)

    sniff(iface="wlp3s0", prn=traffic_monitor_callbak, store=0, timeout=1)

    # sort by total bytes, descending
    traffic_sorted = sorted(traffic.items(), key=itemgetter(1), reverse=True) 
    for x in range(len(traffic_sorted)):
        try:
            #print (traffic_sorted)
            src = traffic_sorted[x][0][0]
            dst = traffic_sorted[x][0][1]
            host_total = traffic_sorted[x][1]
            # get hostname from IP
            try:
                src_hostname = socket.gethostbyaddr(src)
            except:
                src_hostname = src

            try:    
                dst_hostname = socket.gethostbyaddr(dst)
            except:
                dst_hostname = dst

            if ((src_hostname==ip)or (dst_hostname==ip)):
                print ("%s: %s (%s) -> %s (%s)" % (human(host_total), src_hostname[0], src, dst_hostname[0], dst))
                writea(human(host_total), src_hostname[0], src, dst_hostname[0], dst)
        except:
            pass
    #print('reset')


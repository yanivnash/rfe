'''
Created on Jun 9, 2020

Using ECS Version 1.5
https://www.elastic.co/guide/en/ecs/current/ecs-client.html

'''
import socket
import json
import datetime
import configparser
from elasticsearch import Elasticsearch
from scapy.all import ARP, Ether, srp
from elasticsearch.helpers.actions import bulk
import time
import argparse
import os

def genereate_actions(data):
    for item in data:
        yield {
            "_index": "lanclient",
            "_source" : item
        }

def send_to_elastic(clients, filename, index_file):
    print('loading ElasticSearch...')
    config = configparser.ConfigParser()
    if not filename == None:
        config.read(filename)
    else:
        config.read('config.ini')    
    
    host = [config['DEFAULT']['hosts']]
    verify_cert = True if config['DEFAULT']['verify_certs'] == 'True' else False
    ssl_warn =  True if config['DEFAULT']['ssl_show_warn'] == 'True' else False
        
    es = Elasticsearch(
            host,
            verify_certs=verify_cert,
            ssl_show_warn=ssl_warn
        )  
    
    if not index_file == None:
        with open(index_file, 'r') as file:
            mapping = json.load(file)
        # ignore 400 already exists code
        es.indices.create(index="lanclient", body=mapping, ignore=400)
      
    bulk(es, genereate_actions(clients))
    print('Bulk Upload to ElasticSearch Complete')
    
def get_domain(clientname):
    # Default Google wifi Primary & Guest unless you switch them
    domain = 'unknown'
    if '192.168.86' in clientname:
        domain = 'primary'
    if '192.168.87' in clientname:
        domain = 'guest'
    return domain

def scan_network(filename, index, print_results=False, load_to_elastic=True):
    current_time = datetime.datetime.utcnow().isoformat()
    print("Starting at "+ current_time)
    print("scanning....")
        
    clientname = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
        if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
        s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
        socket.SOCK_DGRAM)]][0][1]]) if l][0][0])    
    target_ip = (clientname+"/24")
    domain = get_domain(clientname)
          
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    
    clients = []
    for sent, received in result:
        client = {'@timestamp': current_time,
                    'client' : {
                    'ip': received.psrc, 
                    'mac': received.hwsrc, 
                    'name': socket.getfqdn(received.psrc),
                    'domain' : domain
                      }
                  }        
        clients.append(client)
    
    if print_results:
        print("IP" + " "*18 +"MAC" + " "*19 + "Host Name")    
        for client in clients:
            print("{:16}    {}     {}".format(client['client']['ip'], client['client']['mac'], client['client']['name']))
    if load_to_elastic:    
        send_to_elastic(clients, filename, index)
        
    print('Scan Complete')

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg
    
def run_scan():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filename", required=False,
                    help="config.ini file", metavar="File",
                    type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-index", dest="index", required=False,
                    help="elasticsearch index.json", metavar="File",
                    type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()

    while True:
        scan_network(args.filename, args.index)
        time.sleep(1800) # 30 Minutes

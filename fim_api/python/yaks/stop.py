from fog05 import FIMAPI
import uuid
import json
import sys
import os
import time

DESC_FOLDER = '.'



def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip):
    a = FIMAPI(ip)

    fdus={}

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {}'.format(n))
        discs = a.fdu.list()
        for d_id in discs:
            info = a.fdu.instance_list(d_id)
            print ('info : {}'.format(info))
            if n in info:
                time.sleep(1)
                i_ids=info[n]
                for iid in i_ids:
                    print ('Terminating iid : {}'.format(iid))
                    a.fdu.terminate(iid)
                    a.fdu.offload(d_id)

    nets = a.network.list()
    if nets:
        print ('networks : {}'.format(nets))
        for n in nets:
            net_uuid=n['uuid']
            print ('net_id : {}'.format(net_uuid))
            a.network.remove_network(net_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[Usage] {} <yaks ip:port>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1])

import os
from fog05 import FIMAPI
from fog05.interfaces.FDU import FDU
import sys
import time
import json


DESC_FOLDER = '.'
net_desc = []
#descs = [
#        ('fdu_detect_faces.json','4a560914-1c3e-4966-9fa8-7f0acc903253'),
#        ('fdu_display_faces.json','4a560914-1c3e-4966-9fa8-7f0acc903253'),
#        ('fdu_recognize_faces.json','4a560914-1c3e-4966-9fa8-7f0acc903253')
#    ]
descs = [('fdu_test.json','1d6407ab-d1e7-e478-1bc2-7d4f5d77666b')]
def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def read(fname):
    return open(fname).read()


def main(ip):
    a = FIMAPI(ip)

    fdus = {}
    nets = []

    #input('Press enter to instantiate the demo')

    for d in net_desc:
        path_d = os.path.join(DESC_FOLDER,d)
        netd = json.loads(read(path_d))
        a.network.add_network(netd)
        nets.append(netd['uuid'])
        time.sleep(1)

    for d,n in descs:
        path_d = os.path.join(DESC_FOLDER,d)
        fdu_d = FDU(json.loads(read(path_d)))
        res = a.fdu.onboard(fdu_d)
        fdu_id = res.get_uuid()
        print ('fdu_id : {}'.format(fdu_id))
        inst_info = a.fdu.instantiate(fdu_id, n)
        iid = inst_info.get_uuid()
        print ('iid : {}'.format(iid))
        print('Instantiated: {}'.format(fdu_d.get_name()))
        fdus.update({fdu_id: iid})
        time.sleep(1)

    print('Bye!')



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage {} <yaks ip:port>")
        exit(-1)
    main(sys.argv[1])

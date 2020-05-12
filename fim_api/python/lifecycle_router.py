from fog05 import FIMAPI
import uuid
import json
import sys
import os
from fog05_sdk.interfaces.FDU import FDU


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, fdufile, netfile, routerfile):
    a = FIMAPI(ip)

    nodes = a.node.list()
    if len(nodes) == 0:
        print('No nodes')
        exit(-1)

    print('Nodes:')
    for n in nodes:
        print('UUID: {}'.format(n))

    fdu_d = FDU(json.loads(read_file(fdufile)))
    net_d = json.loads(read_file(netfile))
    router_d = json.loads(read_file(routerfile))

    # e_uuid = fdu_d.get('uuid')
    n_uuid = net_d.get('uuid')
    r_uuid = router_d.get('uuid')

    input("Press enter to create network")
    a.network.add_network(net_d)


    n1 = '4a560914-1c3e-4966-9fa8-7f0acc903253' #nuc

    input('press enter to onboard descriptor')
    desc = a.fdu.onboard(fdu_d)
    e_uuid = desc.get_uuid()
    input('Press enter to instantiate')
    rec = a.fdu.instantiate(e_uuid, n1)
    intsid = rec.get_uuid()
    input('Press enter to create router')
    a.network.add_router(n1, router_d)


    # input("press enter to add router port")
    # res = a.network.add_router_port(n1, r_uuid, "INTERNAL", "6cc2aa30-1dcf-4c93-a57e-433fd0bd498e", "192.168.234.1/24")
    # print(res)

    # input("press enter to remove router port")
    # res = a.network.remove_router_port(n1, r_uuid, "6cc2aa30-1dcf-4c93-a57e-433fd0bd498e")
    # print(res)

    # input('Press enter to stop')
    # a.entity.stop(e_uuid, n1, i_uuid)
    # input('Press enter to clean')
    # a.entity.clean(e_uuid, n1, i_uuid)
    # input('Press enter to undefine')
    # a.entity.undefine(e_uuid, n1)

    # input('Press enter to migrate')

    #res = a.entity.migrate(e_uuid, i_uuid, n1, n2)
    #print('Res is: {}'.format(res))
    input('Press enter to remove')

    a.fdu.terminate(intsid)
    a.fdu.offload(e_uuid)
    input('Press enter to remove router')
    a.network.remove_router(n1, r_uuid)
    input("Press enter to remove network")
    a.network.remove_network(n_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('[Usage] {} <yaks ip:port> <path to fdu descripto> <path to net descriptor> <path to router descriptor>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

from fog05 import FIMAPI
from fog05sdk.interfaces.FDU import FDU
import uuid
import json
import sys
import os


def read_file(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def main(ip, fdufile, netfile):
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

    n_uuid = net_d.get('uuid')




    #n1 = 'a2d358aa-af2b-42cb-8d23-a89e88b97e5c' #fosmed
    n1 = '4a560914-1c3e-4966-9fa8-7f0acc903253' #nuc
    # n1 = '53712df2-9649-4a21-be2e-80eed00ff9ce' #ubuntuvm1
    #n1 = 'a4589fae-0493-40cf-b976-2d03020d060d' #foskvm
    # n1 = '53712df2-9649-4a21-be2e-80eed00ff9ce' #ubuntuvm1
    # n1 = 'd07b095f-7948-4f9b-95cc-c61029f6c3c3' #fosdbg

    input("Press enter to create network")
    a.network.add_network(net_d)
    a.network.add_network_to_node(net_d, n1)

    input('press enter to onboard descriptor')
    res = a.fdu.onboard(fdu_d)
    e_uuid = res.get_uuid()
    input('Press enter to intantiate')
    inst_info = a.fdu.instantiate(e_uuid, n1)
    instid = inst_info.get_uuid()


    # input('Press enter to stop')
    # a.entity.stop(e_uuid, n1, i_uuid)
    # input('Press enter to clean')
    # a.entity.clean(e_uuid, n1, i_uuid)
    # input('Press enter to undefine')
    # a.entity.undefine(e_uuid, n1)

    # input('Press enter to migrate')
    input('Press get info')
    info = a.fdu.instance_info(instid)
    print(info.to_json())

    #res = a.entity.migrate(e_uuid, i_uuid, n1, n2)
    #print('Res is: {}'.format(res))
    input('Press enter to terminate')

    a.fdu.terminate(instid)
    a.fdu.offload(e_uuid)
    input("Press enter to remove network")
    a.network.remove_network_from_node(n_uuid, n1)
    a.network.remove_network(n_uuid)

    exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('[Usage] {} <yaks ip:port> <path to fdu descripto> <path to net descriptor>'.format(
            sys.argv[0]))
        exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

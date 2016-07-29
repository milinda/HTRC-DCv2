import libvirt
import sys

with libvirt.open('qemu+tcp://192.168.1.16:16509/system') as conn:
    sp = conn.storagePoolLookupByName('default')
    if sp is None:
        print('Failed to find storage pool \'default\'.')
        exit(1)

    stgvols = sp.listVolumes()
    print("Number of volumes = {}".format(len(stgvols))

# This shows that we can't use libvirt.open with 'with' construct
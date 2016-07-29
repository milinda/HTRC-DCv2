from __future__ import print_function
import sys
import libvirt
from xml.dom import minidom

poolName = 'default'

conn = libvirt.open('qemu+tcp://192.168.1.16:16509/system')
if conn == None:
    print('Failed to open connection to qemu:///system', file=sys.stderr)
    exit(1)

sp = conn.storagePoolLookupByName(poolName)
if sp == None:
    print('Failed to find storage pool '+poolName, file=sys.stderr)
    exit(1)

stgvols = sp.listVolumes()
print('Storage pool: \n'+ str(sp.XMLDesc()))
for stgvol in stgvols :
    print('  Storage vol: '+stgvol)
    volinfo = sp.storageVolLookupByName(stgvol)
    print('  Vol path: ' + str(volinfo.path()))
    print('  Vol allocation: ' + str(volinfo.info()[1]))

conn.close()
exit(0)
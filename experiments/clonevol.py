from __future__ import print_function
import sys
import libvirt
from xml.dom import minidom
from xml.etree import ElementTree


def _create_volume_xml(vol_name, vol_allocation, vol_capacity, target_path_root=''):
        volume = ElementTree.Element('volume')
        
        name = ElementTree.SubElement(volume, 'name')
        name.text = '{}.img'.format(vol_name)

        allocation = ElementTree.SubElement(volume, 'allocation')
        allocation.text = vol_allocation

        capacity = ElementTree.SubElement(volume, 'capacity')
        capacity.text = str(vol_capacity)

        #target = ElementTree.SubElement(volume, 'target')

        #path = ElementTree.SubElement(target, 'path')
        #path.text = '{}/{}.img'.format(target_path_root, vol_name)

        return ElementTree.tostring(volume)

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

for vol in stgvols:
    if vol == 'ubuntu-16-04.img':
        volref = sp.storageVolLookupByName(vol)
        new_vol_xml = _create_volume_xml('colned-1', 0, volref.info()[1])
        print(new_vol_xml)
        newvol = sp.createXMLFrom(new_vol_xml, volref, 0)
        if newvol is None:
            print('Failed to clone volume ' + vol)
            exit(1)
        print('new vol path ' + newvol.path())
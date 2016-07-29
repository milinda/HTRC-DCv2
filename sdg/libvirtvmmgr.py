# -*- coding: utf-8 -*-
"""
    Libvirt VM Manager
    ~~~~~~~~~~~~~~~~~~
    VM Manager written on top of libvirt.

    :author Milinda Pathirage, Samitha Liyanage
    :maintainer Milinda Pathirage, Samitha Liyanage
    :license LGPLv2+
"""
import libvirt
import logging
from dcmgr import VMManager
from xml.etree import ElementTree


class LibVirtVMManager(VMManager):
    class Factory:
        def create(self, config={}):
            return LibVirtVMManager(config)

    lv_hosts = {}

    def __init__(self, config={}):
        lv_hosts_config = config['LV_HOSTS']
        for host_id, host_config in lv_hosts_config.iteritems():
            logging.info('Loading host configuration for host {}'
                         .format(host_id))
            host_info = {}
            host_uri = _get_libvirt_remote_uri(host_config)
            host_info['uri'] = host_uri
            host_info['capacity'] = _get_lv_host_capability(host_uri)
            host_info['config'] = host_config
            lv_hosts[host_id] = host_info

    def create_vm(self, img, vcpus, mem):
        pass

    def _clone_image(self, src_img_name, vm_id, storage_pool, host_uri):
        conn = libvirt.open(host_uri)
        try:
            sp = conn.storagePoolLookupByName(storage_pool)
            if sp is None:
                err_msg = 'Failed to locate storage pool {}'.format(storage_pool)
                logging.error(err_msg)
                raise RuntimeError(err_msg)

            srcvol = sp.storageVolLookupByName(src_img_name)
            newvol_xml = _create_volume_xml(vm_id, srcvol.info()[1], 12)
            newvol = sp.createXMLFrom(newvol_xml, srcvol, 0)
            
            if newvol is None:
                err_msg = 'Failed to clone image {}'.format(src_img_name)
                logging.err(err_msg)
                raise RuntimeError(err_msg)

            return newvol.path()
        finally:
            conn.close()

    def _is_image_exists(self, image_name, storage_pool, host_uri):
        conn = libvirt.openReadOnly(host_uri)
        try:
            if conn is None:
                err_msg = 'Cannot connect to {}'.format(host_uri)
                logging.error(err_msg)
                raise RuntimeError(err_msg)

            sp = conn.storagePoolLookupByName(storage_pool)
            if sp is None:
                err_msg = 'Failed to locate storage pool {}'.format(storage_pool)
                logging.error(err_msg)
                raise RuntimeError(err_msg)

            vol = sp.storageVolLookupByName(image_name)
            return vol is not None
        finally:
            conn.close()

    def _get_lv_host_capability(self, host_uri):
        # This should talk to DB to get existing capsules running this host.
        # Then update the available slots accordingly (May be libvirtd already
        # do that).
        conn = libvirt.openReadOnly(host_uri)

        try:
            if conn is None:
                raise RuntimeError('Cannot connect to {}'.format(host_uri))

            vcpus = conn.getMaxVcpus(None)
            nodeinfo = conn.getInfo()
            memlist = conn.getCellsFreeMemory(0, nodeinfo[4])

            freemem = 0

            for cell_freemem in memlist:
                freemem += cell_freemem

            return {'max_vcpus': vcpus, 'freemem': freemem,
                    'totalmem': nodeinfo[1]}
        finally:
            conn.close()

    def _get_libvirt_remote_uri(self, host_config={}):
        # TODO: This currently works only for non-secure tcp. Fix it to add
        # other type of uris.
        return '{}+{}://{}:{}/{}'.format(host_config['driver'],
                                         host_config['transport'],
                                         host_config['hostname'],
                                         host_config['port'],
                                         host_config['path'])

    def _create_volume_xml(self, vol_name, vol_capacity, vol_allocation, vol_allocation_unit='G'):
        volume = ElementTree.Element('volume')
        
        name = ElementTree.SubElement(volume, 'name')
        name.text = '{}.img'.format(vol_name)

        allocation = ElementTree.SubElement(volume, 'allocation')
        allocation.set('unit', vol_allocation_unit)
        allocation.text = str(vol_allocation)

        capacity = ElementTree.SubElement(volume, 'capacity')
        capacity.text = str(vol_capacity)

        return ElementTree.tostring(volume)

    def _create_vm_xml(self, host_config, name, memmax, mem, vcpus, vnc_port, img_path, 
                       memunit='KiB', arch='x86_64'):
        domain = ElementTree.Element('domain')
        domain.set('type', host_config['type'])

        dname = ElementTree.SubElement(domain, 'name')
        dname.text = name

        memory = ElementTree.SubElement(domain, 'memory')
        memory.set('unit', memunit)
        memory.text = memmax

        curmem = ElementTree.SubElement(domain, 'currentMemory')
        curmem.set('unit', memunit)
        curmem.text = mem

        vcpus = ElementTree.SubElement(domain, 'vpu')
        vcpus.text = vcpus

        os = ElementTree.SubElement(domain, 'os')
        os_type = ElementTree.SubElement(os, 'type')
        os_type.set('arch', arch)
        os_type.text = host_config['os_type']
        os_boot = ElementTree.SubElement(os, 'boot')
        os_boot.set('dev', 'hd')

        devices = ElementTree.SubElement(domain, 'devices')
        devices_emu = ElementTree.SubElement(devices, 'emulator')
        devices_emu.text = host_config['emulator']

        # Disk types should be configurable and it should be possible to figure out proper source.
        disk = ElementTree.SubElement(devices, 'disk')
        disk.set('device', 'disk')
        disk.set('type', 'file')

        source = ElementTree.SubElement(disk, 'source')
        source.set('file', img_path)

        target = ElementTree.SubElement(disk, 'target')
        target.set('dev', 'hda')

        network_interface = ElementTree.SubElement(devices, 'interface')
        network_interface.set('type', 'network')
        network_source = ElementTree.SubElement(network_interface, 'source')
        network_source.set('network', 'default')

        video = ElementTree.SubElement(devices, 'video')
        vmodel = ElementTree.SubElement(video, 'model')
        vmodel.set('type', 'vmware')

        graphics = ElementTree.SubElement(devices, 'graphics')
        graphics.set('type', 'vnc')
        graphics.set('port', '-1')
        graphics.set('autoport', 'yes')
        
        return ElementTree.tostring(domain)

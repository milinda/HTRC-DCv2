# -*- coding: utf-8 -*-
"""
    Libvirt DC Manager
    ~~~~~~~~~~
    Data Capsules Manager written on of libvirt.

    :author Milinda Pathirage, Samitha Liyanage
    :maintainer Milinda Pathirage, Samitha Liyanage
    :license LGPLv2+
"""
import libvirt
import logging
from dcmgr import DCManager
from xml.etree import ElementTree
from string import ascii_lowercase


class LibVirtDCManager(DCManager):
    class Factory:
        def create(self, config={}):
            return LibVirtDCManager(config)

    dc_hosts = {}

    def __init__(self, config={}):
        dc_hosts_config = config['DC_HOSTS']
        for host_id, host_config in dc_hosts_config.iteritems():
            logging.info('Loading host configuration for host {}'
                         .format(host_id))
            host_info = {}
            host_uri = _get_libvirt_remote_uri(host_config)
            host_info['uri'] = host_uri
            host_info['capacity'] = _get_dc_host_capability(host_uri)
            host_info['config'] = host_config
            dc_hosts[host_id] = host_info

    def _is_image_exists(self, image_name, storage_pool, host_uri):
        conn = libvirt.openReadOnly(host_uri)
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

        conn.close()
        
        return vol is not None


    def _get_dc_host_capability(self, host_uri):
        # This should talk to DB to get existing capsules running this host.
        # Then update the available slots accordingly (May be libvirtd already
        # do that).
        conn = libvirt.openReadOnly(host_uri)
        if conn is None:
            raise RuntimeError('Cannot connect to {}'.format(host_uri))

        vcpus = conn.getMaxVcpus(None)
        nodeinfo = conn.getInfo()
        memlist = conn.getCellsFreeMemory(0, nodeinfo[4])

        conn.close()

        freemem = 0

        for cell_freemem in memlist:
            freemem += cell_freemem

        return {'max_vcpus': vcpus, 'freemem': freemem,
                'totalmem': nodeinfo[1]}

    def _get_libvirt_remote_uri(self, host_config={}):
        # TODO: This currently works only for non-secure tcp. Fix it to add
        # other type of uris.
        return '{}+{}://{}:{}/{}'.format(host_config['driver'],
                                         host_config['transport'],
                                         host_config['hostname'],
                                         host_config['port'],
                                         host_config['path'])

    def _create_capsule_xml(host_config, name, memmax, mem, vcpus, vnc_port, image, disk_volume, 
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

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
from dcmgr import DCManager


class LibVirtDCManager(DCManager):
    class Factory:
        def create(self, config={}):
            return LibVirtDCManager(config)

    dc_hosts = {}

    def __init__(self, config={}):
        dc_hosts_config = config['DC_HOSTS']
        for host_id, host_config in dc_hosts_config.iteritems():
            host_info = {}
            host_uri = _get_libvirt_remote_uri(host_config)
            host_info['uri'] = host_uri
            host_info['capacity'] = _get_dc_host_capability(host_uri)
            dc_hosts[host_id] = host_info

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

    def _create_vm_xml():
        pass

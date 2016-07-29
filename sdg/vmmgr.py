# -*- coding: utf-8 -*-
"""
    DC Manager
    ~~~~~~~~~~
    Data Capsules Manager abstraction.

    :author Milinda Pathirage, Samitha Liyanage
    :maintainer Milinda Pathirage, Samitha Liyanage
    :license LGPLv2+
"""
import libvirt


class VMManagerFactory:
    factories = {}

    def add_factory(id, vm_mgr_factory):
        VMManagerFactory.factories.put[id] = vm_mgr_factory
    add_factory = staticmethod(add_factory)

    def create_vm_mgr(id, config):
        if id not in VMManagerFactory.factories:
            VMManagerFactory.factories[id] = eval(id + '.Factory()')
        return VMManagerFactory.factories[id].create(config)
    create_vm_mgr = staticmethod(create_vm_mgr)
# To create a VMManager instance use VMManagerFactory.create_dc_mgr()


class VMManager(object):
    def create_vm(self):
        raise NotImplementedError

    def switch_vm_mode(self):
        raise NotImplementedError

    def stop_vm(self):
        raise NotImplementedError

    def delete_vm(self):
        raise NotImplementedError


class MockVMManager(VMManager):
    class Factory:
        def create(self, config={}):
            return MockVMManager()

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


class DCManagerFactory:
    factories = {}

    def add_factory(id, dc_mgr_factory):
        DCManagerFactory.factories.put[id] = dc_mgr_factory
    add_factory = staticmethod(add_factory)

    def create_dc_mgr(id, config):
        if id not in DCManagerFactory.factories:
            DCManagerFactory.factories[id] = eval(id + '.Factory()')
        return DCManagerFactory.factories[id].create(config)
    create_dc_mgr = staticmethod(create_dc_mgr)
# To create a DCManager instance use DCManagerFactory.create_dc_mgr()


class DCManager(object):
    def create_capsule(self):
        raise NotImplementedError

    def switch_capsule_mode(self):
        raise NotImplementedError

    def stop_capsule(self):
        raise NotImplementedError

    def delete_capsule(self):
        raise NotImplementedError


class MockDCManager(DCManager):
    class Factory:
        def create(self, config={}):
            return MockDCManager()

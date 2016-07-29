# -*- coding: utf-8 -*-
"""
    DCv2
    ~~~~
    HTRC Data Capsules v2 written on top of libvirt.

    :author Milinda Pathirage, Samitha Liyanage
    :maintainer Milinda Pathirage, Samitha Liyanage
    :license LGPLv2+
"""
from __future__ import print_function
import sys
import os
import libvirt
import logging
import logging.config
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

app = Flask(__name__, instance_relative_config=True)
app.config.update(dict(
    DEBUG=True,
    VM_HOST='192.168.1.16:16509',
    API_HOST='192.168.1.14'))
app.config.from_pyfile('config.py')
app.config.from_envvar('DCV2_SETTINGS', silent=True)

try:
    with app.open_instance_resource('logging.conf') as f:
        logging.config.fileConfig(f.name)
except:
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)
    logging.warning('Couldn\'t find logging configuration (logging.conf)' +
                    ' file in instance directory.')

conn_str = 'qemu+tcp://' + app.config['VM_HOST'] + '/system'
conn = libvirt.open(conn_str)
if conn is None:
    print('Failed to open connection to ' + conn_str, file=sys.stderr)
    exit(1)

xmlconfig = """
<domain type='qemu'>
  <name>demo2</name>
  <uuid>c9b6fdbd-cdaf-9455-926a-d65c16db1809</uuid>
  <memory unit='MB'>2048</memory>
  <vcpu>2</vcpu>
  <os>
    <type arch='x86_64' machine='pc'>hvm</type>
    <boot dev='hd'/>
    </os>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <source file='/var/lib/libvirt/images/ubuntu-16-04.img'/>
      <driver name='qemu' type='qcow2'/>
      <target dev='hda'/>
    </disk>
    <input type='mouse' bus='ps2'/>
    <interface type='network'>
      <source network='default'/>
    </interface>
    <graphics type='vnc' port='16011' listen='0.0.0.0' passwd='vnc'/>
  </devices>
</domain>
"""


@app.route('/')
def version():
    return jsonify(name='HTRC Data Capsules v2',
                   version='0.0.1',
                   host=app.config['API_HOST'])


@app.route('/capsules', methods=['GET'])
def get_capsules():
    return jsonify(vm_host=conn.getHostname(),
                   max_vcpus=conn.getMaxVcpus(None),
                   vm_host_info=conn.getInfo())


@app.route('/capsules', methods=['POST'])
def create_capsule():
    dom = conn.defineXML(xmlconfig)

    if dom is None:
        response = jsonify(error='Failed to define a domain from an XML' +
                           'definition.')
        response.status_code = 500
        return response

    if dom.create() < 0:
        response = jsonify(error='Can not boot guest domain.')
        response.status_code = 500
        return response

    return jsonify(domains=conn.listDomainsID())

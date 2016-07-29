from __future__ import print_function
import sys
import libvirt

conn = libvirt.open('qemu+tcp://192.168.1.16:16509/system')
if conn is None:
    print('Failed to open connection to qemu+tcp://192.168.1.16:16509/system', file=sys.stderr)
    exit(1)

ifaceNames = conn.listInterfaces()

print("Active host interfaces:")
for ifaceName in ifaceNames:
    print('  '+ifaceName)

ifaceNames = conn.listDefinedInterfaces()

print("Inactive host interfaces:")
for ifaceName in ifaceNames:
    print('  '+ifaceName)

iface = conn.interfaceLookupByName('em1')

print("The interface XML description is:\n"+iface.XMLDesc(0))

# lookup the default network by name
network = conn.networkLookupByName('default')
print('Virtual network default:')
print('  name: '+network.name())
print('  UUID: '+network.UUIDString())
print('  bridge: '+network.bridgeName())
print('  autostart: '+str(network.autostart()))
print('  is active: '+str(network.isActive()))
print('  is persistent: '+str(network.isPersistent()))
print()

print('Unsetting autostart')
network.setAutostart(0)
print('  autostart: '+str(network.autostart()))
print('Setting autostart')
network.setAutostart(1)
print('  autostart: '+str(network.autostart()))
print()

xml = network.XMLDesc(0)
print('XML description:')
print(xml)

conn.close()
exit(0)
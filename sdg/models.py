import enum
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class VMHost(db.Model):
    __tablename__ = 'vmhost'

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(256), unique=True)
    port = db.Column(db.Integer)
    driver = db.Column(db.String(16))
    virt_type = db.Column(db.String(16))
    transport = db.Column(db.String(16))
    path = db.Column(db.String(128))
    emulator = db.Column(db.String(256))
    os_type = db.Column(db.String(16))
    storage_pool = db.Column(db.String(64))
    vcpus = db.Column(db.Integer)
    free_mem = db.Column(db.Integer)
    total_mem = db.Column(db.Integer)
    
    def __init__(self, vcpus, free_mem, total_mem, config={}):
        self.vcpus = vcpus
        self.free_mem = free_mem
        self.total_mem = total_mem
        self.hostname = config['hostname']
        self.port = config['port']
        self.driver = config['driver']
        self.virt_type = config['type']
        self.transport = config['transport']
        self.path = config['path']
        self.emulator = config['emulator']
        self.os_type = config['os_type']
        self.storage_pool = config['storage_pool']

    def __repr__(self):
        return '<VMHost(driver={},transport={},hostname={},port={},path={})>'.format(
            self.driver, self.transport, self.hostname, self.port, self.path)

class VMImage(db.Model):
    __tablename__ = 'vmimage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))
    login_username = db.Column(db.String(64))
    login_password = db.Column(db.String(64))
    
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<VMImage(name={})>'.format(self.name)

class VMMode(enum.Enum):
    m = 'm'
    s = 's'

class VMState(enum.Enum):
    created = 'created'
    running = 'running'
    stopped = 'stopped'
    suspended = 'suspended'
    failed = 'failed'
    deleted = 'deleted'

class VM(db.Model):
    __tablename__ = 'vm'

    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.Enum('m','s', name='vm_modes'))
    state = db.Column(db.Enum('created', 'running', 'stopped', 'suspended', 'failed', 'deleted', 
                              name='vm_states'))
    hostname = db.Column(db.String(128))
    ssh_port = db.Column(db.Integer)
    vnc_port = db.Column(db.Integer)
    image_id = db.Column(db.Integer, db.ForeignKey('vmimage.id'))
    vmimage = db.relationship('VMImage', backref=db.backref('vms', lazy='dynamic'))
    vnc_username = db.Column(db.String(64))
    vnc_password = db.Column(db.String(64))
    vcpus = db.Column(db.Integer)
    memmb = db.Column(db.Integer)
    diskgb = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('vms', lazy='dynamic'))
    vmhost_id = db.Column(db.Integer, db.ForeignKey('vmhost.id'))
    vmhost = db.relationship('VMHost', backref=db.backref('vms', lazy='dynamic'))
    
    def __init__(self, mode, state, hostname, ssh_port, vnc_port, image, vnc_username, vnc_password,
                 vcpus, memmb, diskgb, user, vmhost):
        self.mode = mode
        self.state = state
        self.hostname = hostname
        self.ssh_port = ssh_port
        self.vnc_port = vnc_port
        self.vmimage = image
        self.vnc_username = vnc_username
        self.vnc_password = vnc_password
        self.vcpus = vcpus
        self.memmb = memmb
        self.diskgb = diskgb
        self.user = user
        self.vmhost = vmhost

    def __repr__(self):
        return '<VM(id={},mode={},state={},hostname={},user={})>'.format(
               self.id, self.mode, self.state, self.hostname, self.user_id)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    cpu_quota = db.Column(db.Integer)
    mem_quota = db.Column(db.Integer)
    disk_quota = db.Column(db.Integer)
    
    def __init__(self, username, email, cpu_quota, mem_quota, disk_quota):
        self.username = username
        self.email = email
        self.cpu_quota = cpu_quota
        self.mem_quota = mem_quota
        self.disk_quota = disk_quota

    def __repr__(self):
        return '<User(username={},email={}))>'.format(self.username, self.email)

class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    notified_at = db.Column(db.DateTime)
    content = db.Column(db.LargeBinary)
    vm_id = db.Column(db.Integer, db.ForeignKey('vm.id'))
    vm = db.relationship('VM', backref=db.backref('results', lazy='dynamic'))
    notified = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)

    def __init__(self, content, vm):
        self.content = content
        self.vm = vm

    def __repr__(self):
        return '<Result(id={},create_at={},vm_id={})>'.format(self.id, self.create_at, self.vm_id)

class VMActivity(db.Model):
    __tablename__ = 'vmactivity'

    id = db.Column(db.BigInteger, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    vm_id = db.Column(db.Integer, db.ForeignKey('vm.id'))
    vm = db.relationship('VM', backref=db.backref('activities', lazy='dynamic'))
    prev_mode = db.Column(db.Enum('m','s', name='vm_modes'))
    curr_mode = db.Column(db.Enum('m','s', name='vm_modes'))
    prev_state = db.Column(db.Enum('created', 'running', 'stopped', 'suspended', 'failed', 'deleted', 
                              name='vm_states'))
    curr_state = db.Column(db.Enum('created', 'running', 'stopped', 'suspended', 'failed', 'deleted', 
                              name='vm_states'))
    
    def __init__(self, vm, prev_mode, curr_mode, prev_state, curr_state):
        self.vm = vm
        self.prev_mode = prev_mode
        self.curr_mode = curr_mode
        self.prev_state = prev_state
        self.curr_state = curr_state

    def __repr__(self):
        return '<VMActivity(ts={},prev_mode={},curr_mode={},prev_state={},curr_state={})>'.format(
               self.timestamp, self.prev_mode, self.curr_mode, self.prev_state, self.curr_state)
import subprocess

__author__ = 'Amir H.'


def bucket_type_create(name, properties={}):
    comm = "riak-admin bucket-type create {bt_name} '{prop}'"
    bt_props = {'props': properties}
    bt_props = str(bt_props).replace("'", '"').lower()
    comm = comm.format(bt_name=name, prop=bt_props)
    return subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()
    # subprocess.call(comm, shell=True)


def bucket_type_activate(name):
    comm = "riak-admin bucket-type activate {bt_name}".format(bt_name=name)
    return subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()


def bucket_type_status(name, property=None):
    if property:
        comm = "riak-admin bucket-type status {bt_name} | grep {prop}".format(bt_name=name, prop=property)
    else:
        comm = "riak-admin bucket-type status {bt_name}".format(bt_name=name)
    return subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()


def bucket_type_list():
    comm = "riak-admin bucket-type list"
    return subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()


def bucket_type_update(name, properties={}):
    comm = "riak-admin bucket-type update {bt_name} '{prop}'"
    bt_props = {'props': properties}
    bt_props = str(bt_props).replace("'", '"').lower()
    comm = comm.format(bt_name=name, prop=bt_props)
    return subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()

import socket


def etcd_is_available():
    try:
        socket.create_connection(('127.0.0.1', 4001), 1.0)
    except socket.error:
        return False
    else:
        return True

import zmq

import oscope.zmq_socket_helpers as socket_helpers


def test_ctx_manager():
    with socket_helpers.PublishContext(("ipc://foo", "ipc://bar")) as pub_socket:
        assert isinstance(pub_socket, zmq.Socket)


def test_ipc_temp_unique():
    with socket_helpers.IPCTemp(["test1"]) as paths1:
        with socket_helpers.IPCTemp(["test1"]) as paths2:
            unique_names = set()
            unique_names.update(paths1)
            unique_names.update(paths2)
            
            assert len(unique_names) == 2, unique_names

def test_linked_pair():
    with socket_helpers.LinkedPubSubPair() as (pub, sub):
        for x in range(30):
            msg = "foo-" + str(x)
            pub.send_pyobj(msg)
            assert sub.poll(timeout=1000)
            assert sub.recv_pyobj() == msg

import pytest
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

def test_ipc_temp_too_long():
    with pytest.raises(AssertionError):
        socket_helpers.IPCTemp(["f" * (socket_helpers.IPC_PATH_MAX_LEN + 1)]).__enter__()

def test_LinkedPubSubPair_basic():
    with socket_helpers.LinkedPubSubPair() as (pub, sub):
        pass

def test_LinkedPubSubPair_sends():
    with socket_helpers.LinkedPubSubPair() as (pub, sub):
        for x in range(30):
            msg = "foo-" + str(x)
            pub.send_pyobj(msg)
            assert sub.poll(timeout=1000)
            assert sub.recv_pyobj() == msg

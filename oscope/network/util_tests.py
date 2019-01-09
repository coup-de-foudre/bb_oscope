import time

import pytest
import zmq

import oscope.base
import oscope.network.util as socket_helpers


def test_ipc_temp_unique():
    with socket_helpers.IPCTemp(["test1"]) as paths1:
        with socket_helpers.IPCTemp(["test1"]) as paths2:
            unique_names = set()
            unique_names.update(paths1)
            unique_names.update(paths2)

            oscope.base.assert_length(unique_names, 2)

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

def test_PubSocket_ctx_manager():
    with socket_helpers.PubSocket() as pub_socket:
        pub_socket.bind("ipc://foo")
        oscope.base.assert_isinstance(pub_socket, zmq.Socket)

def test_NoisyPubSocket_smoke():
    with socket_helpers.NoisyPubSocket() as skt:
        oscope.base.assert_isinstance(skt, zmq.Socket)

def test_NoisyPubSocket():
    with socket_helpers.NoisyPubSocket() as pub:
        with socket_helpers.SubscribeSocket() as sub:
            port = pub.bind_to_random_port("tcp://127.0.0.1")
            sub.connect("tcp://localhost:{}".format(port))
            sub.subscribe("")
            assert sub.poll(timeout=1000) > 0, ":("


import oscope.scope.fake
import oscope.trace
import oscope.trace_publish
import oscope.zmq_socket_helpers as helpers

def test_publishing():
    fakescope = oscope.scope.fake.FakeOscilloscope()

    with helpers.LinkedPubSubPair() as (pub, sub):
        publisher = oscope.trace_publish.TracePublisher(pub, fakescope)

        for x in range(10):
            publisher.push()

            assert sub.poll(timeout=1000)
            packaged = sub.recv_multipart()

            meta, trace = oscope.trace.unpackage_trace_data(packaged)

            assert meta["sequence"] == x
        
    